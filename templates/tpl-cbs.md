---
phase: 01_pre-venda
deliverable: Cost Breakdown Structure (CBS)
owner: Performa_IT
status: draft
source: [entregaveis_[nome-do-projeto]_v1.md; skill cbs-completo, ETAPA C]
related_issues:
version: 0.1
last_review: [data]
---

# CBS - [Nome do Projeto]

Cost Breakdown Structure gerado pela skill `cbs-completo` (ETAPA C), a partir
dos entregáveis candidatos estruturados na ETAPA B — ver `skills/cbs-completo/SKILL.md`.
Alimenta diretamente as seções "Entregáveis" e "Cronograma estimado"/"Investimento
e condições comerciais" de `templates/tpl-proposta-comercial.md`, e a seção
"2. Entregáveis" de `templates/tpl-memoria-projeto.md` quando o projeto for
aprovado.

## Arquivo CSV principal

**Arquivo:** `CBS_[nome-do-projeto]_v1.csv`

### Especificação das colunas (ordem exata)

| Col | Header | Notas |
|---|---|---|
| A | `Tipo` | `Nova` ou `Ativa` |
| B | `Situação` | `Ativa` (padrão) |
| C | `Épico` | **Apenas o nome, sem numeração e sem a palavra "Épico".** Ex: `Gestão de Agenda` |
| D | `Feature/Entregável` | **Apenas o nome, sem numeração.** Ex: `Agenda Diária e Semanal` |
| E | `Descrição/Compreensão da Feature ou Entregável` | Fluxos, campos, regras de negócio |
| F | `Horas FE (IA)` | número |
| G | `Horas BE (IA)` | número |
| H | `Horas Totais (IA)` | F + G |
| I | `Observações` | Dependências, riscos, decisões abertas |
| J | `Premissas` | O que deve ser verdadeiro para a estimativa ser válida |

### Encoding obrigatório

**UTF-8 BOM** — usar `encoding='utf-8-sig'` no Python. Garante que acentos
abram corretamente no Excel e Numbers sem conversão manual.

Regras adicionais do CSV:
- Separador: vírgula
- Campos com vírgula interna: entre aspas duplas
- **Sem linhas de resumo ou totais no CSV** — quebram importação no Excel e Jira

## Modelo de estimativa — alavancagem de IA explícita

> Racional completo e alternativas descartadas em
> `docs/adr/ADR-001-calibracao-ia-dlc-cbs.md`.

As tabelas têm **duas colunas**:

- **Base (convencional):** esforço sem assistência de IA.
- **IA-DLC:** esforço com o modelo de entrega da `FASE 4 — DESENVOLVIMENTO`
  (agente de IA gera a implementação, engenheiro valida e aprova). **É esta a
  coluna que vai para o CBS**, desde que o gate de pré-condições esteja
  satisfeito.

Fórmula aplicada por feature:

```
Horas = valor IA-DLC × Fator_Reúso    (respeitado o piso de overhead humano)
```

**Fator de reúso** — Nº de vezes que o mesmo padrão aparece *neste projeto*:

| Ocorrência do padrão no projeto | Fator |
|---|---|
| 1ª (cria o componente/serviço de referência) | 1,0× |
| 2ª e 3ª | 0,7× |
| 4ª em diante | 0,5× |

**Piso de overhead humano** — nenhuma feature abaixo de **2h FE** ou **2h BE**
na camada que ela toca. É o custo irredutível de ler a SPEC, revisar o código
gerado, validar com o cliente e aprovar o PR.

### Gate de pré-condições da coluna IA-DLC

A coluna IA-DLC **só é válida** se estas condições forem verdadeiras. O que
falhar, estimar pela coluna Base e registrar nas Premissas da linha:

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

## Tabela de referência — estimativas FE

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

## Tabela de referência — estimativas BE

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

### Por que os fatores não são iguais

O fator mede **quanto do esforço daquele item é digitação de código
previsível** — que é o que a IA colapsa —, não "quanto a IA ajuda" em abstrato.

- **Alta alavancagem (0,3–0,45×)** — auth, CRUD, formulários, listagens, toasts.
- **Média (0,5–0,6×)** — dashboards, wizards, RBAC, motor de regras: metade do
  esforço é decisão de negócio e modelagem, que continua humana.
- **Baixa (0,7–0,75×)** — integração complexa com terceiro e migração de dados:
  o gargalo é externo e empírico, não velocidade de escrita.

> Desvios da tabela, para cima ou para baixo, devem ser justificados nas
> Observações da linha.

## Regras de granularidade

- **1 linha = 1 feature** — nunca agregar features distintas
- **Piso:** nenhuma feature abaixo de 2h na camada que ela toca (FE e/ou BE)
- **Feature grande:** se FE > 24h **ou** BE > 32h na régua IA-DLC, registrar nas
  Observações: "Recomendado dividir em sub-features no backlog"
- **Sem numeração** em Épico e Feature — só o nome. Nada de `Épico 1:`, `1.1`,
  `N.N` ou prefixo equivalente em nenhuma das duas colunas
- A **ordem das linhas** no CSV carrega a sequência lógica de entrega, que antes
  era carregada pela numeração: features do mesmo épico ficam contíguas, e os
  épicos aparecem na ordem em que devem ser entregues
- Nomes de épico e de feature devem ser **únicos** no CBS — sem o número, o nome
  é a única chave de referência em Observações, dependências e backlog

## Validações antes de salvar

- [ ] Nenhuma linha com horas = 0 sem justificativa
- [ ] Horas Totais = FE + BE em todas as linhas
- [ ] **Nenhum prefixo de numeração** nas colunas `Épico` e `Feature/Entregável`
      (nem `Épico 1:`, nem `1.1`, nem `N.N`)
- [ ] Nomes de épico e de feature únicos no CBS
- [ ] Linhas do mesmo épico contíguas, na ordem lógica de entrega
- [ ] Nenhuma feature sem descrição
- [ ] Features `Nova` com descrição ampliada
- [ ] Features com integração externa têm Premissas preenchidas
- [ ] Gate de pré-condições IA-DLC verificado e registrado no resumo
- [ ] Piso de 2h respeitado na camada tocada
- [ ] Fator de reúso aplicado onde o padrão se repete
- [ ] Desvios da tabela justificados nas Observações

## Arquivo de resumo

**Arquivo:** `CBS_[nome-do-projeto]_resumo_v1.md`

### Totais por épico

| Épico | Horas FE | Horas BE | Horas Totais | Dias (8h/dia) |
|---|---|---|---|---|
| [Nome do Épico — sem numeração] | [FE] | [BE] | [Total] | [Dias] |

### Totais por fase/sistema

[Agrupamento por fase de entrega ou por sistema/módulo, se fizer sentido para o projeto.]

### Total geral

- Horas FE: [total]
- Horas BE: [total]
- Horas Totais: [total]
- Dias estimados (8h = 1 dia útil): [total]

### Distribuição FE × BE

- FE: [%]
- BE: [%]

### Fatores aplicados

- **Régua usada:** [IA-DLC | Base | mista — detalhar]
- **Gate de pré-condições IA-DLC:**

| Pré-condição | Atendida? | Consequência aplicada |
|---|---|---|
| DESIGN.md / design system aprovado | [Sim/Não] | [—  / FE pela coluna Base] |
| CONTEXT.md + AGENT_RULES.md preenchidos | [Sim/Não] | [— / coluna Base] |
| SPEC por funcionalidade antes do bolt | [Sim/Não] | [— / coluna Base] |
| Stack mainstream | [Sim/Não] | [— / +30% sobre IA-DLC] |
| Greenfield ou legado com testes | [Sim/Não] | [— / Base no legado] |
| Time treinado em AI-DLC | [Sim/Não] | [— / coluna Base] |

- **Épicos/features estimados pela coluna Base apesar da régua IA-DLC:**
  [lista e motivo]
- **Fator de reúso aplicado em:** [padrões repetidos e ocorrências]
- **Desvios manuais da tabela:** [feature, fator usado, motivo]

### Features sinalizadas para divisão no backlog

- [Feature] — [motivo: FE > 40h / BE > 60h]

### Decisões abertas que afetam o escopo

- [Decisão pendente e quem precisa validá-la]

## Premissas globais

- Estimativa em horas; **8h = 1 dia útil**
- **Régua IA-DLC:** as horas assumem o modelo de entrega da `FASE 4 —
  DESENVOLVIMENTO` (agente de IA gera a implementação, engenheiro valida e
  aprova), com o gate de pré-condições satisfeito. Sem esse caminho de entrega,
  a estimativa correta é a coluna Base — tipicamente **~2× o valor apresentado**
- Horas incluem o ciclo humano de revisão, validação e aprovação do código
  gerado — a IA reduz a escrita, não a validação
- Os fatores de alavancagem são **julgamento de engenharia calibrado**, não
  medição histórica — corrigir por estimado × realizado ao longo dos bolts
- **1 dev fullstack por feature**; FE e BE estimados separadamente
- Estimativas **não incluem:** QA automatizado, DevOps/infra, gestão de
  projeto, documentação técnica
- Integrações com APIs de terceiros: assume API **documentada e disponível**
  — se não documentada: buffer de 30–50%
- Migração de dados: estimada em épico próprio — não incluída nas features
  funcionais
- Layout/design: FE assume **Figma/protótipo aprovado** antes do
  desenvolvimento
- [Premissa adicional específica deste projeto, se houver]
