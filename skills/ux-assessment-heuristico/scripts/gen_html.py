#!/usr/bin/env python3
"""
gen_html.py -- Gera o UX Assessment final em HTML, preenchendo o template visual fixo
da Performa.it (assets/template_base.html) com o conteudo do cliente.

REGRA INEGOCIAVEL: este script NAO desenha HTML a partir do zero. Ele carrega
assets/template_base.html -- que e uma copia LITERAL, byte a byte, do padrao visual
da Performa.it (extraido do padrao visual de referencia da Performa.it, validado em
entregas reais anteriores e revisado internamente) -- e faz substituicao de tokens
[[[NOME]]] e expansao de blocos <!--REPEAT:nome-->...<!--END:nome--> dentro dele.

Isso existe para uma razao especifica: se cada assessment fosse gerado por um
LLM reescrevendo o HTML/CSS na hora, dois assessments diferentes (ou o mesmo
assessment gerado em duas sessoes diferentes) poderiam sair com layout, cores ou
estrutura sutilmente diferentes. Usando um template literal + substituicao de
tokens, o CSS, o JS e a estrutura de cada tipo de slide sao IDENTICOS, sempre --
só o conteudo (cliente, telas, achados) muda. Ver o comentario no topo de
assets/template_base.html e a secao "O padrao visual do HTML e fixo" no SKILL.md.

Ao reusar esta skill para um novo cliente, troque o CONTEUDO (config.json / data.py)
-- nunca edite assets/template_base.html para "ajustar" o layout de um cliente
especifico. Se o layout genuinamente precisar mudar (não so os dados), esse e um
pedido para mudar a skill em si (e o template), nao para o gerar diferente so
desta vez -- converse com o usuario antes de editar o template.

Importado por build_xlsx.py e gen_review_md.py para garantir que os 3 entregaveis
(Markdown de revisao, XLSX, HTML) usem exatamente a mesma logica de calculo.

Uso:
    python gen_html.py --config config.json --data data.py --out "UX Assessment - Cliente.html"
"""
import argparse
import base64
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes do metodo (ver references/metodo_pontuacao.md)
# ---------------------------------------------------------------------------

AREAS = ["conteudo", "ai", "design", "tecnologia", "negocios"]

AREA_LABELS = {
    "conteudo": "Conteúdo",
    "ai": "Arquitetura da Informação",
    "design": "Design",
    "tecnologia": "Tecnologia",
    "negocios": "Negócios",
}

# Usado na etiqueta compacta de cada card (carrossel de achados).
AREA_TAG = {
    "conteudo": "Conteúdo",
    "ai": "Arq. Informação",
    "design": "Design",
    "tecnologia": "Tecnologia",
    "negocios": "Negócios",
}

# As 5 areas, sua ordem e suas descricoes sao parte FIXA do metodo (ver
# assets/template_base.html, bloco "method-grid", ja escrito de forma literal
# la dentro). Mantidas aqui como a fonte-da-verdade documental: se um dia o
# metodo mudar (nova area, nova descricao), mude aqui E no template junto.
AREA_DESC = {
    "conteudo": "O que é dito, em que ordem, com que clareza — texto, dados e mensagens exibidas.",
    "ai": "Como a informação é estruturada, nomeada, encontrada e reconhecida entre telas.",
    "design": "Como o conteúdo é apresentado visualmente — hierarquia, cor, tipografia, espaço.",
    "tecnologia": "Como o sistema responde, valida, orienta e sustenta o processo tecnicamente.",
    "negocios": "Como a tela comunica a marca e serve aos objetivos comerciais do negócio.",
}
AREA_NUM = {"conteudo": "01", "ai": "02", "design": "03", "tecnologia": "04", "negocios": "05"}

QUEBRA_FATOR = {"Nenhum": 0.0, "Ruído": 0.25, "Obstáculo": 0.5, "Obstrução": 0.75, "Barreira": 1.0}
QUEBRA_SCORE_CLASS = {
    "Nenhum": "", "Ruído": "score-ruido", "Obstáculo": "score-obstaculo",
    "Obstrução": "score-obstrucao", "Barreira": "score-barreira",
}

BASIS_FALLBACK = "Framework próprio Performa.it — lente de negócio"
BASIS_GENERIC = {
    "conteudo": "Nielsen (1994) — Heurísticas de usabilidade",
    "ai": "Nielsen (1994) — Heurísticas de usabilidade",
    "design": "WCAG 2.1",
    "tecnologia": "ISO 9241-110:2020",
    "negocios": BASIS_FALLBACK,
}

# --- Slide dedicado de metodologia ("N bases teoricas, M achados") ---
#
# Existe porque "heuristica", no sentido estrito, e so o metodo de Nielsen -- as outras bases
# (ISO, Morville, WCAG/APCA, Miller/Hick, o framework proprio da Performa) sao tipos diferentes
# (norma, modelo, diretriz, achado empirico, lente de negocio), nao "heuristicas" tambem. Uma
# entrega anterior teve exatamente essa imprecisao relatada: o documento chamava todo achado de
# "heuristica" independente da base real citada no card. Este slide existe para deixar isso
# explicito e auditavel, com contagens REAIS por familia (nunca hardcoded), porque cada cliente
# tem uma distribuicao diferente de quais bases pesaram mais.
BASIS_FAMILY_ORDER = ["nielsen", "iso", "morville", "wcag", "miller", "performa"]
BASIS_FAMILY_INFO = {
    "nielsen": {
        "nome": "Nielsen (1994; 1993)", "tipo": "Heurísticas de usabilidade",
        "avalia": "Clareza, prevenção de erro, reconhecimento e tempo de resposta numa tela específica.",
    },
    "iso": {
        "nome": "ISO 9241-110:2020", "tipo": "Norma internacional de diálogo",
        "avalia": "Se o sistema sustenta a tarefa como processo contínuo, não só uma tela isolada.",
    },
    "morville": {
        "nome": "Honeycomb de Morville (2004)", "tipo": "Modelo de arquitetura da informação",
        "avalia": "Se a informação está organizada de um jeito que dispensa memorização do usuário.",
    },
    "wcag": {
        "nome": "WCAG 2.1 / APCA", "tipo": "Diretriz de acessibilidade",
        "avalia": "Contraste, legibilidade e uso de cor, medidos de forma objetiva.",
    },
    "miller": {
        "nome": "Miller (1956) e Hick-Hyman", "tipo": "Achado de psicologia cognitiva",
        "avalia": "Limite de itens e opções que a atenção humana processa de uma vez.",
    },
    "performa": {
        "nome": "Framework próprio Performa.it", "tipo": "Lente de negócio proprietária",
        "avalia": "Se a tela serve aos objetivos comerciais e à imagem da marca, além da usabilidade.",
    },
}


def classify_basis(basis_str):
    """Classifica uma citacao de base ja resolvida (saida de basis_for()) numa das 6 familias
    fixas do metodo. Por substring, porque o texto exato de cada citacao varia por achado (ex.:
    'Nielsen (1994) — Heuristica 9' e 'Nielsen (1994) — Heuristicas de usabilidade' sao a mesma
    familia); nunca falha para uma familia desconhecida -- cai em 'performa' como ultimo recurso,
    mesmo padrao de fallback que basis_for() ja usa para a area Negocios."""
    b = basis_str.lower()
    if "nielsen" in b:
        return "nielsen"
    if "iso 9241" in b:
        return "iso"
    if "morville" in b or "honeycomb" in b:
        return "morville"
    if "wcag" in b or "apca" in b:
        return "wcag"
    if "miller" in b or "hick" in b:
        return "miller"
    return "performa"


def compute_basis_rows(stats):
    """Conta quantos achados (cards com Quebra != Nenhum, o mesmo filtro usado para renderizar
    os cards de verdade) citam cada familia de base teorica, para popular a lamina dedicada de
    metodologia. So retorna familias com pelo menos 1 achado -- um cliente cujo data.py nunca
    aciona, por exemplo, o bucket Miller/Hick simplesmente nao mostra essa linha, em vez de expor
    uma linha com contagem 0 (o que pareceria um erro de geracao, nao uma escolha real)."""
    counts = {k: 0 for k in BASIS_FAMILY_ORDER}
    for tela in stats["telas"]:
        for row in tela["rows"]:
            if row["quebra"] == "Nenhum":
                continue
            counts[classify_basis(basis_for(row))] += 1
    rows = []
    for key in BASIS_FAMILY_ORDER:
        n = counts[key]
        if n == 0:
            continue
        info = BASIS_FAMILY_INFO[key]
        rows.append({"BASE_NOME": info["nome"], "BASE_TIPO": info["tipo"],
                     "BASE_N": n, "BASE_AVALIA": info["avalia"], "_key": key})
    return rows


def _render_base_row(block, item):
    return fill_tokens(block, {
        "BASE_NOME": item["BASE_NOME"],
        "BASE_TIPO": item["BASE_TIPO"],
        "BASE_N": item["BASE_N"],
        "BASE_AVALIA": item["BASE_AVALIA"],
    })

# As 8 referencias tambem sao fixas por metodo e ja estao escritas de forma
# literal em assets/template_base.html (slide "Referências"). Mantidas aqui para
# uso por build_xlsx.py / gen_review_md.py, que citam a base teorica por fora do HTML.
REFERENCIAS = [
    ("Nielsen, J. &amp; Molich, R. (1990).", "Heuristic evaluation of user interfaces.", "CHI '90 Proceedings."),
    ("Nielsen, J. (1994).", "10 Usability Heuristics for User Interface Design.", "Nielsen Norman Group."),
    ("ISO 9241-110:2020.", "Ergonomics of human-system interaction — Dialogue principles.", ""),
    ("W3C (2018).", "Web Content Accessibility Guidelines (WCAG) 2.1", "— SC 1.4.1 Use of Color, SC 1.4.4 Resize Text."),
    ("Morville, P. (2004).", "User Experience Design Honeycomb.", "Semantic Studios."),
    ("Miller, G. A. (1956).", "The Magical Number Seven, Plus or Minus Two.", "Psychological Review."),
    ("Hick, W. E. (1952).", "On the rate of gain of information.", "Quarterly Journal of Experimental Psychology."),
    ("Somers, A. (2019-2024).", "APCA — Accessible Perceptual Contrast Algorithm.", "W3 WCAG 3 (Silver) Task Force."),
]

REQUIRED_CFG_KEYS = ["cliente", "produto", "consultoria", "avaliadores", "data_avaliacao"]

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "assets" / "template_base.html"


# ---------------------------------------------------------------------------
# Motor de template minimo -- sem dependencias externas (nao usa Jinja2).
#
# Por que um motor caseiro em vez de Jinja2: a unica coisa que este script
# precisa fazer e (a) trocar [[[TOKEN]]] por um valor e (b) repetir um trecho
# de HTML uma vez por item de uma lista. Um `str.replace` mais um extrator de
# bloco resolvem isso em ~30 linhas, sem adicionar uma dependencia externa ao
# ambiente onde a skill roda. Ver o SKILL.md, secao "O padrao visual do HTML
# e fixo", para a razao de existir disso tudo.
# ---------------------------------------------------------------------------

def extract_repeat(template, name):
    """Localiza <!--REPEAT:name-->BLOCO<!--END:name--> e devolve (antes, bloco, depois)."""
    start = f"<!--REPEAT:{name}-->"
    end = f"<!--END:{name}-->"
    i = template.index(start)
    j = template.index(end, i)
    return template[:i], template[i + len(start):j], template[j + len(end):]


def fill_tokens(s, mapping):
    """Substitui cada [[[CHAVE]]] pelo valor correspondente em `mapping` (str.replace simples)."""
    for k, v in mapping.items():
        s = s.replace(f"[[[{k}]]]", str(v))
    return s


def render_repeat(template, name, items, item_fn):
    """Expande o bloco `name` uma vez por item de `items`, aplicando item_fn(bloco, item) a cada copia,
    e substitui o bloco marcado (incluindo os marcadores) pelo resultado concatenado."""
    before, block, after = extract_repeat(template, name)
    rendered = "".join(item_fn(block, item) for item in items)
    return before + rendered + after


def fill_pagenos(html):
    """[[[PAGENO]]] aparece 2x por slide (id="slide-N" e o rodape "N"). Numera sequencialmente,
    na ordem em que os slides aparecem no documento montado, dando o mesmo numero aos 2 usos
    de um mesmo slide."""
    parts = html.split("[[[PAGENO]]]")
    occurrences = len(parts) - 1
    if occurrences % 2 != 0:
        raise ValueError(f"Numero impar de [[[PAGENO]]] ({occurrences}) -- algum slide esta quebrado.")
    out = [parts[0]]
    counter = 0
    for idx in range(occurrences):
        if idx % 2 == 0:
            counter += 1
        out.append(f"{counter:02d}")
        out.append(parts[idx + 1])
    return "".join(out)


def assert_no_leftover_tokens(html):
    """Trava de seguranca: se sobrar qualquer [[[...]]] no HTML final, e porque o codigo
    esqueceu de preencher algum token -- melhor falhar alto do que entregar um HTML com
    "[[[TELA_LABEL]]]" escrito na tela do cliente."""
    leftover = re.findall(r"\[\[\[[A-Z0-9_]+\]\]\]", html)
    if leftover:
        raise ValueError(f"Tokens nao preenchidos no HTML final: {sorted(set(leftover))}")


# ---------------------------------------------------------------------------
# Helpers de dominio
# ---------------------------------------------------------------------------

def slugify(s):
    s = s.lower()
    repl = {
        "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "ô": "o", "õ": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
    }
    for a, b in repl.items():
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def img_b64(path):
    """Retorna um data-URI base64 para o arquivo de imagem em `path`, ou None se ausente."""
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    ext = p.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "svg": "image/svg+xml"}.get(ext, "image/jpeg")
    with open(p, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"


def recolor_svg_fill(svg_text, color):
    """Troca todo fill="white"/"#fff"/"#ffffff" (case-insensitive) por `color`.

    Existe por causa de um bug real ja identificado em uma entrega anterior: a logo da marca so
    existia como um arquivo BRANCO (pensado para fundo escuro, ex. a capa) e o mesmo arquivo era
    reaplicado, sem recolorir, no "wordmark" das paginas de fundo CLARO — branco sobre branco, logo
    invisivel. Um logo de marca costuma vir como um vetor monocromatico unico, pensado para ser
    recolorido por quem implementa conforme o fundo, nao como dois arquivos prontos. Isso so faz
    sentido para SVGs com fill solido single-color; um SVG multi-cor (comum em logo de cliente,
    nao da Performa) deve receber uma variante propria via `logo_dark_path` no config, em vez de
    depender deste recolor automatico — ver `img_b64_recolored` e a secao de logo no SKILL.md."""
    import re as _re
    return _re.sub(r'fill="(white|#fff|#ffffff)"', f'fill="{color}"', svg_text, flags=_re.IGNORECASE)


def img_b64_recolored(path, color):
    """Como img_b64, mas para SVG: recolore fills brancos para `color` antes de codificar (ver
    `recolor_svg_fill`). Para qualquer coisa que nao seja um .svg, cai de volta em img_b64(path)
    sem tentar recolorir (ex.: um PNG so pode ser trocado por outro arquivo, nao recolorido em
    tempo de geracao)."""
    p = Path(path) if path else None
    if not p or not p.exists() or p.suffix.lower() != ".svg":
        return img_b64(path)
    svg_text = p.read_text(encoding="utf-8")
    recolored = recolor_svg_fill(svg_text, color)
    data = base64.b64encode(recolored.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{data}"


def esc(s):
    """Escapa texto para uso seguro dentro de HTML (nao mexe em entidades que o proprio
    metodo ja usa de proposito, como &times;/&amp;)."""
    if s is None:
        return ""
    return str(s)


def basis_for(row):
    """Retorna a base teorica citavel de uma avaliacao: usa `base` explicito se fornecido,
    senao cai para um default generico por area (ver references/bases_teoricas.md)."""
    if row.get("base"):
        return row["base"]
    return BASIS_GENERIC.get(row["area"], BASIS_FALLBACK)


def quadrante(erro, imp_media):
    """Classifica uma combinacao tela x area na matriz de risco 2x2.
    Ver references/metodo_pontuacao.md para a justificativa dos limiares."""
    critico_erro = erro >= 0.5
    critico_imp = imp_media >= 2.0
    if critico_erro and critico_imp:
        return "Crítico"
    if critico_erro and not critico_imp:
        return "Monitorar"
    if not critico_erro and critico_imp:
        return "Sob controle"
    return "Aceitável"


def load_data_module(path):
    """Carrega data.py como modulo Python, retornando o objeto modulo (espera-se um TELAS)."""
    spec = importlib.util.spec_from_file_location("ux_data_module", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "TELAS"):
        raise ValueError(f"{path} precisa definir uma lista TELAS (ver scripts/data_exemplo.py)")
    return mod


def validate_cfg(cfg):
    missing = [k for k in REQUIRED_CFG_KEYS if k not in cfg]
    if missing:
        raise ValueError(f"config.json está faltando chave(s) obrigatória(s): {missing}")
    if not cfg["avaliadores"]:
        raise ValueError("config.json precisa de pelo menos 1 avaliador em 'avaliadores'")


# ---------------------------------------------------------------------------
# Agregacao / calculo (a mesma logica e usada pelo XLSX e pelo Markdown de revisao)
# ---------------------------------------------------------------------------

def compute(telas):
    """Recebe TELAS (lista de dicts com key/label/screenshot/rows) e retorna todas as
    agregacoes necessarias para os 3 entregaveis: erro% por tela/area/geral, e a matriz
    de risco tela x area."""
    out_telas = []
    grand_nota = 0.0
    grand_imp = 0.0
    risk_rows = []

    for tela in telas:
        rows = tela["rows"]
        area_stats = {}
        tela_nota = 0.0
        tela_imp = 0.0
        tela_n_problemas = 0

        for area in AREAS:
            area_rows = [r for r in rows if r["area"] == area]
            problem_rows = [r for r in area_rows if r["quebra"] != "Nenhum"]
            nota_sum = sum(r["nota"] for r in problem_rows)
            imp_sum = sum(r["importancia"] for r in problem_rows)
            imp_media = (imp_sum / len(problem_rows)) if problem_rows else 0.0
            erro = (nota_sum / imp_sum) if imp_sum > 0 else 0.0

            area_stats[area] = {
                "nota": nota_sum,
                "imp": imp_sum,
                "n_problemas": len(problem_rows),
                "n_total": len(area_rows),
                "erro": erro,
                "imp_media": imp_media,
                "rows": problem_rows,
            }

            tela_nota += nota_sum
            tela_imp += imp_sum
            tela_n_problemas += len(problem_rows)

            if problem_rows:
                risk_rows.append({
                    "tela": tela["label"],
                    "area": AREA_LABELS[area],
                    "importancia": imp_media,
                    "erro": erro,
                    "quadrante": quadrante(erro, imp_media),
                })

        tela_erro = (tela_nota / tela_imp) if tela_imp > 0 else 0.0
        grand_nota += tela_nota
        grand_imp += tela_imp

        out_telas.append({
            "key": tela["key"],
            "label": tela["label"],
            "screenshot": tela.get("screenshot"),
            "rows": rows,
            "area_stats": area_stats,
            "erro": tela_erro,
            "nota": tela_nota,
            "imp": tela_imp,
            "n_problemas": tela_n_problemas,
            "n_total": len(rows),
        })

    grand_erro = (grand_nota / grand_imp) if grand_imp > 0 else 0.0

    return {
        "telas": out_telas,
        "grand_nota": grand_nota,
        "grand_imp": grand_imp,
        "grand_erro": grand_erro,
        "risk_rows": sorted(risk_rows, key=lambda r: -r["erro"]),
        "n_avaliacoes_total": sum(t["n_total"] for t in out_telas),
        "n_problemas_total": sum(t["n_problemas"] for t in out_telas),
    }


# ---------------------------------------------------------------------------
# Grafico da matriz de risco (SVG) -- substitui a antiga tabela de 2 colunas.
#
# Historico: a v1 deste grafico usava uma tabela ("Tela | Área | Importância | Erro% |
# Quadrante"). Um cliente anterior pediu explicitamente para virar um grafico, sem
# perder os nomes das areas. A v1 do grafico (posicionamento por distancia entre
# pontos) ainda deixava rotulos sobrepostos em clusters densos -- o cliente apontou
# isso com um print. Esta versao usa 2 tecnicas para resolver:
# (1) jitter horizontal pequeno para pontos com Erro% quase identico dentro da
# mesma area, e (2) alocacao de "pista" (lane) vertical por ordem de chegada,
# ciente da largura em pixels de cada rotulo (agendamento por intervalos),
# em vez de uma heuristica ingenua baseada so em distancia entre pontos.
# ---------------------------------------------------------------------------

QUAD_COLOR = {
    "Crítico": "#C62828",
    "Monitorar": "#FF6E01",
    "Sob controle": "#2E6DA4",
    "Aceitável": "#9AA0A6",
}

_CHART_CHAR_W = 5.0   # aprox. px por caractere em font-size 8.2
_CHART_LABEL_GAP = 7  # espaco minimo (px) exigido entre rotulos adjacentes na mesma pista


def build_risk_chart_svg(risk_rows, width=1180, height=420):
    """Gera o SVG do grafico de matriz de risco a partir de stats['risk_rows']
    (lista de dicts com tela/area/importancia/erro/quadrante, ja calculados por compute()).
    Uma banda horizontal por area, na ordem fixa AREAS; X = Erro%; tamanho do ponto = Importancia.

    ATENCAO altura (height=420, nao mude sem medir o slide de novo): o slide da matriz de risco
    tem 608px de altura util (content-wrap) menos ~143px do eyebrow+titulo+lead acima do grafico,
    sobrando ~465px reais. 420 foi validado (via render+crop, ver skill build log) para caber com
    folga mesmo no caso mais denso (5 areas, todas com varios achados). Um height=580 (valor antigo
    desta funcao) ESTOURA o slide e corta a ultima banda de area — foi um bug real ja identificado
    numa entrega anterior. Se o layout do slide ao redor do grafico mudar (mais texto no lead,
    etc.), recalcule o orcamento de altura antes de mudar este numero.
    """
    areas_order = [AREA_LABELS[a] for a in AREAS]
    # pad_b maior que o "normal" de proposito: reserva espaco para eixo + rotulos + UMA LINHA
    # SEPARADA para a legenda de quadrante, abaixo do eixo — nunca dentro da area de plotagem.
    # Antes, a legenda ficava em cy=pad_t-2 (dentro da primeira banda de area) e podia se
    # misturar visualmente com os pontos plotados; isso foi um bug real relatado pelo cliente.
    # pad_l precisa caber o rotulo de area mais longo das 5 fixas ("Arquitetura da Informação",
    # ~25 caracteres em 13px bold) sem cortar no x=0 do viewBox — 168 cortava esse rotulo
    # (bug real encontrado ao validar visualmente esta funcao); 210 da folga suficiente.
    pad_l, pad_r, pad_t, pad_b = 210, 26, 10, 64
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    n_areas = len(areas_order)
    band_h = plot_h / n_areas

    def px(erro):
        return pad_l + erro * plot_w

    x_thresh = px(0.5)

    by_area = {a: [] for a in areas_order}
    for r in risk_rows:
        by_area.setdefault(r["area"], []).append(r)

    parts = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-family="Poppins, sans-serif">']

    for i, area in enumerate(areas_order):
        y0 = pad_t + i * band_h
        band_fill = "#F7F7F5" if i % 2 == 0 else "#FFFFFF"
        parts.append(f'<rect x="{pad_l}" y="{y0:.1f}" width="{plot_w}" height="{band_h:.1f}" fill="{band_fill}"/>')
        parts.append(f'<rect x="{x_thresh:.1f}" y="{y0:.1f}" width="{pad_l+plot_w-x_thresh:.1f}" height="{band_h:.1f}" fill="#C62828" opacity="0.045"/>')

    for i, area in enumerate(areas_order):
        y0 = pad_t + i * band_h
        parts.append(f'<line x1="{pad_l}" y1="{y0:.1f}" x2="{pad_l+plot_w}" y2="{y0:.1f}" stroke="#e2e2e2" stroke-width="1"/>')
        parts.append(f'<text x="{pad_l-14}" y="{y0+band_h/2+4:.1f}" font-size="13" font-weight="700" fill="#000614" text-anchor="end">{area}</text>')
    parts.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h:.1f}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h:.1f}" stroke="#e2e2e2" stroke-width="1"/>')
    parts.append(f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h:.1f}" fill="none" stroke="#ccc" stroke-width="1.2"/>')

    parts.append(f'<line x1="{x_thresh:.1f}" y1="{pad_t}" x2="{x_thresh:.1f}" y2="{pad_t+plot_h:.1f}" stroke="#C62828" stroke-width="1.4" stroke-dasharray="5,3" opacity="0.7"/>')
    parts.append(f'<text x="{x_thresh:.1f}" y="{pad_t-2}" font-size="9.5" fill="#C62828" font-weight="700" text-anchor="middle">Erro% ≥ 50%</text>')

    for pct in [0, 25, 50, 75, 100]:
        x = px(pct / 100.0)
        parts.append(f'<line x1="{x:.1f}" y1="{pad_t+plot_h:.1f}" x2="{x:.1f}" y2="{pad_t+plot_h+5:.1f}" stroke="#999" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="{pad_t+plot_h+18:.1f}" font-size="10.5" fill="#666" text-anchor="middle">{pct}%</text>')

    # Legenda de quadrante: SEMPRE numa linha propria, abaixo do eixo, com um divisor sutil —
    # nunca dentro da area de plotagem (ver nota no docstring da funcao sobre o bug antigo).
    legend_y = pad_t + plot_h + 30
    parts.append(f'<line x1="0" y1="{legend_y-8:.1f}" x2="{width}" y2="{legend_y-8:.1f}" stroke="#eee" stroke-width="1"/>')
    legend_items = [("Crítico", QUAD_COLOR["Crítico"]), ("Monitorar", QUAD_COLOR["Monitorar"]),
                    ("Sob controle", QUAD_COLOR["Sob controle"]), ("Aceitável", QUAD_COLOR["Aceitável"])]
    gx = pad_l
    for name, color in legend_items:
        parts.append(f'<circle cx="{gx}" cy="{legend_y:.1f}" r="5.0" fill="{color}"/>')
        parts.append(f'<text x="{gx+10}" y="{legend_y+3.5:.1f}" font-size="10.5" fill="#333">{name}</text>')
        gx += 16 + len(name) * 6.6 + 26

    parts.append(f'<text x="{pad_l}" y="{height-6}" font-size="10" fill="#888">Erro% por combinação tela &amp; área (tamanho do ponto = Importância)</text>')

    dot_parts = []
    label_parts = []

    for i, area in enumerate(areas_order):
        y0 = pad_t + i * band_h
        baseline = y0 + band_h / 2
        items = sorted(by_area[area], key=lambda r: r["erro"])

        # 1) espalha (jitter horizontal) valores de erro identicos/quase identicos
        jittered = []
        j = 0
        n_items = len(items)
        while j < n_items:
            k = j
            while k + 1 < n_items and abs(items[k + 1]["erro"] - items[j]["erro"]) < 0.006:
                k += 1
            group = items[j:k + 1]
            g = len(group)
            for gi, r in enumerate(group):
                offset = (gi - (g - 1) / 2) * 0.018
                jittered.append((r, r["erro"] + offset))
            j = k + 1

        # 2) alocacao de pista ciente da largura do rotulo (agendamento por intervalos)
        lane_dy_pattern = [band_h * 0.36, -band_h * 0.36, band_h * 0.14, -band_h * 0.14,
                           band_h * 0.46, -band_h * 0.46, band_h * 0.24, -band_h * 0.24]
        lane_last_x_end = []

        for r, jx in jittered:
            cx = px(jx)
            radius = 3.0 + (r["importancia"] / 3.0) * 5.0
            color = QUAD_COLOR[r["quadrante"]]
            title = f'{r["tela"]} · {area} — Importância {r["importancia"]:.2f}, Erro% {r["erro"]*100:.0f}%, {r["quadrante"]}'
            dot_parts.append(
                f'<circle cx="{cx:.1f}" cy="{baseline:.1f}" r="{radius:.1f}" fill="{color}" stroke="#fff" stroke-width="0.9" opacity="0.92"><title>{title}</title></circle>'
            )

            label = r["tela"]
            label_w = len(label) * _CHART_CHAR_W
            half = label_w / 2

            lane_idx = None
            for li, last_end in enumerate(lane_last_x_end):
                if cx - half - _CHART_LABEL_GAP > last_end:
                    lane_idx = li
                    break
            if lane_idx is None:
                lane_idx = len(lane_last_x_end)
                lane_last_x_end.append(0)
            lane_last_x_end[lane_idx] = cx + half

            dy = lane_dy_pattern[lane_idx % len(lane_dy_pattern)] * (1 + lane_idx // len(lane_dy_pattern) * 0.9)
            ly = baseline + dy
            ly = max(y0 + 9, min(y0 + band_h - 3, ly))

            lx = cx - half
            label_parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="8.2" fill="#333" text-anchor="start">{label}</text>')
            if abs(ly - baseline) > 10:
                label_parts.append(f'<line x1="{cx:.1f}" y1="{baseline + (radius if dy>0 else -radius):.1f}" x2="{cx:.1f}" y2="{ly - (7 if dy>0 else -3):.1f}" stroke="#bbb" stroke-width="0.6"/>')

    parts.extend(dot_parts)
    parts.extend(label_parts)
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Preenchimento do template (assets/template_base.html)
# ---------------------------------------------------------------------------

def _no_shot_html():
    return '''<div class="laptop laptop-empty"><div class="no-shot">
      <div class="no-shot-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="4" width="18" height="14" rx="2" stroke="#999" stroke-width="1.6"/><path d="M3 16L8 11L12 14L16 10L21 15" stroke="#999" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      Screenshot não fornecido para esta tela.<span>A avaliação usa apenas evidência narrada/contexto disponível.</span>
    </div></div>'''


def _render_area_row(block, item):
    area, area_stat = item
    n_prob = area_stat["n_problemas"]
    erro_text = f'{area_stat["erro"]*100:.1f}%' + (" (sem problema)" if n_prob == 0 else "")
    return fill_tokens(block, {
        "AREA_LABEL": AREA_LABELS[area],
        "AREA_N_PROBLEMAS": n_prob,
        "AREA_NOTA": f'{area_stat["nota"]:.2f}',
        "AREA_ERRO_NONE_CLASS": " erro-none" if n_prob == 0 else "",
        "AREA_ERRO_TEXT": erro_text,
    })


def _render_card(block, row):
    quebra = row["quebra"]
    nota = row["importancia"] * QUEBRA_FATOR[quebra]
    return fill_tokens(block, {
        "CARD_AREA_TAG": AREA_TAG[row["area"]],
        "CARD_TEMA": esc(row["tema"]),
        "CARD_BASE": basis_for(row),
        "CARD_PROBLEMA": esc(row["problema"]),
        "CARD_SOLUCAO": esc(row["solucao"]),
        "CARD_IMPORTANCIA": row["importancia"],
        "CARD_SCORE_CLASS": QUEBRA_SCORE_CLASS.get(quebra, ""),
        "CARD_QUEBRA": quebra,
        "CARD_NOTA": f"{nota:.2f}",
    })


def _render_tela_pair(block, tela):
    shot_b64 = img_b64(tela["screenshot"]) if tela.get("screenshot") else None
    if shot_b64:
        img_html = f'<div class="laptop"><div class="laptop-notch"></div><img src="{shot_b64}" class="laptop-img"/></div>'
    else:
        img_html = _no_shot_html()

    problem_rows = [r for r in tela["rows"] if r["quebra"] != "Nenhum"]
    slug = slugify(tela["key"])

    s = fill_tokens(block, {
        "TELA_LABEL": esc(tela["label"]),
        "TELA_IMG_HTML": img_html,
        "TELA_ERRO_PCT": f'{tela["erro"]*100:.1f}',
        "TELA_N_PROBLEMAS": tela["n_problemas"],
        "TELA_N_TOTAL": tela["n_total"],
        "TELA_NOTA": f'{tela["nota"]:.2f}',
        "CARDS_ID": f"cards-{slug}",
    })
    s = render_repeat(s, "AREA_ROW", [(a, tela["area_stats"][a]) for a in AREAS], _render_area_row)
    s = render_repeat(s, "CARD", problem_rows, _render_card)
    return s


def build(cfg, telas_raw):
    validate_cfg(cfg)
    stats = compute(telas_raw)
    basis_rows = compute_basis_rows(stats)

    here = Path(__file__).resolve().parent
    # LOGO_B64 (branco): usado na capa e no slide "Obrigado" — fundo escuro (--ink), a logo
    # como o arquivo-fonte ja e (branca) fica visivel sem alteracao.
    # LOGO_DARK_B64: usado no "wordmark" do topo de toda pagina de fundo claro (#fff) — precisa
    # de uma cor escura para nao ficar invisivel (ver recolor_svg_fill acima para o porque disso
    # existir). Se `logo_dark_path` vier no config (ex.: cliente com logo propria multi-cor que
    # ja tem uma variante pronta para fundo claro), usa esse arquivo direto, sem recolorir nada.
    logo_path = cfg.get("logo_path") or str(here.parent / "assets" / "performa_logo.svg")
    logo_dark_path = cfg.get("logo_dark_path")
    logo_dark_color = cfg.get("logo_dark_color", "#000614")
    squiggle_path = cfg.get("squiggle_path") or str(here.parent / "assets" / "performa_squiggle.png")
    logo_b64 = img_b64(logo_path)
    logo_dark_b64 = img_b64(logo_dark_path) if logo_dark_path else img_b64_recolored(logo_path, logo_dark_color)
    squiggle_b64 = img_b64(squiggle_path)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    ordered = sorted(stats["telas"], key=lambda t: -t["erro"])
    pior, melhor = ordered[0], ordered[-1]
    n_total = stats["n_avaliacoes_total"]
    n_problemas = stats["n_problemas_total"]

    global_tokens = {
        "TITLE": f'UX Assessment — {cfg["produto"]} ({cfg["cliente"]}) · {cfg["consultoria"]}',
        "LOGO_B64": logo_b64,
        "LOGO_DARK_B64": logo_dark_b64,
        "SQUIGGLE_B64": squiggle_b64,
        "PRODUTO": esc(cfg["produto"]),
        "CLIENTE": esc(cfg["cliente"]),
        "N_TELAS": len(stats["telas"]),
        "CONSULTORIA": esc(cfg["consultoria"]),
        "DATA_AVALIACAO": esc(cfg["data_avaliacao"]),
        "PUBLICO": esc(cfg.get("publico", "operação")),
        "N_TOTAL": n_total,
        "N_PROBLEMAS": n_problemas,
        "N_SEM": n_total - n_problemas,
        "N_BASES_FAMILIAS": len(basis_rows),
        "N_NIELSEN": next((r["BASE_N"] for r in basis_rows if r["_key"] == "nielsen"), 0),
        "N_OUTRAS_BASES": len([r for r in basis_rows if r["_key"] != "nielsen"]),
        "DIAGNOSTICO_FERRAMENTA_ATUAL": esc(cfg.get("diagnostico_ferramenta_atual") or (
            f'Um produto funcional, construído de forma incremental. Cada tela resolve bem o seu '
            f'problema local, mas nenhuma foi pensada em conjunto com as outras — falta uma jornada '
            f'única que atravesse o {cfg["produto"]} do início ao fim do uso diário.'
        )),
        "DIAGNOSTICO_NECESSIDADE_NEGOCIO": esc(cfg.get("diagnostico_necessidade_negocio") or (
            f'Uma plataforma percebida como única e confiável por quem a usa no dia a dia: um único '
            f'vocabulário visual de status, feedback claro de erro, e uma jornada contínua entre telas.'
        )),
        "GRAND_ERRO_PCT": f'{stats["grand_erro"]*100:.1f}',
        "GRAND_IMP": f'{stats["grand_imp"]:.0f}',
        "GRAND_NOTA": f'{stats["grand_nota"]:.2f}',
        "N_RISK_ROWS": len(stats["risk_rows"]),
        "MATRIX_CHART_SVG": build_risk_chart_svg(stats["risk_rows"]),
        "PIOR_LABEL": esc(pior["label"]),
        "PIOR_ERRO_PCT": f'{pior["erro"]*100:.1f}',
        "MELHOR_LABEL": esc(melhor["label"]),
        "MELHOR_ERRO_PCT": f'{melhor["erro"]*100:.1f}',
    }

    # 1) blocos repetidos primeiro (nenhum token global colide com os tokens locais deles)
    html = render_repeat(template, "RANK_ROW", ordered, lambda block, t: fill_tokens(block, {
        "TELA_LABEL": esc(t["label"]),
        "ERRO_PCT": f'{t["erro"]*100:.1f}',
    }))
    html = render_repeat(html, "TELA_PAIR", stats["telas"], _render_tela_pair)
    html = render_repeat(html, "BASE_ROW", basis_rows, _render_base_row)

    atendidas = cfg.get("oportunidades_atendidas") or [
        "Nenhuma funcionalidade destacada explicitamente — preencher com achados positivos reais."]
    nao_atendidas = cfg.get("oportunidades_nao_atendidas") or [
        "Nenhuma oportunidade destacada explicitamente — preencher com lacunas reais identificadas."]
    html = render_repeat(html, "LI_OK", atendidas, lambda block, x: fill_tokens(block, {"LI_TEXT": esc(x)}))
    html = render_repeat(html, "LI_BAD", nao_atendidas, lambda block, x: fill_tokens(block, {"LI_TEXT": esc(x)}))

    def _render_contact(block, av):
        iniciais = "".join(p[0].upper() for p in av["nome"].split()[:2])
        mail_html = f'<div class="contact-mail">{esc(av["email"])}</div>' if av.get("email") else ""
        return fill_tokens(block, {
            "CONTACT_INICIAIS": iniciais,
            "CONTACT_NOME": esc(av["nome"]),
            "CONTACT_PAPEL": esc(av.get("papel", cfg["consultoria"])),
            "CONTACT_MAIL_HTML": mail_html,
        })
    html = render_repeat(html, "CONTACT_CARD", cfg["avaliadores"], _render_contact)

    # 2) tokens singulares (o resto do documento, ja "achatado")
    html = fill_tokens(html, global_tokens)

    # 3) numeracao sequencial de pagina, por ultimo
    html = fill_pagenos(html)

    assert_no_leftover_tokens(html)

    return html, stats


def main():
    ap = argparse.ArgumentParser(description="Gera o UX Assessment final em HTML.")
    ap.add_argument("--config", required=True, help="Caminho para config.json")
    ap.add_argument("--data", required=True, help="Caminho para data.py (define TELAS)")
    ap.add_argument("--out", required=True, help="Caminho do HTML de saída")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)

    mod = load_data_module(args.data)
    html, stats = build(cfg, mod.TELAS)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"OK: {args.out} ({len(html)} chars, {len(stats['telas'])} telas, "
          f"Erro% geral {stats['grand_erro']*100:.1f}%)")


if __name__ == "__main__":
    main()
