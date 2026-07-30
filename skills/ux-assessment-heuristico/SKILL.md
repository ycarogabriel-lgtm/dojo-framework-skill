---
name: ux-assessment-heuristico
description: Conduz uma avaliação heurística de UX completa (método Performa.it) de qualquer produto digital, a partir de screenshots reais e, opcionalmente, vídeos de walkthrough e fluxos do Figma. Produz um documento de revisão em Markdown (gate de aprovação, com prints, contraste APCA e a lógica de cada nota), uma planilha XLSX editável (matriz heurística por tela e área, com fórmulas) e um UX Assessment final em HTML no padrão visual da Performa.it (achados citando suas bases teóricas -- Nielsen, ISO 9241-110, WCAG/APCA, Morville, Miller/Hick --, semáforo de 2 cores sem verde, Erro% = Importância x Quebra). Use sempre que o pedido for avaliar usabilidade, fazer um "UX assessment", uma auditoria ou matriz heurística, medir contraste de interface, ou revisar a experiência de um sistema/CRM/app a partir de prints -- mesmo sem esses termos exatos, como em "dá uma olhada nesse sistema e me diz o que está ruim" com capturas de tela anexadas.
---

# UX Assessment Heurístico (método Performa.it)

## Regra inegociável: evidência real, sempre

Todo achado citado nos 3 entregáveis desta skill precisa estar ancorado em algo que você
realmente observou: um screenshot fornecido, um frame de vídeo, uma frase transcrita de um
narrador, ou uma medição real de contraste. Nunca invente um problema de usabilidade "genérico"
que soaria plausível para o tipo de tela. Se você não tem evidência para uma das 5 áreas em uma
tela, é legítimo que essa área tenha poucos ou nenhum achado com quebra — isso é um resultado
válido, não uma lacuna a preencher com suposição.

Da mesma forma, nunca estime contraste "de olho". Toda métrica de contraste citada num achado de
Design/Cores precisa vir de uma medição real via APCA (ver `references/apca_contraste.md` e
`scripts/apca/`), não de um julgamento visual do tipo "parece baixo contraste".

## Os 3 entregáveis, na ordem certa

Esta skill nunca pula direto para o HTML final. A sequência existe para dar à pessoa um ponto de
aprovação humana antes de qualquer trabalho de formatação final:

1. **Documento de revisão em Markdown** (`revisao_<cliente>.md`) — o gate. Lista, tela por tela,
   cada screenshot (linkado por caminho relativo, para poder ser aberto junto do .md em qualquer
   editor/preview), o problema identificado, a métrica de contraste medida quando aplicável, os
   achados narrados extraídos dos vídeos (se houver), a pontuação (Importância, Quebra, Nota) e a
   **lógica por trás de cada nota** — por que aquela Importância, por que aquele fator de Quebra.
   É um Markdown puro (nenhuma dependência de biblioteca de imagem embutida), editável em
   qualquer editor de texto. A pessoa revisa e aprova (ou pede ajustes) antes da Etapa 4.
2. **Planilha XLSX editável** (`matriz_<cliente>.xlsx`) — a matriz heurística completa, com
   todas as 15 avaliações por tela (incluindo as marcadas "Nenhum", que não entram no HTML mas
   ficam registradas aqui), fórmulas de Erro% e validações de dropdown para Quebra. É o
   documento de trabalho vivo — quem revisa pode editar uma nota ali e as fórmulas recalculam.
3. **UX Assessment final em HTML** (`UX Assessment - <cliente>.html`) — o entregável do cliente,
   no padrão visual fixo da Performa.it. Só é gerado depois que a Etapa 3 (documento de revisão)
   foi aprovada.

## Estado atual da implementação

`scripts/gen_html.py` e `scripts/data_exemplo.py` existem e são o motor real e testado do
entregável final (Etapa 4, item 3). Os demais scripts citados neste documento —
`gen_review_md.py` (Etapa 3), `build_xlsx.py` e `scripts/office/recalc.py` (Etapa 4, item 2),
`scripts/validate_html.py` e `scripts/apca/sample_and_measure.py` — descrevem o fluxo **desejado**
da skill, mas ainda não foram implementados neste pacote. Ao chegar numa fase que dependa de um
desses scripts, trate o comando como especificação do que precisa existir, não como algo para
rodar direto — implemente o script (ou o passo equivalente manualmente) antes de prosseguir, e
sinalize esse gap para quem está usando a skill em vez de pular a etapa silenciosamente.

## Fluxo completo

### Etapa 1 — Intake

Reúna:
- **Screenshots das telas avaliadas** (obrigatório — pelo menos 1 por tela). Peça se não vierem
  anexados; sem eles não há avaliação heurística real, só suposição.
- **Até 3 vídeos, todos opcionais**: (a) alguém narrando o fluxo E os problemas de uso juntos,
  (b) alguém explicando o que cada tela/funcionalidade faz (contexto, não achado), (c) alguém
  narrando problemas de usabilidade tela por tela especificamente. Transcreva os trechos
  relevantes e cite-os como evidência narrada nos achados que eles sustentam.
- **Fluxo de telas do Figma**, opcional — usado para entender navegação entre telas (de onde
  vem, para onde vai), não como fonte de achados por si só.

Se só vierem screenshots (o mínimo), prossiga normalmente — vídeos e Figma enriquecem o achado,
não são pré-requisito.

### Etapa 2 — Análise

Para cada tela, avalie as 5 áreas fixas do método (Conteúdo, Arquitetura da Informação, Design,
Tecnologia, Negócios), com 3 critérios por área (15 avaliações por tela) — "critério" é o termo
correto para o conjunto; "heurística", no sentido estrito, descreve só o método de Nielsen (ver
`references/bases_teoricas.md`, seção "Precisão terminológica"). Ver
`references/metodo_pontuacao.md` para a escala completa e `references/bases_teoricas.md` para as
fontes teóricas citáveis por tipo de achado. Meça contraste real via
`scripts/apca/sample_and_measure.py` sempre que um achado envolver legibilidade/cor
(`references/apca_contraste.md`). Ao final, cada avaliação tem: Importância (0-3), Quebra
(Nenhum/Ruído/Obstáculo/Obstrução/Barreira) e a lógica de por que essa nota — isso vai direto
para o documento de revisão da Etapa 3.

### Etapa 3 — Documento de revisão (gate humano)

Gere o documento de revisão:

```
python scripts/gen_review_md.py --config config.json --data data.py --out revisao_<cliente>.md
```

`config.json` e `data.py` seguem o schema documentado abaixo (seção Parametrização) e em
`scripts/config_exemplo.json` / `scripts/data_exemplo.py`. Apresente este .md para a pessoa
revisar. **Não prossiga para a Etapa 4 sem aprovação explícita.** Se vierem ajustes, edite
`data.py` (ou os campos de `config.json`) e regenere o .md até aprovar.

### Etapa 4 — Humanização e finalização

Só depois da aprovação:

1. Rode a camada humanizadora (`revisor-narrativa-executiva`, se disponível como skill) sobre
   todo texto narrativo em português que vai para o HTML/XLSX final — travessão, cacofonia,
   tiques de IA, legibilidade. Esta é uma **dependência opcional**: `revisor-narrativa-executiva`
   não faz parte deste pacote de skills. Se ela não existir no ambiente/pacote em uso, aplique
   manualmente os princípios descritos em `references/humanizacao.md` antes de prosseguir — nunca
   pule este passo silenciosamente só porque a skill dedicada não está disponível.
2. Gere a planilha:
   ```
   python scripts/build_xlsx.py --config config.json --data data.py --out matriz_<cliente>.xlsx
   python scripts/office/recalc.py matriz_<cliente>.xlsx   # da skill xlsx — 0 erros obrigatório
   ```
3. Gere o HTML final:
   ```
   python scripts/gen_html.py --config config.json --data data.py --out "UX Assessment - <cliente>.html"
   python scripts/validate_html.py "UX Assessment - <cliente>.html"   # 0 erros estruturais obrigatório
   ```
4. Se Playwright com Chromium estiver disponível no ambiente, tire um screenshot de 2-3 slides
   representativos do HTML para conferência visual final. **Isso é um bônus, não um bloqueio**:
   ambientes sandbox às vezes não têm as bibliotecas de sistema necessárias para o Chromium
   (ex.: `libXdamage.so.1` ausente e sem acesso root para instalar) — nesse caso, confie na
   validação estrutural (`validate_html.py`) e na conferência numérica cruzada entre HTML e XLSX
   (o Erro% de cada tela deve bater exatamente nos dois documentos) como garantia de qualidade.
5. Cruze os números: o Erro% por tela e por área deve ser idêntico entre o XLSX e o HTML (ambos
   importam a mesma lógica de `gen_html.py`, então uma divergência aponta um bug real).

## Parametrização

`config.json` precisa de, no mínimo:
- `cliente`: nome do cliente (ex. "Vetta Operações")
- `produto`: nome do produto avaliado (ex. "Painel Zeta")
- `consultoria`: nome de quem assina (default "Performa.it")
- `avaliadores`: lista de `{nome, papel, email}` para o slide de encerramento
- `data_avaliacao`: data da avaliação, para o rodapé/contexto

Opcional, para trocar a marca (ex. numa versão com a identidade do próprio cliente em vez da
Performa.it):
- `logo_path`: caminho para um SVG ou PNG a usar na capa e no slide de encerramento (fundo
  escuro). Default: `assets/performa_logo.svg`.
- `logo_dark_path`: caminho para uma variante **já pronta** do logo para fundo claro (o wordmark
  de topo de cada página interna). Use isto quando o logo do cliente já for multicolor ou já
  tiver uma variante própria para fundo claro — nesse caso nada é recolorido.
- `logo_dark_color`: cor hex para recolorir automaticamente `logo_path` quando `logo_dark_path`
  **não** for informado (default `#000614`, o `--ink` da Performa.it). Só funciona para SVGs
  monocromáticos com `fill="white"`/`#fff`/`#ffffff` (ver `recolor_svg_fill()` em `gen_html.py`) —
  um PNG raster não pode ser recolorido, então um cliente com logo só em PNG precisa fornecer
  `logo_dark_path` explicitamente.

Nunca reuse o mesmo arquivo de logo nos dois contextos sem checar a cor de fundo: um logo
monocromático branco fica invisível num wordmark de fundo `#fff` se esse passo for esquecido —
um erro fácil de cometer e fácil de evitar checando o contraste antes de considerar a entrega
pronta.

`data.py` define `TELAS`: uma lista de dicts, cada um com `key` (slug), `label` (nome de
exibição), `screenshot` (caminho da imagem) e uma lista de até 15 avaliações por área, cada uma
via o helper `R(area, tema, importancia, quebra, problema, solucao, justificativa=None,
contraste_medido=None, evidencia_narrada=None)`. Ver `scripts/data_exemplo.py` para o formato
exato e os comentários de cada campo.

## O padrão visual do HTML é fixo — vem de um arquivo de template literal

`gen_html.py` **não desenha HTML a partir do zero**. Ele carrega `assets/template_base.html` —
uma cópia literal, byte a byte, do padrão visual da Performa.it (extraído e validado a partir de
entregas reais anteriores da Performa.it, já revisado e aprovado internamente) — e faz
substituição de tokens `[[[NOME]]]` e expansão de blocos `<!--REPEAT:nome-->...<!--END:nome-->`
dentro dele. O CSS e o JS ficam inteiros dentro desse arquivo, sem nenhum token: são idênticos em
todo assessment gerado por esta skill, sempre.

Isso existe por um motivo concreto: se cada assessment fosse gerado por um LLM reescrevendo
HTML/CSS na hora, dois clientes diferentes — ou o mesmo cliente gerado em duas sessões
diferentes — poderiam sair com layout, cores, espaçamento ou estrutura sutilmente diferentes,
sem que ninguém pedisse essa mudança. Com um template literal + substituição de tokens, a
única forma de dois assessments divergirem no visual é alguém editar
`assets/template_base.html` de propósito — nunca como efeito colateral de "gerar de novo".

Ao usar esta skill para um novo cliente, **edite apenas `config.json`/`data.py`** — nunca
`assets/template_base.html` — para trocar cliente, produto, telas, achados e screenshots. Se o
usuário pedir explicitamente um visual diferente (outra cor, outro layout), isso é uma mudança na
própria skill (o template), não um parâmetro por cliente — converse com o usuário antes de tocar
no template, e trate como uma decisão deliberada, não uma personalização pontual.

Duas partes do HTML final continuam sendo **computadas**, não literais, porque dependem dos
dados: o gráfico SVG da matriz de risco (`build_risk_chart_svg()` em `gen_html.py`, posições dos
pontos variam com Erro%/Importância reais) e a numeração sequencial de página. Isso é esperado —
o que é fixo é a estrutura ao redor delas (moldura do slide, eixo, legenda, tipografia), não os
números em si. Uma terceira parte é semi-computada: o slide dedicado de metodologia lista, numa
tabela, quantos achados vieram de cada base teórica (Nielsen/ISO/Morville/WCAG/Miller/Performa) —
a estrutura da tabela é fixa, mas as linhas e contagens vêm de `compute_basis_rows(stats)`, então
cada cliente vê a distribuição real dos seus próprios achados, nunca um número copiado de outro
assessment.

### Cada slide tem um orçamento de altura fixo — respeite-o ao adicionar conteúdo novo

`.slide` é `1280×720px` com `overflow:hidden`; `.content-wrap` consome o resto depois do
`brandbar`/padding, sobrando **~608px de altura útil e ~1184px de largura útil**. Qualquer
elemento novo (gráfico, tabela, texto) que não caiba nesse espaço é cortado silenciosamente pelo
`overflow:hidden` — não gera erro nem warning, só corta visualmente. Isso já aconteceu duas vezes
nesta skill: o gráfico da matriz de risco ultrapassava a altura do slide, e a legenda desse mesmo
gráfico ficava sobreposta aos dados por estar posicionada dentro da área de plotagem em vez de
abaixo do eixo X. Ambos só foram descobertos ao renderizar o SVG isoladamente e inspecionar a
imagem (`cairosvg` + corte/inspeção via PIL — não há Playwright/Chromium garantido neste
ambiente). Ao adicionar qualquer visual nesse estilo, teste da mesma forma antes de considerar
pronto: gere o SVG/HTML isolado, renderize para imagem, e confira visualmente que nada é cortado
ou sobreposto — não confie só na ausência de erro de execução.

## Encaixe opcional no fluxo do Dojo Framework

Esta skill é um diagnóstico autocontido: não faz parte da sequência obrigatória de nenhuma FASE
do vault e pode ser usada em qualquer momento em que existam capturas de tela reais de um sistema
a avaliar — inclusive na pré-venda, se o cliente já fornecer prints do sistema atual nesse
estágio.

Há, porém, um encaixe natural e opcional dentro da `assets/FASE 2 - DISCOVERY.md` (não editada
por esta skill): a ETAPA 1 daquele documento (Reunião de Kick-Off) já solicita ao cliente
"Capturas de tela de outros sistemas já existentes (quando aplicável)" como parte dos materiais
de identidade visual/DESIGN SYSTEM. Essa é exatamente a evidência mínima exigida pela Etapa 1
(Intake) desta skill. Se o cliente fornecer prints de um sistema legado/atual nesse momento do
Kick-off, considere rodar esta skill como um diagnóstico AS-IS complementar — os campos
`diagnostico_ferramenta_atual` / `diagnostico_necessidade_negocio` do documento gerado podem
alimentar diretamente a ETAPA 2 daquele documento (Criação das PERSONAS, FUNCIONALIDADES,
JORNADAS e do DESIGN SYSTEM). Este uso é opcional e complementar — não altera, substitui nem
supre nenhum artefato exigido por `assets/FASE 2 - DISCOVERY.md`.

## Entregáveis rastreáveis no vault do projeto

`revisao_<cliente>.md` (o entregável da Etapa 3) é um documento rastreável do vault — versionado,
com dono e status — e deve começar com o frontmatter padrão do pacote (`phase`, `deliverable`,
`owner`, `status`, `source`, `related_issues`, `version`, `last_review`). Use
`templates/tpl-ux-assessment-revisao.md` (no pacote Dojo Framework) como ponto de partida em vez
de escrever esse cabeçalho do zero — ele já traz a estrutura por tela (screenshot, achados por
área, Importância/Quebra/Nota, justificativa, contraste medido, evidência narrada) alinhada aos
campos de `scripts/data_exemplo.py`. `matriz_<cliente>.xlsx` e `UX Assessment - <cliente>.html`
são artefatos gerados (planilha binária e HTML autocontido), sem frontmatter Markdown próprio —
referencie-os a partir do `.md` (campo `source`, ou um link relativo) para manter a
rastreabilidade entre os 3 entregáveis.

## Onde ler mais

- `references/metodo_pontuacao.md` — a fórmula completa (Importância × Quebra = Nota, Erro%,
  matriz de risco 2×2, semáforo de 2 cores).
- `references/bases_teoricas.md` — Nielsen, ISO 9241-110, WCAG 2.1, Morville, Miller/Hick, APCA e
  quando citar cada um, além da precisão terminológica ("heurística" vs. "critério").
- `references/apca_contraste.md` — como medir contraste real com `scripts/apca/`.
- `references/humanizacao.md` — o que a camada de humanização de texto verifica, incluindo as
  exceções (nomes próprios de tela, citações bibliográficas) que nunca devem ser reestruturadas.
- `references/captura_evidencias.md` — como tratar screenshots, vídeos e fluxos do Figma como
  evidência.
- `templates/tpl-ux-assessment-revisao.md` — modelo de frontmatter e estrutura por tela para o
  documento de revisão da Etapa 3 (ver seção "Entregáveis rastreáveis no vault do projeto" acima).

## Checklist antes de entregar

1. Toda tela avaliada tem pelo menos 1 screenshot real referenciado (nunca um placeholder).
2. Cada screenshot mostra de fato a tela/funcionalidade sendo avaliada — não um artefato que ela
   gera (ex.: um PDF exportado, um relatório impresso). Ver "Não confunda o artefato com a tela"
   em `captura_evidencias.md`; um achado analisado sobre a evidência errada invalida a avaliação
   inteira daquela tela, não só o achado específico.
3. Todo achado com Quebra ≠ Nenhum cita a base teórica correta (ver `bases_teoricas.md`).
4. Todo achado de contraste/legibilidade tem um valor Lc de APCA medido, não estimado.
5. O documento de revisão (Etapa 3) foi aprovado explicitamente antes de gerar XLSX/HTML finais.
6. `validate_html.py` retorna 0 erros estruturais.
7. `recalc.py` retorna 0 erros de fórmula no XLSX.
8. O Erro% por tela é idêntico entre XLSX e HTML.
9. A camada de humanização de narrativa executiva foi aplicada ao texto final (travessão em
   excesso reestruturado, não só repontuado — ver `humanizacao.md`).
10. A matriz de risco aparece no HTML como o gráfico visual do template (nunca uma tabela
    substituta), com o nome de cada tela e área preservado nos pontos e na legenda.
11. A síntese de diagnóstico (`diagnostico_ferramenta_atual`) nomeia explicitamente se existe (ou
    não) uma jornada única que atravessa as telas do produto — não é só a soma dos achados por
    tela isolada. Ver "Síntese de diagnóstico é sobre jornada, não só notas por tela" em
    `metodo_pontuacao.md`.
12. Nenhum HTML/XLSX gerado tem template/token literal sobrando (ex.: `[[[TELA_LABEL]]]`
    aparecendo no lugar de um valor real) — `gen_html.py` já falha alto se isso acontecer, mas
    confira visualmente mesmo assim antes de entregar.
13. A logo usa a variante certa por fundo: a variante clara/"como está" só em fundo escuro (capa,
    encerramento); uma variante escura — recolorida via `logo_dark_color` ou fornecida via
    `logo_dark_path` — no wordmark de topo de página em fundo claro. Nunca a mesma variante nos
    dois contextos (ver seção "Parametrização").
14. "Heurística" não aparece como sinônimo genérico em nenhum texto fixo (título, `aria-label`,
    contador) — só quando o achado específico vem de Nielsen. Ver `bases_teoricas.md`.
15. Qualquer elemento visual novo (gráfico, tabela grande) foi conferido contra o orçamento de
    ~608px de altura útil do slide, renderizando isoladamente para imagem antes de considerar
    pronto — não só confiando na ausência de erro de execução (ver "Cada slide tem um orçamento
    de altura fixo").
