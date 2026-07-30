#!/usr/bin/env node

/**
 * DESIGN.md Validator — PerformaIT
 * 
 * Valida um DESIGN.md sem impor nomenclatura de tokens nem convenções externas.
 * Filosofia: verifica FORMA (sintaxe, tipos, referências), não CONVENÇÃO (naming).
 * 
 * Contraste via APCA 0.0.98G-W3 (Myndex/apca-w3, W3/AGWG license).
 * 
 * Uso:
 *   node validate-design-md.js DESIGN.md
 *   node validate-design-md.js DESIGN.md --verbose
 */

const fs   = require('fs');
const path = require('path');

// ─── APCA 0.0.98G-W3 ────────────────────────────────────────────────────────

const APCA = {
  mainTRC:      2.4,
  normBG:       0.56,
  normTXT:      0.57,
  revTXT:       0.62,
  revBG:        0.65,
  sRco:         0.2126729,
  sGco:         0.7151522,
  sBco:         0.0721750,
  blkThrs:      0.022,
  blkClmp:      1.414,
  loClip:       0.1,
  deltaYmin:    0.0005,
  scaleBoW:     1.14,
  loBoWoffset:  0.027,
  scaleWoB:     1.14,
  loWoBoffset:  0.027,
};

function hexToRGB(hex) {
  const h = hex.replace('#', '');
  if (!/^[0-9a-fA-F]{6}$/.test(h)) return null;
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}

function sRGBtoY(rgb) {
  let [r, g, b] = rgb.map(c => Math.pow(c / 255, APCA.mainTRC));
  let Y = APCA.sRco * r + APCA.sGco * g + APCA.sBco * b;
  if (Y < APCA.blkThrs) {
    Y = Y + Math.pow(APCA.blkThrs - Y, APCA.blkClmp);
  }
  return Y;
}

function calcLc(textHex, bgHex) {
  const tRGB = hexToRGB(textHex);
  const bRGB = hexToRGB(bgHex);
  if (!tRGB || !bRGB) return null;

  const Yt = sRGBtoY(tRGB);
  const Yb = sRGBtoY(bRGB);

  if (Math.abs(Yb - Yt) < APCA.deltaYmin) return 0;

  let Sapc;
  if (Yb > Yt) {
    // texto escuro sobre fundo claro (BoW)
    Sapc = (Math.pow(Yb, APCA.normBG) - Math.pow(Yt, APCA.normTXT)) * APCA.scaleBoW;
  } else {
    // texto claro sobre fundo escuro (WoB)
    Sapc = (Math.pow(Yb, APCA.revBG) - Math.pow(Yt, APCA.revTXT)) * APCA.scaleWoB;
  }

  if (Math.abs(Sapc) < APCA.loClip) return 0;

  const Lc = Sapc > 0
    ? (Sapc - APCA.loBoWoffset) * 100
    : (Sapc + APCA.loWoBoffset) * 100;

  return Math.round(Lc * 10) / 10;
}

// ─── YAML FRONT MATTER PARSER (sem dependências externas) ───────────────────

function parseFrontMatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return { yaml: null, body: content };
  return { raw: match[1], body: content.slice(match[0].length) };
}

// Parser YAML mínimo: suporta flat keys e nested de até 3 níveis
// Suficiente para o schema do DESIGN.md
function parseYAML(raw) {
  const lines = raw.split('\n');
  const result = {};
  let currentL1 = null;
  let currentL2 = null;

  for (const line of lines) {
    if (!line.trim() || line.trim().startsWith('#')) continue;

    const indent = line.match(/^(\s*)/)[1].length;
    const kv = line.trim().match(/^([^:]+):\s*(.*)?$/);
    if (!kv) continue;

    const key = kv[1].trim();
    const val = (kv[2] || '').trim().replace(/^["']|["']$/g, '');

    if (indent === 0) {
      currentL1 = key;
      currentL2 = null;
      result[key] = val || {};
    } else if (indent === 2) {
      if (typeof result[currentL1] !== 'object') result[currentL1] = {};
      currentL2 = key;
      result[currentL1][key] = val || {};
    } else if (indent === 4) {
      if (currentL2) {
        if (typeof result[currentL1][currentL2] !== 'object') {
          result[currentL1][currentL2] = {};
        }
        result[currentL1][currentL2][key] = val;
      }
    }
  }
  return result;
}

// ─── VALIDAÇÕES ──────────────────────────────────────────────────────────────

const VALID_UNITS   = ['px', 'em', 'rem'];
const SECTION_ORDER = [
  'overview', 'colors', 'typography', 'layout',
  'elevation', 'shapes', 'components', "do's and don'ts", 'agent prompt guide'
];

// Aliases aceitos pelo spec
const SECTION_ALIASES = {
  'brand & style':       'overview',
  'brand and style':     'overview',
  'layout & spacing':    'layout',
  'layout and spacing':  'layout',
  'elevation & depth':   'elevation',
  'elevation and depth': 'elevation',
  "do's & don'ts":       "do's and don'ts",
  'dos and donts':       "do's and don'ts",
  'agent prompt guide':  'agent prompt guide',
};

function normSection(h) {
  const s = h.replace(/^##\s*/, '').trim().toLowerCase();
  return SECTION_ALIASES[s] || s;
}

function isValidHex(v)       { return /^#[0-9a-fA-F]{6}$/.test(v); }
function isValidDimension(v) { return VALID_UNITS.some(u => v.endsWith(u) && !isNaN(parseFloat(v))); }
function isValidDimOrNum(v)  { return isValidDimension(v) || !isNaN(Number(v)); }
function isTokenRef(v)       { return /^\{[a-zA-Z0-9._-]+\}$/.test(v); }

function resolveRef(ref, tokens) {
  const path = ref.replace(/[{}]/g, '').split('.');
  let cur = tokens;
  for (const p of path) {
    if (!cur || typeof cur !== 'object') return undefined;
    cur = cur[p];
  }
  return cur;
}

// ─── RUNNER ──────────────────────────────────────────────────────────────────

function validate(filePath, verbose = false) {
  const errors   = [];
  const warnings = [];
  const infos    = [];

  const add = (list, msg) => list.push(msg);
  const err  = msg => add(errors,   `❌ ${msg}`);
  const warn = msg => add(warnings, `⚠️  ${msg}`);
  const info = msg => verbose && add(infos, `ℹ️  ${msg}`);

  // ── Leitura do arquivo ───────────────────────────────────────────────────
  if (!fs.existsSync(filePath)) {
    err(`Arquivo não encontrado: ${filePath}`);
    return report(errors, warnings, infos);
  }
  const content = fs.readFileSync(filePath, 'utf8');

  // ── Front matter ─────────────────────────────────────────────────────────
  const { raw, body } = parseFrontMatter(content);

  if (!raw) {
    warn('Nenhum YAML front matter encontrado. O arquivo é válido sem ele, mas tokens machine-readable não estarão disponíveis para agentes.');
  }

  let tokens = {};
  if (raw) {
    tokens = parseYAML(raw);

    // name obrigatório
    if (!tokens.name || typeof tokens.name !== 'string' || !tokens.name.trim()) {
      err('YAML: campo `name` ausente ou vazio. É obrigatório.');
    } else {
      info(`name: "${tokens.name}"`);
    }

    // ── colors ──────────────────────────────────────────────────────────
    if (tokens.colors) {
      if (typeof tokens.colors !== 'object') {
        err('YAML: `colors` deve ser um mapa de tokens.');
      } else {
        for (const [k, v] of Object.entries(tokens.colors)) {
          if (typeof v !== 'string') {
            err(`YAML colors.${k}: valor deve ser string hex. Recebido: ${JSON.stringify(v)}`);
          } else if (!isValidHex(v)) {
            err(`YAML colors.${k}: "${v}" não é um hex válido (#RRGGBB em sRGB).`);
          } else {
            info(`colors.${k}: ${v} ✓`);
          }
        }
      }
    }

    // ── typography ──────────────────────────────────────────────────────
    if (tokens.typography) {
      if (typeof tokens.typography !== 'object') {
        err('YAML: `typography` deve ser um mapa de tokens.');
      } else {
        for (const [k, v] of Object.entries(tokens.typography)) {
          if (typeof v !== 'object') {
            err(`YAML typography.${k}: deve ser um objeto com propriedades tipográficas.`);
            continue;
          }
          // fontFamily obrigatório
          if (!v.fontFamily) {
            err(`YAML typography.${k}: "fontFamily" ausente.`);
          }
          // fontSize
          if (v.fontSize && !isValidDimension(v.fontSize)) {
            err(`YAML typography.${k}.fontSize: "${v.fontSize}" não é uma dimensão válida (px, em, rem).`);
          }
          // fontWeight deve ser número
          if (v.fontWeight !== undefined) {
            const fw = Number(v.fontWeight);
            if (isNaN(fw) || fw < 100 || fw > 900 || fw % 100 !== 0) {
              // pesos variáveis como 450 também são válidos — relaxar para apenas checar se é número
              if (isNaN(Number(v.fontWeight))) {
                err(`YAML typography.${k}.fontWeight: "${v.fontWeight}" deve ser um valor numérico (ex: 400, 600, 700).`);
              }
            }
          }
          // lineHeight
          if (v.lineHeight && !isValidDimOrNum(v.lineHeight)) {
            err(`YAML typography.${k}.lineHeight: "${v.lineHeight}" não é válido. Use dimensão (px/em/rem) ou número unitless (ex: 1.5).`);
          }
          // letterSpacing
          if (v.letterSpacing && !isValidDimension(v.letterSpacing) && !v.letterSpacing.endsWith('em')) {
            warn(`YAML typography.${k}.letterSpacing: "${v.letterSpacing}" — confirme que é uma dimensão válida.`);
          }
          info(`typography.${k} ✓`);
        }
      }
    }

    // ── rounded ─────────────────────────────────────────────────────────
    if (tokens.rounded) {
      for (const [k, v] of Object.entries(tokens.rounded)) {
        if (!isValidDimension(String(v))) {
          err(`YAML rounded.${k}: "${v}" não é uma dimensão válida (px, em, rem).`);
        } else {
          info(`rounded.${k}: ${v} ✓`);
        }
      }
    }

    // ── spacing ─────────────────────────────────────────────────────────
    if (tokens.spacing) {
      for (const [k, v] of Object.entries(tokens.spacing)) {
        if (!isValidDimOrNum(String(v))) {
          err(`YAML spacing.${k}: "${v}" não é válido. Use dimensão (px/em/rem) ou número unitless.`);
        } else {
          info(`spacing.${k}: ${v} ✓`);
        }
      }
    }

    // ── components ──────────────────────────────────────────────────────
    const VALID_COMP_PROPS = [
      'backgroundColor', 'textColor', 'typography',
      'rounded', 'padding', 'size', 'height', 'width'
    ];

    if (tokens.components) {
      for (const [compName, props] of Object.entries(tokens.components)) {
        if (typeof props !== 'object') {
          err(`YAML components.${compName}: deve ser um mapa de propriedades.`);
          continue;
        }
        for (const [prop, val] of Object.entries(props)) {
          const strVal = String(val);

          // propriedade desconhecida — warn, não erro (flexibilidade)
          if (!VALID_COMP_PROPS.includes(prop)) {
            warn(`YAML components.${compName}.${prop}: propriedade não reconhecida pelo spec. Será preservada, mas agentes podem ignorá-la.`);
          }

          // resolver referências
          if (isTokenRef(strVal)) {
            const resolved = resolveRef(strVal, tokens);
            if (resolved === undefined) {
              err(`YAML components.${compName}.${prop}: referência "${strVal}" não encontrada no YAML.`);
            } else {
              info(`components.${compName}.${prop}: ${strVal} → ${resolved} ✓`);
            }
            continue;
          }

          // validar por tipo de propriedade
          if (['backgroundColor', 'textColor'].includes(prop)) {
            if (!isValidHex(strVal)) {
              err(`YAML components.${compName}.${prop}: "${strVal}" não é hex válido nem referência {path.to.token}.`);
            }
          }
          if (['rounded', 'padding', 'size', 'height', 'width'].includes(prop)) {
            if (!isValidDimension(strVal)) {
              warn(`YAML components.${compName}.${prop}: "${strVal}" — confirme que é uma dimensão válida (px/em/rem).`);
            }
          }
        }

        // ── APCA: validar par textColor / backgroundColor ──────────────
        const bg   = props.backgroundColor;
        const text = props.textColor;

        const resolveColor = v => {
          if (!v) return null;
          const s = String(v);
          if (isValidHex(s)) return s;
          if (isTokenRef(s)) {
            const r = resolveRef(s, tokens);
            return r && isValidHex(String(r)) ? String(r) : null;
          }
          return null;
        };

        const bgHex   = resolveColor(bg);
        const textHex = resolveColor(text);

        if (bgHex && textHex) {
          const Lc = calcLc(textHex, bgHex);
          if (Lc === null) {
            warn(`APCA components.${compName}: não foi possível calcular Lc (hex inválido após resolução).`);
          } else {
            const absLc = Math.abs(Lc);
            const polarity = Lc >= 0 ? 'texto escuro / fundo claro' : 'texto claro / fundo escuro';
            info(`APCA components.${compName}: Lc ${Lc} (${polarity})`);

            if (absLc < 30) {
              err(`APCA components.${compName}: Lc ${absLc} — contraste insuficiente para qualquer uso de texto.`);
            } else if (absLc < 45) {
              warn(`APCA components.${compName}: Lc ${absLc} — adequado apenas para texto decorativo/placeholder. Insuficiente para texto funcional.`);
            } else if (absLc < 60) {
              warn(`APCA components.${compName}: Lc ${absLc} — abaixo de Lc 60. Só adequado para headings grandes (≥24px, peso 700+).`);
            } else if (absLc < 75) {
              info(`APCA components.${compName}: Lc ${absLc} — adequado para labels/botões (≥14px, peso 600+). Insuficiente para corpo de texto.`);
            } else {
              info(`APCA components.${compName}: Lc ${absLc} — adequado para corpo de texto. ✓`);
            }
          }
        } else if (bg && !bgHex) {
          warn(`APCA components.${compName}: backgroundColor "${bg}" não pôde ser resolvido para hex — contraste não calculado.`);
        } else if (text && !textHex) {
          warn(`APCA components.${compName}: textColor "${text}" não pôde ser resolvido para hex — contraste não calculado.`);
        }
      }
    }

    // ── referências soltas no YAML (fora de components) ─────────────────
    function checkRefs(obj, path) {
      if (typeof obj === 'string' && isTokenRef(obj)) {
        const resolved = resolveRef(obj, tokens);
        if (resolved === undefined) {
          err(`YAML ${path}: referência "${obj}" não encontrada.`);
        }
      } else if (typeof obj === 'object' && obj !== null) {
        for (const [k, v] of Object.entries(obj)) {
          checkRefs(v, `${path}.${k}`);
        }
      }
    }
    // verificar refs fora de components (rounded, spacing raramente usam refs, mas é válido)
    for (const [section, val] of Object.entries(tokens)) {
      if (section === 'components') continue; // já verificado acima
      checkRefs(val, section);
    }
  }

  // ── Markdown body: ordem das seções ─────────────────────────────────────
  if (body) {
    const headings = [...body.matchAll(/^##\s+.+/gm)].map(m => m[0]);
    const normalized = headings.map(normSection);

    // checar duplicatas
    const seen = {};
    for (const h of normalized) {
      if (seen[h]) {
        err(`Markdown: seção duplicada "${h}". O spec rejeita headings ## duplicados.`);
      }
      seen[h] = true;
    }

    // checar ordem relativa (apenas entre seções do spec)
    const specSections = normalized.filter(h => SECTION_ORDER.includes(h));
    for (let i = 1; i < specSections.length; i++) {
      const prev = SECTION_ORDER.indexOf(specSections[i - 1]);
      const curr = SECTION_ORDER.indexOf(specSections[i]);
      if (curr < prev) {
        warn(`Markdown: seção "${specSections[i]}" aparece antes de "${specSections[i-1]}". O spec recomenda a ordem canônica.`);
      }
    }

    // seções presentes
    info(`Seções encontradas: ${normalized.join(', ')}`);

    // seções customizadas (não do spec) — OK, apenas informar
    const custom = normalized.filter(h => !SECTION_ORDER.includes(h));
    if (custom.length > 0) {
      info(`Seções customizadas (fora do spec, preservadas): ${custom.join(', ')}`);
    }
  }

  return report(errors, warnings, infos, tokens);
}

function report(errors, warnings, infos, tokens) {
  console.log('\n══════════════════════════════════════════');
  console.log('  DESIGN.md Validator — PerformaIT');
  console.log('  Contraste: APCA 0.0.98G-W3');
  console.log('══════════════════════════════════════════\n');

  if (infos.length)    infos.forEach(m => console.log(m));
  if (warnings.length) warnings.forEach(m => console.log(m));
  if (errors.length)   errors.forEach(m => console.log(m));

  console.log('');
  if (errors.length === 0 && warnings.length === 0) {
    console.log('✅ DESIGN.md válido. Nenhum problema encontrado.');
  } else {
    if (errors.length)   console.log(`${errors.length} erro(s) encontrado(s).`);
    if (warnings.length) console.log(`${warnings.length} aviso(s) encontrado(s).`);
    if (errors.length)   console.log('\nCorreija os erros antes de usar o DESIGN.md com agentes.');
  }
  console.log('');

  return { errors, warnings, infos };
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

const args    = process.argv.slice(2);
const file    = args.find(a => !a.startsWith('--')) || 'DESIGN.md';
const verbose = args.includes('--verbose');

validate(path.resolve(file), verbose);
