---
name: cbs-completo
description: Use quando o time precisar transformar a primeira reunião com um cliente (Demanda Inicial / Refinamento da Demanda) em um CBS (Cost Breakdown Structure) pronto para embasar a proposta comercial — analisando a navegação gravada do sistema atual do cliente (timestamps de vídeo) para calibrar estimativas de FE e gerando o CSV final de horas FE/BE em UTF-8 BOM, com resumo de totais. Dispara com "gerar o CBS", "montar a proposta comercial", "processar a reunião de cliente", "fazer o pré-venda", "estimar o projeto em horas", "rodar o fluxo completo de pré-venda". Funciona sem vídeo — se não houver gravação, aplica um buffer de incerteza e segue apenas com a descrição textual.
---

# CBS Completo — Fluxo de Pré-Venda (Demanda Inicial → Refinamento da Demanda)

Este fluxo ocorre inteiramente dentro da **FASE 1 — Pré-Venda** do vault Dojo
Framework (ver `assets/FASE 1 - PREVENDA.md`), cobrindo as **Etapas 1 e 2**
daquele documento (**Demanda Inicial** e **Refinamento da Demanda**).

## MISSÃO

Transformar a primeira reunião com um cliente em um CBS (Cost Breakdown
Structure) completo e pronto para a **PROPOSTA COMERCIAL**, orquestrando três
etapas: duas delas já cobertas por skills irmãs deste pacote, e a terceira —
a geração do CBS em si — de responsabilidade exclusiva desta skill.

Esta skill é um **orquestrador fino** para as suas duas primeiras etapas: ela
não reimplementa a lógica de consolidação de contexto nem a de extração de
entregáveis, apenas verifica se já rodaram e invoca as skills correspondentes
quando necessário. A única lógica genuinamente nova e própria desta skill é a
análise de navegação de telas (ETAPA B1) e a geração do CBS em si (ETAPA C).

---

## FLUXO GERAL

```
INPUTS (transcript + vídeo/timestamps + docs do cliente)
    ↓
ETAPA A — CONSOLIDAÇÃO DO CONTEXTO ESTRATÉGICO (delegada)
    → skill consolidacao-pos-reuniao-inicial
    → Gera memória operacional do cliente
    ↓
ETAPA B — ANÁLISE DE TELAS + EXTRAÇÃO DE ENTREGÁVEIS
    → B1: Análise de navegação do sistema atual (conteúdo próprio desta skill)
    → B2: Estruturação de entregáveis candidatos (delegada a preparacao-refinamento-demanda)
    ↓
ETAPA C — GERAÇÃO DO CBS (conteúdo próprio desta skill)
    → Gera CBS_*.csv (UTF-8 BOM)
    → Gera CBS_*_resumo_*.md (totais separados)
```

---

## DETECÇÃO DE ESTADO — ONDE COMEÇAR

Antes de executar, verificar o que já existe na pasta do projeto:

| Condição | Ação |
|---|---|
| Não existem os artefatos gerados pela skill `consolidacao-pos-reuniao-inicial` nesta pasta de projeto | Invocar essa skill (ETAPA A), depois executar B1 + B2 + C |
| Artefatos da `consolidacao-pos-reuniao-inicial` existem, mas não há `entregaveis_*.md` nem análise de telas registrada | Executar ETAPA B (B1 + B2) + ETAPA C |
| `entregaveis_*.md` existe, mas não há CBS CSV | Executar só a ETAPA C |
| CBS CSV existe | Informar o usuário e perguntar se quer regenerar |

> Se houver dúvida, executar o fluxo completo (A → B1 → B2 → C).

> **Nota:** os nomes exatos dos arquivos gerados pela `consolidacao-pos-reuniao-inicial`
> vivem na SKILL.md daquela skill (`01_pre-venda/qualificacao/*`, conforme sua
> própria integração) — não assumir aqui os nomes numerados antigos
> (`01_client-context.md` etc.); esta skill não gera mais esses arquivos.

---

## FONTES DE CONTEXTO — LEITURA OBRIGATÓRIA

Consumir em ordem de prioridade:

1. **Transcript da reunião** — arquivo `.txt` na pasta (ex: `*transcript*.txt`,
   `*gravacao*.txt`). Reunião 1 (**Demanda Inicial**) e Reunião 2
   (**Refinamento da Demanda**), conforme `assets/FASE 1 - PREVENDA.md`.
2. **Timestamps de navegação do sistema atual** — arquivo `timestamps_*.md`
   ou `*navegacao*.md`
3. **Documentos do cliente** — PDFs, apresentações, e-mails mencionados
4. **Artefatos já existentes** — qualquer saída já gerada por
   `consolidacao-pos-reuniao-inicial` ou por `preparacao-refinamento-demanda`
   nesta pasta de projeto
5. **Screenshots** — se disponíveis, usar para calibrar estimativas FE

> **Sem vídeo ou screenshots:** a skill funciona normalmente. Adicionar nas
> Premissas do resumo: "Estimativas FE baseadas em descrição textual — sem
> navegação gravada do sistema atual. Recomendado revisar após prototipação."

---

## ETAPA A — CONSOLIDAÇÃO DO CONTEXTO ESTRATÉGICO (delegada)

> Cobre a **Demanda Inicial** (Etapa 1 da FASE 1 — Pré-Venda).

Antes de iniciar, verificar (ver DETECÇÃO DE ESTADO) se os artefatos já foram
gerados nesta pasta de projeto pela skill `consolidacao-pos-reuniao-inicial`
(ver `skills/consolidacao-pos-reuniao-inicial/SKILL.md`). Se não existirem,
invocar essa skill para produzi-los antes de prosseguir para a ETAPA B.
**Não reimplementar essa lógica aqui.**

Se o projeto já possuir `RASCUNHO_INTENT.md` ou `INTENT_REFINADO.md` (gerados
pelo fluxo Intent Listener/Refiner — ver `assets/SPEC_IntentListener.md` e
`assets/SPEC_IntentRefiner.md`), esses arquivos são a fonte de INTENT DO
PROJETO a usar — não pedir à `consolidacao-pos-reuniao-inicial` para gerar um
concorrente.

---

## ETAPA B — ANÁLISE DE TELAS + EXTRAÇÃO DE ENTREGÁVEIS

> Cobre o **Refinamento da Demanda** (Etapa 2 da FASE 1 — Pré-Venda), até a
> estruturação dos entregáveis candidatos que alimentarão o CBS.

### B1 — Análise de navegação do sistema atual (conteúdo próprio desta skill)

> Esta sub-etapa é exclusiva do `cbs-completo`: não existe equivalente em
> `preparacao-refinamento-demanda`. Preservar integralmente.

Se existir um arquivo de timestamps de vídeo (`timestamps_*.md`,
`*navegacao*.md`, ou similar):

1. Ler os timestamps e identificar as telas navegadas
2. Para cada tela relevante, registrar:
   - Nome/função da tela
   - Complexidade aparente (simples / média / alta)
   - Campos, ações, fluxos visíveis
   - Observações sobre UX e limitações do sistema atual
3. Usar essas observações para calibrar estimativas de FE na ETAPA C

Se **não houver** arquivo de timestamps:
- Registrar nas Premissas do resumo: "Estimativas FE baseadas em descrição
  textual — sem screenshots ou gravação do sistema atual. Adicionar 10–15%
  como buffer de incerteza em telas complexas."

### B2 — Estruturação dos entregáveis candidatos (delegada)

Para a extração de entregáveis candidatos e lacunas, invocar a skill
`preparacao-refinamento-demanda` (ver
`skills/preparacao-refinamento-demanda/SKILL.md`) se ainda não tiver sido
executada nesta pasta de projeto. **Não reimplementar essa lógica aqui.**

As observações de calibração de FE produzidas em B1 devem ser somadas como
insumo adicional à saída dessa skill irmã, mesmo quando o arquivo de
entregáveis vier dela — B1 não tem equivalente lá e não deve se perder.

O arquivo de entregáveis candidatos resultante (`entregaveis_*.md` ou
equivalente gerado por `preparacao-refinamento-demanda`) segue o formato
Épico > Feature abaixo, usado como insumo direto da ETAPA C. Ver também
`templates/tpl-entregaveis-candidatos.md` para a versão formalizada deste
artefato, caso o projeto decida rastreá-lo como entregável versionado do
vault.

Formato por feature:
```markdown
## Épico N: [Nome do Épico]

### N.X — [Nome da Feature]
**Tipo:** Nova | Ativa
**Situação:** Ativa
**Descrição:** O que entrega, fluxos principais, campos relevantes, regras de negócio
**Observações:** Dependências, riscos, integrações
**Premissas:** O que precisa ser verdadeiro para esta estimativa ser válida
```

Critérios de agrupamento a observar (herdados do conceito de Épico usado por
`preparacao-refinamento-demanda`, reforçados aqui porque calibram o CBS):
- Coesão funcional (mesma jornada de usuário ou módulo)
- Independência suficiente para entrega incremental
- Orientação a valor de negócio
- Granularidade: 1 Feature = 1 entregável testável pelo usuário

---

## ETAPA C — GERAÇÃO DO CBS (conteúdo próprio desta skill)

> Executar sempre (última etapa do fluxo). Esta é a única lógica sem qualquer
> equivalente nas skills irmãs — preservada integralmente.

### Especificação das colunas (ordem exata)

| Col | Header | Notas |
|---|---|---|
| A | `Tipo` | `Nova` ou `Ativa` |
| B | `Situação` | `Ativa` (padrão) |
| C | `Épico (número e nome)` | Ex: `Épico 1: Gestão de Agenda` |
| D | `Feature/Entregável (número e nome)` | Ex: `1.1 Agenda Diária e Semanal` |
| E | `Descrição/Compreensão da Feature ou Entregável` | Fluxos, campos, regras de negócio |
| F | `Horas FE (IA)` | número |
| G | `Horas BE (IA)` | número |
| H | `Horas Totais (IA)` | F + G |
| I | `Observações` | Dependências, riscos, decisões abertas |
| J | `Premissas` | O que deve ser verdadeiro para a estimativa ser válida |

### Encoding obrigatório

**UTF-8 BOM** — usar `encoding='utf-8-sig'` no Python. Garante que acentos
abram corretamente no Excel e Numbers sem conversão manual.

### Modelo de estimativa — alavancagem de IA explícita

> Ver `docs/adr/ADR-001-calibracao-ia-dlc-cbs.md` para o racional completo desta
> calibração e as alternativas descartadas.

As tabelas abaixo têm **duas colunas**:

- **Base (convencional):** esforço sem assistência de IA. É a régua antiga.
- **IA-DLC:** esforço com o modelo de entrega da `FASE 4 — DESENVOLVIMENTO`
  (agente propõe plano e gera a implementação, engenheiro valida e aprova).
  **É esta a coluna que vai para o CBS**, desde que o gate de pré-condições
  abaixo esteja satisfeito.

A fórmula aplicada por feature:

```
Horas = valor IA-DLC × Fator_Reúso    (respeitado o piso de overhead humano)
```

**Fator de reúso** — o Nº de vezes que o mesmo padrão aparece *neste projeto*:

| Ocorrência do padrão no projeto | Fator |
|---|---|
| 1ª (cria o componente/serviço de referência) | 1,0× |
| 2ª e 3ª | 0,7× |
| 4ª em diante | 0,5× |

**Piso de overhead humano** — nenhuma feature abaixo de **2h FE** ou **2h BE**
quando aquela camada for tocada. É o custo irredutível de ler a SPEC, revisar o
que o agente gerou, validar com o cliente e aprovar o PR — a IA não remove esse
ciclo. Se a composição de fatores levar abaixo do piso, usar o piso.

#### Gate de pré-condições da coluna IA-DLC

A coluna IA-DLC **só é válida** se estas condições forem verdadeiras. Verificar
antes de estimar; o que falhar, estimar pela coluna Base e registrar nas
Premissas da linha:

- [ ] `DESIGN.md` / design system definido e aprovado antes do desenvolvimento
      → se não: **FE pela coluna Base**
- [ ] `CONTEXT.md` e `AGENT_RULES.md` preenchidos (FASE 3, Etapa 6)
      → se não: **coluna Base para todo o projeto**
- [ ] `SPEC_{FUNCIONALIDADE}.md` produzida antes de cada bolt (FASE 4, Etapa 3)
      → se não: **coluna Base para todo o projeto**
- [ ] Stack mainstream e bem representada (ex: React/TS, Node, .NET, Python)
      → se stack de nicho ou proprietária: **+30% sobre a coluna IA-DLC**
- [ ] Greenfield, **ou** base legada com cobertura de testes
      → se legado sem testes: **coluna Base para o que tocar o legado**
- [ ] Time treinado no fluxo AI-DLC (não é "usar IA às vezes")
      → se não: **coluna Base**

> Registrar no resumo do CBS quais pré-condições foram assumidas. É o que torna
> a estimativa defensável — o número baixo é o preço de um caminho de entrega
> específico, não otimismo.

### Tabela de referência — estimativas FE

| Tipo de tela / componente | Base | **IA-DLC** | Fator |
|---|---|---|---|
| Tela de listagem simples (tabela + filtros básicos) | 8–12h | **3–5h** | 0,4× |
| Tela de listagem com filtros complexos + export | 12–18h | **5–8h** | 0,45× |
| Formulário simples (até 10 campos) | 8–12h | **3–5h** | 0,4× |
| Formulário complexo (múltiplas abas, validações, 20+ campos) | 16–24h | **8–12h** | 0,5× |
| Modal / drawer de detalhe | 6–10h | **2–4h** | 0,4× |
| Dashboard / painel com gráficos e indicadores | 16–24h | **8–12h** | 0,5× |
| Fluxo multi-step / wizard (3–5 etapas) | 20–30h | **10–16h** | 0,5× |
| Agenda / calendário interativo | 30–50h | **18–28h** | 0,55× |
| Timeline cronológica | 12–18h | **5–8h** | 0,45× |
| Tela de prescrição / editor texto livre | 12–20h | **6–10h** | 0,5× |
| Integração de componente externo (embed/iframe) | 8–16h | **5–10h** | 0,6× |
| Painel de exibição em TV / display tempo real | 12–20h | **7–12h** | 0,6× |
| Upload + preview de arquivo/imagem | 8–14h | **4–7h** | 0,5× |
| Notificações e toasts | 4–6h | **1–2h** | 0,3× |
| Componentes compartilhados reutilizáveis | 6–12h | **3–6h** | 0,5× |
| Configuração / cadastro simples | 8–14h | **3–5h** | 0,4× |

> **Sem screenshots/timestamps:** aumentar FE em 10–15% e registrar nas
> Observações: "Estimativa FE baseada em descrição textual — sem gravação do
> sistema atual."

### Tabela de referência — estimativas BE

| Tipo de operação | Base | **IA-DLC** | Fator |
|---|---|---|---|
| CRUD simples (1 entidade, sem regras complexas) | 8–12h | **3–5h** | 0,4× |
| CRUD com regras de negócio (validações, workflows) | 12–20h | **6–10h** | 0,5× |
| Integração com API externa simples (REST documentada) | 8–16h | **5–10h** | 0,6× |
| Integração com API externa complexa (bidirecional, webhooks) | 20–40h | **14–28h** | 0,7× |
| Motor de regras de negócio | 20–40h | **12–24h** | 0,6× |
| Relatório / query analítica complexa | 12–24h | **6–12h** | 0,5× |
| Sistema de notificações (push/email/SMS/WhatsApp) | 12–20h | **7–12h** | 0,6× |
| Sistema de permissões / RBAC | 16–24h | **8–12h** | 0,5× |
| Upload e processamento de arquivos | 8–16h | **4–8h** | 0,5× |
| Pipeline ETL / migração de dados | 24–80h | **18–60h** (por entidade) | 0,75× |
| Autenticação e gestão de sessão | 12–20h | **4–8h** | 0,35× |
| WebSocket / atualização em tempo real | 12–20h | **7–12h** | 0,6× |
| Geração de PDF / documentos | 8–16h | **4–8h** | 0,5× |

#### Por que os fatores não são iguais

O fator não mede "quanto a IA ajuda" em abstrato — mede **quanto do esforço
daquele item é digitação de código previsível**, que é o que a IA colapsa.

- **Alta alavancagem (0,3–0,45×)** — auth, CRUD, formulários, listagens, toasts:
  padrões massivamente representados; o agente entrega quase pronto a partir da
  SPEC e do design system.
- **Média (0,5–0,6×)** — dashboards, wizards, RBAC, motor de regras: metade do
  esforço é decisão de negócio e modelagem, que continua humana.
- **Baixa (0,7–0,75×)** — integração complexa com terceiro e migração de dados:
  o gargalo é externo e empírico (sandbox indisponível, contrato de API que só
  se revela na prática, dado sujo que ninguém mapeou). Gerar código rápido não
  resolve descobrir a realidade do outro lado.

> Ao subir o fator acima do valor da tabela, explicar o motivo nas Observações
> da linha. Ao baixar, idem. A tabela é ponto de partida, não veredito.

### Regras de granularidade

- **1 linha = 1 feature** — nunca agregar features distintas
- **Piso:** nenhuma feature abaixo de 2h na camada que ela toca (FE e/ou BE)
- **Feature grande:** se FE > 24h **ou** BE > 32h na régua IA-DLC, registrar nas
  Observações: "Recomendado dividir em sub-features no backlog"
- Épicos numerados sequencialmente sem pular; Features numeradas N.1, N.2...

### Validações antes de salvar

- [ ] Nenhuma linha com horas = 0 sem justificativa
- [ ] Horas Totais = FE + BE em todas as linhas
- [ ] Todos os épicos numerados sequencialmente
- [ ] Nenhuma feature sem descrição
- [ ] Features `Nova` com descrição ampliada
- [ ] Features com integração externa têm Premissas preenchidas
- [ ] **Gate de pré-condições IA-DLC verificado** — e o resultado registrado no
      resumo; o que falhou está estimado pela coluna Base
- [ ] **Piso respeitado** — nenhuma feature abaixo de 2h na camada que toca
- [ ] **Fator de reúso aplicado** onde o mesmo padrão se repete no projeto
- [ ] Desvios da tabela (para cima ou para baixo) justificados nas Observações

### Arquivos a gerar

**Arquivo principal:** `CBS_[nome-do-projeto]_v1.csv`
- Encoding: UTF-8 BOM (`utf-8-sig`)
- Separador: vírgula
- Campos com vírgula interna: entre aspas duplas
- **Sem linhas de resumo ou totais no CSV** — quebram importação no Excel e Jira

**Arquivo de resumo:** `CBS_[nome-do-projeto]_resumo_v1.md`
- Tabela de totais por épico (FE, BE, Total, Dias)
- Totais por fase/sistema
- Total geral
- Distribuição FE × BE (%)
- **Fatores aplicados** — régua usada (IA-DLC ou Base), resultado do gate de
  pré-condições, e onde a coluna Base foi usada apesar da régua IA-DLC
- Features com flag "Recomendado dividir no backlog"
- Decisões abertas que afetam o escopo
- Premissas globais

Ver `templates/tpl-cbs.md` para o esqueleto padronizado do CSV e do resumo,
incluindo o bloco de frontmatter rastreável do vault.

> Estes dois arquivos alimentam diretamente as seções "Entregáveis" e
> "Cronograma estimado"/"Investimento e condições comerciais" de
> `templates/tpl-proposta-comercial.md`, e a seção "2. Entregáveis" de
> `templates/tpl-memoria-projeto.md` quando o projeto for aprovado.

---

## PREMISSAS GLOBAIS (incluir no resumo .md)

- Estimativa em horas; **8h = 1 dia útil**
- **Régua IA-DLC:** as horas assumem o modelo de entrega da `FASE 4 —
  DESENVOLVIMENTO` (agente de IA gera a implementação, engenheiro valida e
  aprova), com o gate de pré-condições satisfeito. Sem esse caminho de entrega,
  a estimativa correta é a coluna Base — tipicamente **~2× o valor apresentado**
- Horas incluem o ciclo humano de revisão, validação e aprovação do código
  gerado — a IA reduz a escrita, não a validação
- **1 dev fullstack por feature**; FE e BE estimados separadamente
- Estimativas **não incluem:** QA automatizado, DevOps/infra, gestão de
  projeto, documentação técnica
- Integrações com APIs de terceiros: assume API **documentada e disponível**
  — se não documentada: buffer de 30–50%
- Migração de dados: estimada em épico próprio — não incluída nas features
  funcionais
- Layout/design: FE assume **Figma/protótipo aprovado** antes do
  desenvolvimento
- Os fatores de alavancagem são **julgamento de engenharia calibrado**, não
  medição histórica — devem ser corrigidos por estimado × realizado ao longo dos
  bolts (ver `docs/adr/ADR-001-calibracao-ia-dlc-cbs.md`)

---

## FRONTMATTER E MEMÓRIA DE TRABALHO

Os artefatos gerados pela ETAPA A e pela ETAPA B2 pertencem às skills irmãs
que os produzem — seguir o frontmatter e a convenção de nome definidos em
cada uma delas.

Dentro desta skill: o `entregaveis_*.md` (quando gerado por esta skill na
ausência de `preparacao-refinamento-demanda`) e as notas de análise de telas
da B1 são memória de trabalho interna e não seguem o frontmatter padrão do
vault. Já o `CBS_[nome-do-projeto]_resumo_v1.md`, por ser um entregável
rastreável, deve incluir o bloco de frontmatter padrão (`phase: 01_pre-venda`,
`deliverable: Cost Breakdown Structure (CBS)`, `owner: Performa_IT`,
`status: draft`, `source: entregaveis_[nome-do-projeto]_v1.md`,
`related_issues:`, `version: 0.1`, `last_review: [data]`) conforme
`templates/tpl-cbs.md`.

---

## INSTRUÇÃO DE EXECUÇÃO

**Passo 0:** Confirmar que o projeto já possui uma chave **PIPROJETO-XXXX**
registrada (ver `assets/FASE 1 - PREVENDA.md`, Etapa 1). Se não houver,
alertar o responsável pelo projeto antes de prosseguir.

**Passo 1:** Detectar o estado atual da pasta (ver DETECÇÃO DE ESTADO —
quais etapas/artefatos já existem, inclusive das skills irmãs).

**Passo 2:** Executar as etapas necessárias em sequência:
- ETAPA A — invocar `consolidacao-pos-reuniao-inicial` se seus artefatos
  ainda não existirem
- ETAPA B1 — análise de navegação de telas (conteúdo próprio, sempre que
  houver timestamps/screenshots disponíveis)
- ETAPA B2 — invocar `preparacao-refinamento-demanda` se `entregaveis_*.md`
  ainda não existir
- ETAPA C — gerar o CBS (sempre, é a etapa final). Antes de estimar qualquer
  linha, percorrer o **gate de pré-condições IA-DLC** e decidir a régua
  (IA-DLC ou Base, no todo ou por camada). Se o gate não puder ser verificado
  com o cliente nesta etapa, assumir IA-DLC e declarar isso como premissa
  explícita — nunca silenciosamente.

**Passo 3:** Ao final, reportar:
- Quais etapas foram executadas nesta execução (e quais skills irmãs foram
  invocadas, se alguma)
- **Régua usada e resultado do gate de pré-condições** — inclusive o que ficou
  na coluna Base e por quê
- Total de Épicos e Features gerados
- Total geral de horas (FE + BE)
- Arquivos criados com seus caminhos
- Decisões abertas que podem impactar o escopo
- Recomendação de próximos passos (ex: validar entregáveis com o cliente
  antes de enviar a proposta)

---

## NOTA FINAL

Esta skill orquestra o fluxo de pré-venda cobrindo a Demanda Inicial e o
Refinamento da Demanda até a entrega do CBS:

```
Reunião 1 — Demanda Inicial (transcript)
    → ETAPA A: skill consolidacao-pos-reuniao-inicial (delegada)
    → ETAPA B1: análise de telas (conteúdo próprio desta skill)
    → ETAPA B2: skill preparacao-refinamento-demanda (delegada)
    → ETAPA C: geração do CBS (conteúdo próprio desta skill)
    → OUTPUT: CBS pronto para embasar a PROPOSTA COMERCIAL
```
