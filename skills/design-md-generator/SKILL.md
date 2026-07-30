---
name: design-md-generator
description: "Gera um DESIGN.md pronto para uso por agentes de código (Claude Code, Cursor, v0, Stitch) a partir de insumos reais de projeto: brand book, site, design system em JSON/CSS/tokens, transcrições de reunião, referências visuais. Executa em 3 fases: (1) extração automática dos insumos, (2) geração de documento pré-preenchido para revisão humana, (3) geração do DESIGN.md final após confirmação. Dispara quando o usuário pedir para 'gerar o design.md', 'criar o design.md do projeto', 'montar o md de design', ou entregar insumos de design (brand book, tokens, site de referência)."
---

# DESIGN.md GENERATOR

## MISSÃO

Transformar insumos reais de projeto (brand book, site, design system, reunião, referências) em um DESIGN.md pronto para ser lido por agentes de código.

O DESIGN.md **documenta intenção e rationale de decisões já tomadas**. Ele não define o Design System, não toma decisões de design em nome do time, e não prescreve arquitetura de tokens. Quem define tokens, escala de cores e hierarquia semântica é o DS — o MD documenta *por que* essas decisões existem e como o agente deve aplicá-las.

**Base de referência:** a estrutura desta skill é inspirada em práticas abertas de documentação de design tokens para agentes de código — no espírito do formato `design.md` popularizado por ferramentas de design-to-code. Usamos essa convenção como estrutura base — o formato de duas camadas (YAML front matter + markdown body), a ordem das seções e a sintaxe de referência cruzada `{path.to.token}` seguem esse padrão.

**Flexibilidade de consultoria:** a Performa_IT atua em projetos de naturezas muito distintas — produtos com DS maduro, projetos greenfield sem DS definido, clientes com brand books rigorosos, e projetos sem nenhum insumo visual formalizado. A skill não impõe uma estrutura única. Ela se adapta ao que o projeto tem: se o DS define tokens semânticos, o MD os documenta; se não há DS, o MD pode estabelecer as decisões com revisão do designer; se o projeto é simples, seções inteiras podem ser omitidas. O que nunca muda é o princípio: o MD documenta intenção, não substitui o DS nem toma decisões de design pela equipe.

O processo é colaborativo em 3 fases: extração → revisão → geração. A skill executa as fases 1 e 2 automaticamente; a fase 3 aguarda confirmação humana.

**Relação com o DESIGN.md da FASE 2 do Dojo Framework:** o `DESIGN.md` gerado por esta skill é exatamente o mesmo artefato citado em `assets/FASE 2 - DISCOVERY.md` (ETAPA 4, "Prototipação das Jornadas") e estruturado em `templates/tpl-design.md` — não são dois documentos diferentes. A prosa da FASE 2 descreve o DESIGN.md a partir da perspectiva de cada jornada prototipada (por isso fala em "o designer produz o DESIGN.md correspondente" ao concluir a prototipação de uma jornada); na prática, o DESIGN.md captura o Design System do projeto como um todo — os tokens e o racional por trás deles — e costuma ser criado uma única vez (a partir do "DESIGN SYSTEM inicial" da Etapa 2) e depois atualizado incrementalmente à medida que novas jornadas são prototipadas, em vez de regenerado do zero a cada jornada. Cada jornada referencia esse DESIGN.md único e evolutivo — por exemplo, na tabela "Componentes do Design System utilizados" do `templates/tpl-design.md` daquela jornada — em vez de duplicar seu conteúdo.

---

## PRINCÍPIO CENTRAL

> O DESIGN.md é o ativo mais importante para evitar slop porque documenta **intenção**, não padrão. Um agente que lê tokens sem rationale pode aplicá-los tecnicamente correto e visualmente errado. Um agente que lê o rationale sabe quando não há uma regra explícita e consegue tomar a decisão certa por analogia.

Consequências práticas desse princípio:

- **A skill não prescreve naming de tokens.** Os nomes de token usados no YAML front matter devem espelhar os nomes que o DS do projeto já usa — sejam eles `primary`, `brand-yellow`, `color-interactive-01` ou qualquer outra convenção. Impor uma nomenclatura externa (ex: `primary/secondary/tertiary` do Material 3) seria sobrescrever uma decisão que pertence ao DS.
- **A skill não separa primitivo de semântico.** Essa é uma decisão arquitetural do DS. O MD referencia os tokens como o DS os nomeia.
- **A skill não define valores que o DS já definiu.** Se o DS tem `--color-action: #5B8DEF`, o MD documenta o papel e a intenção desse token — não redefine ou renomeia.
- **A skill pode estabelecer o que o DS não definiu** — mas isso deve ser documentado explicitamente como uma decisão tomada no MD, não como preenchimento automático da IA.

---

## SPEC DE REFERÊNCIA — DESIGN.md

Um DESIGN.md válido tem duas camadas em um único arquivo:

**YAML front matter** — tokens machine-readable (valores normativos):
```yaml
---
version: alpha
name: <string>
description: <string>          # opcional
colors:
  <token-name>: "<hex>"
typography:
  <token-name>:
    fontFamily: <string>
    fontSize: <Dimension>      # px, em, rem
    fontWeight: <number>       # numérico: 400, 600, 700 — não string
    lineHeight: <Dimension | number>  # unitless recomendado: 1.5
    letterSpacing: <Dimension> # opcional
rounded:
  <scale-level>: <Dimension>   # ex: sm: 4px / md: 8px / full: 9999px
spacing:
  <scale-level>: <Dimension | number>  # number = razão ou contagem de colunas
components:                    # opcional — apenas se DS define tokens de componente
  <component-name>:
    backgroundColor: <Color | {path.to.token}>
    textColor: <Color | {path.to.token}>
    typography: <{path.to.token}>
    rounded: <Dimension | {path.to.token}>
    padding: <Dimension>
    size: <Dimension>
    height: <Dimension>
    width: <Dimension>
  <component-name>-hover:      # variantes de estado como chaves separadas
    backgroundColor: <Color | {path.to.token}>
---
```

> `fontWeight` é número, não string. `400` e `"400"` são equivalentes em YAML — ambos válidos — mas a instrução ao agente deve ser sempre numérica para evitar ambiguidade de tipo.

**Markdown body** — rationale human-readable (8 seções, nessa ordem):

| # | Seção | O que contém |
|---|---|---|
| 1 | `## Overview` | Personalidade, público, resposta emocional desejada. Contexto fundacional usado pelo agente como fallback quando não há token ou regra explícita |
| 2 | `## Colors` | Paleta com papel e contexto de uso de cada cor conforme definido pelo DS |
| 3 | `## Typography` | Hierarquia tipográfica com justificativa de cada nível |
| 4 | `## Layout` | Grid, espaçamento, breakpoints, densidade |
| 5 | `## Elevation & Depth` | Sombras, profundidade, ou estratégia alternativa em design flat |
| 6 | `## Shapes` | Linguagem de formas e border-radius por tipo de elemento |
| 7 | `## Components` | Componentes-chave com tokens mapeados (omitir se DS não define tokens de componente) |
| 8 | `## Do's and Don'ts` | Guardrails explícitos — o que sempre fazer e o que nunca fazer |
| 9 | `## Agent Prompt Guide` | Seção opcional. Exemplos de prompts de componente e guia de iteração para o agente |

> Seções podem ser omitidas, mas as presentes devem seguir essa ordem.

---

## ALGORITMO APCA — IMPLEMENTAÇÃO INTERNA

Quando a skill precisa calcular ou validar contraste, usa o algoritmo APCA 0.0.98G-W3 (versão licenciada para uso com guidelines W3/AGWG). A implementação abaixo é executada internamente pela skill sempre que um par texto/fundo precisar ser avaliado.

### Constantes (APCA 0.0.98G-W3, sRGB)

```
# Expoentes de codificação perceptual
mainTRC = 2.4      # gamma da tela sRGB
normBG  = 0.56     # fundo claro (texto escuro sobre fundo claro)
normTXT = 0.57     # texto escuro sobre fundo claro
revTXT  = 0.62     # texto claro sobre fundo escuro
revBG   = 0.65     # fundo escuro (texto claro sobre fundo escuro)

# Coeficientes de luminância sRGB
sRco = 0.2126729
sGco = 0.7151522
sBco = 0.0721750

# Clamps para preto perceptual
blkThrs = 0.022    # limiar abaixo do qual aplicar compensação de preto
blkClmp = 1.414    # expoente da compensação

# Clamps de saída
loClip    = 0.1    # valores Lc abaixo deste são zerados (ruído)
deltaYmin = 0.0005 # diferença mínima de luminância para calcular

# Escaladores
scaleBoW    = 1.14   # escala texto escuro sobre fundo claro (Black on White)
loBoWoffset = 0.027  # offset de baixo contraste BoW
scaleWoB    = 1.14   # escala texto claro sobre fundo escuro (White on Black)
loWoBoffset = 0.027  # offset de baixo contraste WoB
```

### Passos do cálculo

**Passo 1 — Converter hex para sRGB linear (Y)**

Para cada canal R, G, B do hex:
```
canal_normalizado = valor_decimal / 255
canal_linear = canal_normalizado ^ mainTRC   # ^ = exponenciação
```

Calcular luminância Y:
```
Y = sRco * R_linear + sGco * G_linear + sBco * B_linear
```

Aplicar compensação de preto perceptual (soft clamp):
```
se Y < blkThrs:
    Y = Y + (blkThrs - Y) ^ blkClmp
```

**Passo 2 — Determinar polaridade e calcular Sapc**

```
se Y_fundo > Y_texto:   # texto escuro sobre fundo claro (BoW)
    Sapc = (Y_fundo ^ normBG - Y_texto ^ normTXT) * scaleBoW

se Y_fundo < Y_texto:   # texto claro sobre fundo escuro (WoB)
    Sapc = (Y_fundo ^ revBG - Y_texto ^ revTXT) * scaleWoB
```

**Passo 3 — Aplicar clamps de baixo contraste e offset**

```
se abs(Sapc) < loClip:
    Lc = 0   # contraste muito baixo — zerado

se Sapc > 0:   # BoW
    Lc = (Sapc - loBoWoffset) * 100

se Sapc < 0:   # WoB
    Lc = (Sapc + loWoBoffset) * 100
```

O valor final é **Lc** — positivo para texto escuro/fundo claro, negativo para texto claro/fundo escuro. Para validação, usar o valor absoluto.

### Limiares de referência APCA

| Uso | Lc mínimo | Equivalente aproximado WCAG 2.x |
|---|---|---|
| Texto corpo ≥16px, peso 400 | 75 | ~7:1 |
| Label/botão ≥14px, peso 600 | 60 | ~4.5:1 |
| Heading ≥24px, peso 700 | 45 | ~3:1 |
| Texto decorativo / placeholder | 30 | — |
| Ícone sem texto alternativo | 45 | ~3:1 |

> Lc 90 é considerado "preferido" para leitura sustentada (corpo de texto longo).
> Lc 75 é o mínimo prático para leitura confortável.
> Lc 60 é adequado para elementos curtos e bold (labels, botões, headings grandes).

### Quando a skill executa o cálculo

A skill calcula Lc automaticamente nas seguintes situações:

1. **Fase 1** — ao extrair pares de cor do DS ou do site de referência, se conseguir identificar texto e fundo de um mesmo elemento
2. **Fase 2** — ao preencher a seção de contraste no draft, para cada par identificado
3. **Fase 3** — na verificação interna de lint, para validar todos os pares de componente que têm `textColor` e `backgroundColor` definidos no YAML

Para cada par calculado, reportar:
```
Par: [token-texto] sobre [token-fundo]
Hex: #XXXXXX sobre #YYYYYY
Lc calculado: XX.X
Limiar aplicável: XX (com base no tamanho/peso do nível tipográfico)
Status: PASSA / FALHA / INDEFINIDO (sem nível tipográfico associado)
```

Se o DS não definiu contraste e a skill identifica pares que falham no limiar → sinalizar no draft como `[DECISÃO-NECESSÁRIA]` com o Lc calculado, o limiar esperado e as opções de ajuste. Nunca ajustar a cor automaticamente.

---

## SOBRE CONTRASTE: APCA, NÃO WCAG 2.x

**Por que APCA e não WCAG 2.x:**

O WCAG 2.x usa uma fórmula de razão de contraste (ex: 4.5:1 para texto normal) derivada de pesquisas dos anos 80 sobre legibilidade em monitores CRT de baixa resolução. Essa fórmula trata luminância de forma linear e não modela como o sistema visual humano percebe contraste em contextos modernos — telas de alta densidade, fundos coloridos saturados, texto pequeno em peso leve.

O resultado prático é que o WCAG 2.x aprova combinações que são ilegíveis na prática (ex: amarelo escuro sobre branco passa no ratio mas é difícil de ler) e reprova combinações que funcionam bem visualmente (ex: azul saturado sobre preto).

O **APCA (Accessible Perceptual Contrast Algorithm)**, desenvolvido por Andrew Somers e proposto para o WCAG 3.0, modela o contraste em função de: peso da fonte, tamanho do texto, polaridade (texto claro/escuro sobre fundo claro/escuro) e resposta perceptual não-linear do olho humano. Ele produz um valor Lc (Lightness Contrast) em escala de 0–106, com limiares diferentes para cada combinação de tamanho e peso — o que é muito mais próximo da experiência real de leitura.

**Regra para a skill:**

- Se o DS já definiu combinações de contraste validadas → o MD documenta essa decisão e referencia o Lc mínimo adotado.
- Se o DS **não** definiu → o MD **pode e deve** estabelecer os limiares de contraste como decisão de design documentada. Nesse caso, a skill propõe os valores APCA e o designer os confirma ou ajusta antes da Fase 3.
- A IA **não escolhe** combinações de cor por conta própria para satisfazer contraste — ela sinaliza lacunas e aguarda decisão humana.

Referência: [https://www.myndex.com/APCA/](https://www.myndex.com/APCA/)

---

## TIPOS DE INSUMO E COMO PROCESSAR CADA UM

### Design system em arquivo (.json, .css, tokens, Tailwind config) — processar primeiro

É o insumo de maior confiança: contém os valores exatos que o DS já decidiu.

**.json / tokens DTCG:**
- Ler todas as chaves de cor, tipografia, espaçamento, radius e sombra
- Preservar os nomes de token exatamente como definidos no DS — não renomear
- Identificar se o DS separa primitivos de semânticos e documentar essa estrutura como está
- Anotar tokens sem papel semântico declarado como `[PENDENTE-INTENCIONALIDADE]` — não como erro

**.css / SCSS com custom properties:**
- Ler variáveis `--color-*`, `--font-*`, `--spacing-*`, `--radius-*`
- Preservar os nomes como estão

**Tailwind config:**
- Ler `theme.extend.*` — cores, fontes, espaçamento, radius

**Atenção:** a skill não recomenda renomear tokens do DS para se conformar ao spec de referência. O spec aceita qualquer nome válido em YAML. A consistência com o DS é mais importante que a conformidade com nomenclatura de exemplo.

---

### Brand book / manual de identidade (PDF, imagem, documento)

Extrair intenção, não apenas valores:
- Nome da marca e descrição de posicionamento
- Paleta com os nomes que a própria marca usa (ex: "Azul Vero", "Verde Aura") — esses nomes vão para a prosa do MD
- Tipografia institucional: fontes, pesos, hierarquia e o **motivo declarado** de cada escolha quando disponível
- Linguagem de formas: arredondamentos, geometria e o que ela comunica
- Tom e personalidade: adjetivos usados pelo próprio brand book
- Restrições explícitas (o que o brand book proíbe)

---

### Site de referência (URL)

Fazer `web_fetch` na URL. Extrair evidência real do produto em produção:
- Cores dominantes (`background-color`, `color`, `border-color` dos elementos principais)
- Família tipográfica (`font-family` em body, headings, labels)
- Pesos e tamanhos mais frequentes
- Valores de `border-radius` em botões, cards, inputs
- Escala de `padding`, `margin`, `gap` — inferir grid base
- Presença de `box-shadow` e valores
- Breakpoints em `@media` queries

> Se a URL for um DS documentado (Material, Ant, shadcn, etc.), extrair os tokens publicados na documentação.

---

### Transcrição de reunião (txt, md)

Extrair apenas decisões de design com intenção declarada:
- Restrições explícitas ("não usar emoji", "só ícones outline", "nunca fundo escuro")
- Preferências de comportamento ("animações sutis", "feedback visual imediato")
- Referências de produtos admirados com o motivo ("quero algo como o Vintra porque é denso sem parecer pesado")
- Alertas de contexto de uso ("usuários em campo com luvas", "muita exposição solar")
- Decisões sobre densidade com justificativa
- Qualquer menção a cor, fonte ou componente com decisão tomada

Ignorar: discussões de processo, estimativas, backlog, stakeholders.

---

### Referências visuais (imagens, links)

Extrair adjetivos de intenção, não valores:
- Vibe inferível (clean, denso, bold, sutil, editorial, técnico)
- Padrões de cor predominantes como referência de atmosfera
- Estilo tipográfico (serifado vs. sans, display vs. neutro)
- Linguagem de formas (flat, sombreado, arredondado, angular)

---

## FLUXO DE EXECUÇÃO

```
FASE 1 — EXTRAÇÃO
Processar cada insumo na ordem definida abaixo
Classificar cada dado extraído
    ↓
FASE 2 — DOCUMENTO PRÉ-PREENCHIDO
Gerar design-md-draft.md com tudo extraído
Overview gerado como rascunho autoral [RASCUNHO-DESIGNER]
Aguardar revisão humana
    ↓
FASE 3 — DESIGN.md FINAL
Incorporar revisões → gerar DESIGN.md
Verificar lint internamente antes de entregar
```

---

## FASE 1 — EXTRAÇÃO AUTOMÁTICA

### Ordem de processamento dos insumos

1. Design system em arquivo (valores exatos — maior confiança)
2. Brand book / manual de identidade (intenção declarada)
3. Site de referência via `web_fetch` (evidência em produção)
4. Transcrição de reunião (decisões verbalizadas)
5. Referências visuais (atmosfera e vibe)

### Classificação de cada dado extraído

| Classificação | Quando usar |
|---|---|
| `[EXTRAÍDO]` | Valor direto de um insumo, sem ambiguidade |
| `[INFERIDO]` | Valor deduzido por padrão ou frequência — documentar a lógica |
| `[CONFLITO]` | Valor presente em mais de um insumo com divergência — registrar ambos e a fonte |
| `[PENDENTE]` | Informação não encontrada — campo para o designer preencher |
| `[PENDENTE-INTENCIONALIDADE]` | Valor existe no DS mas sem papel semântico ou rationale declarado — designer deve documentar a intenção |
| `[RASCUNHO-DESIGNER]` | Texto gerado pela IA como pré-rascunho autoral — **obrigatoriamente revisado pelo designer antes da Fase 3** |

---

## FASE 2 — DOCUMENTO PRÉ-PREENCHIDO

Gerar o arquivo `design-md-draft.md` usando a estrutura definida em [`../../templates/tpl-design-draft.md`](../../templates/tpl-design-draft.md).
Preencher com o que foi extraído na Fase 1. O designer revisa, corrige erros, preenche os `[PENDENTE]` e valida os `[RASCUNHO-DESIGNER]`.

> O template cobre: Identidade do projeto, Overview, Cores (com contraste APCA), Tipografia, Layout, Elevation & Depth, Shapes, Componentes-chave e Do's and Don'ts — cada campo já marcado com a classificação da Fase 1 (`[EXTRAÍDO]`, `[INFERIDO]`, `[CONFLITO]`, `[PENDENTE]`, `[PENDENTE-INTENCIONALIDADE]`, `[RASCUNHO-DESIGNER]`). Usar o template como fonte única da verdade para o formato do rascunho — não reescrever essa estrutura aqui.

---

## FASE 3 — GERAÇÃO DO DESIGN.md FINAL

Executar somente após receber o draft revisado e confirmado pelo designer.

Gerar o arquivo final usando a estrutura definida em [`../../templates/tpl-design.md`](../../templates/tpl-design.md) — front matter YAML de tokens + corpo em 9 seções (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts, Agent Prompt Guide).

### Regras de geração

**YAML front matter:**
- Incluir apenas tokens com valor confirmado no draft
- Não inventar valores para `[PENDENTE]` não respondidos — omitir a chave
- Preservar os nomes de token exatamente como definidos pelo DS do projeto
- `fontWeight` sempre como número (ex: `600`, não `"600"`)
- `spacing` pode usar `Dimension` ou `number` unitless (ex: `grid-columns: 5`)
- Referências cruzadas com sintaxe `{path.to.token}` (ex: `{colors.brand-action}`)
- Variantes de componente como chaves separadas: `button-primary`, `button-primary-hover`, `button-primary-disabled`
- Propriedades válidas de componente: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`

**Markdown body:**
- `## Overview`: texto autoral validado pelo designer — não alterar sem revisão. Deve funcionar como fallback de decisão do agente quando não há token explícito
- `## Colors`: uma linha por token com papel semântico e contexto de uso declarado pelo DS. Incluir a decisão de contraste APCA (limiares Lc) — se definida pelo DS, documentar; se definida no MD, sinalizar claramente como decisão estabelecida aqui
- `## Typography`: por nível do DS com justificativa de uso — não apenas os valores
- `## Layout`: grid, escala de espaçamento, estratégia responsiva e densidade com contexto de uso
- `## Elevation & Depth`: estratégia (sombra / flat / tonal) com justificativa
- `## Shapes`: linguagem de formas com o que ela comunica, depois os valores por elemento
- `## Components`: apenas se DS define tokens de componente — com variantes de estado
- `## Do's and Don'ts`: formato de tabela `| Do | Don't |` — mínimo 4 linhas cada coluna. Incluir obrigatoriamente: decisão de contraste APCA, uso de emoji, biblioteca de ícones
- `## Agent Prompt Guide`: incluir se preenchido no draft

**Qualidade obrigatória:**
- Nenhuma seção com afirmação vaga ("usar boas cores", "manter consistência") — toda afirmação deve ser acionável pelo agente
- Nenhum token com valor `null` ou `TBD` no YAML
- O Overview deve ser específico o suficiente para guiar uma decisão de estilo não coberta por token

### Verificação interna antes de entregar (simulação de lint)

Antes de gerar o arquivo final, verificar internamente:

1. Todos os `{path.to.token}` apontam para chaves que existem no YAML?
2. Todos os valores de `fontWeight` são numéricos?
3. Todos os valores de `colors` começam com `#`?
4. A seção `## Do's and Don'ts` contém a decisão de contraste APCA?
5. Algum campo `[PENDENTE]` ou `[RASCUNHO-DESIGNER]` não validado ainda está no draft?

Se qualquer verificação falhar → reportar ao designer antes de gerar o arquivo.

### Nome do arquivo de saída

```
DESIGN.md
```

Salvar na raiz do repositório de código (onde os agentes de FASE 4 o leem
diretamente durante a implementação) **e** manter uma cópia versionada no
vault, em `02_discovery/design-system/DESIGN.md`, usando `templates/tpl-design.md`
como estrutura — essa cópia do vault é a fonte rastreável/de governança
(histórico de versão, link a partir do `CONTEXT.md`); a cópia no repositório
de código é a operacional, consumida em tempo real pelos agentes. Manter as
duas sincronizadas; a do vault é a autoritativa em caso de divergência.

O campo `name` no YAML deve corresponder ao nome do projeto conforme definido no draft.

---

## REPORTAR AO FINAL DE CADA FASE

**Fase 1:**
- Insumos processados e tipo de cada um
- O que foi `[EXTRAÍDO]` com alta confiança
- O que foi `[INFERIDO]` e a lógica usada
- Campos `[PENDENTE]` e `[PENDENTE-INTENCIONALIDADE]` — listar e explicar por quê
- Conflitos detectados entre insumos

**Fase 2:**
- Confirmar geração do `design-md-draft.md`
- Listar `[PENDENTE]` obrigatórios para gerar o DESIGN.md
- Listar `[PENDENTE]` opcionais
- Destacar todos os `[RASCUNHO-DESIGNER]` que precisam de validação humana antes da Fase 3

**Fase 3:**
- Confirmar geração do `DESIGN.md`
- Listar seções geradas e seções omitidas com motivo
- Resultado da verificação interna de lint (itens 1–5 acima)
- Sugerir próximo passo: `node .claude/skills/design-md-generator/scripts/validate-design-md.js DESIGN.md --verbose`
  > O validador incluso na skill (`scripts/validate-design-md.js`) existe porque validadores genéricos desse formato tendem a impor convenções externas de naming de tokens e usar WCAG 2.x para contraste — ambos incompatíveis com a filosofia desta skill. O validador próprio verifica forma sem impor convenção e usa APCA para contraste.
