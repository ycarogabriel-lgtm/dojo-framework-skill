---
name: geracao-backlog
description: Use when the Backlog Agent needs to turn refinement documents and SPECs into traceable backlog items in the Dojo Framework — structuring user stories, épicos, acceptance criteria (BDD/Gherkin), technical tasks and AI-DLC eligibility as Jira stories, linked to the Obsidian vault (memory) and to GitHub PRs (code execution). Jira remains the backlog management tool, GitHub is the code execution layer, and the vault is the source of truth.
---

# Geração de Backlog no Dojo Framework (AI-DLC)

Esta skill define como o **Agente de Backlog** estrutura o output do backlog dentro do Dojo Framework, que opera com três camadas complementares: **o vault (Obsidian) é a memória** (SPECs, refinamentos, decisões, riscos), **o Jira é a ferramenta de gestão do backlog** (épicos, histórias, subtasks, sprints) e **o GitHub é a camada de execução de código** (branches, commits, PRs, releases). Por isso o backlog é gerado como **histórias do Jira rastreáveis**, sempre ligadas de volta aos artefatos do vault (`DOCUMENTO DE REFINAMENTO`, `SPEC_{FUNCIONALIDADE}.md`, `CONTEXT.md`, `INTENT DO PROJETO`, `REGISTRO DE RISCOS`) e, na implementação, ao PR correspondente no GitHub.

O backlog é criado na **FASE 4 — DESENVOLVIMENTO, ETAPA 1.3**, a partir dos documentos de refinamento por funcionalidade da FASE 2 e do DOCUMENTO DE ARQUITETURA DO PROJETO da FASE 3.

## Pré-requisitos (gate de contexto)

Antes de gerar qualquer história, confirme que os insumos abaixo existem e estão aprovados. Se algum faltar, **pergunte antes de gerar** — nunca preencha com suposições.

- `04_desenvolvimento/contexto-agentes/CONTEXT.md` — INTENT, arquitetura, jornadas/funcionalidades com status
- `04_desenvolvimento/contexto-agentes/AGENT_RULES.md` — regras de arquitetura, NFRs, segurança e qualidade
- `04_desenvolvimento/specs/SPEC_{FUNCIONALIDADE}.md` — o COMO técnico da funcionalidade
- `02_discovery/refinamentos/` — DOCUMENTO DE REFINAMENTO (o QUE) por funcionalidade
- `02_discovery/.../DESIGN.md` — referência de UI/UX da jornada
- `_risks/REGISTRO_RISCOS_INICIAL.md` — riscos com impacto no desenvolvimento

## Rastreabilidade vault ↔ Jira ↔ GitHub (regra central)

Toda história do Jira **deve** conter, na descrição, links para os artefatos de memória que a originaram; e todo artefato relevante do vault deve, quando existir, apontar para a história do Jira e para o PR correspondente.

- História (Jira) → vault: link para `SPEC_{FUNCIONALIDADE}.md`, DOCUMENTO DE REFINAMENTO, jornada e `DESIGN.md`.
- Vault → Jira/GitHub: no artefato, registre a chave da história (ex.: `{PROJETO}-123`), a sprint e o PR.
- Jira ↔ GitHub: vincule a história ao PR (integração Jira-GitHub / Smart Commits), citando a chave da história na branch e no commit.
- Uma funcionalidade **não entra em um BOLT/Sprint sem SPEC**.

---

## Mapeamento de Campos → Jira

| Campo no Template | Campo no Jira | Tipo / Observação |
|---|---|---|
| `[EPIC-X] US-YYY: Título` | **Summary** | Text |
| Descrição + Critérios de Aceite | **Description** | Wiki/Markdown (ver exemplos) |
| Story Points | **Story point estimate** | Number (Fibonacci) |
| Prioridade MoSCoW | **Priority** | Highest / High / Medium / Lowest |
| Componente | **Component/s** | Backend / Frontend / Fullstack / Infra |
| Épico | **Epic Link** | Um épico agrupa histórias |
| Bolt (ciclo semanal) | **Sprint** | Sprint do board = bolt |
| Dependências | **Linked Issues** (is blocked by) | Issue Link |
| Tarefas Técnicas | **Sub-tasks** | Child Issues |
| Elegibilidade IA | **Labels** | `ai-eligible` / `ai-partial` / `ai-manual` |
| Rastreabilidade vault | **Description** (links) | `SPEC_*.md`, refinamento, `DESIGN.md` |
| Execução de código | **Linked PR** (integração Jira-GitHub) | PR/commit citando a chave da história |

### Mapeamento de Prioridade

| MoSCoW | Jira Priority | Semântica |
|--------|---------------|-----------|
| Must Have | Highest | Bloqueia o MVP |
| Should Have | High | Importante, mas contornável |
| Could Have | Medium | Desejável se houver folga |
| Won't Have | Lowest | Fora do sprint/MVP atual |

### Elegibilidade AI-DLC (autonomia do agente)

No AI-DLC o agente é protagonista: **o agente propõe o plano, o engenheiro aprova, o agente executa**. Por isso a coluna "Elegível IA?" das tarefas técnicas indica o **nível de autonomia** e onde o checkpoint humano é obrigatório:

| Marcador | Significado |
|----------|-------------|
| **Sim** | Agente executa de ponta a ponta; revisão humana ao final |
| **Parcial** | Agente executa, mas exige checkpoint humano em ponto crítico (segurança, regra financeira, contrato de integração) |
| **Não** | Exige decisão humana/arquiteto antes ou durante (ex.: integração externa não documentada, regra fiscal, impacto financeiro) |

---

## Exemplo Completo: História de CRUD

> Os exemplos abaixo são esqueletos neutros — ao gerar o backlog real de um
> projeto, substitua entidade, regras de negócio, stack e critérios de aceite
> pelo domínio e pela arquitetura descritos no `CONTEXT.md` e no
> `SPEC_{FUNCIONALIDADE}.md` daquele projeto. Nunca reaproveite os nomes de
> entidade ou as regras de exemplo como se fossem o domínio real.

```markdown
### [EPIC-X] US-001: [Ação principal] de [entidade] por [persona]

**Tipo:** Story
**Épico:** [Nome do Épico]
**Sprint:** Bolt N
**Componente:** Fullstack
**Prioridade (MoSCoW):** Must Have · Priority: Highest
**Story Points:** [N] — [justificativa: complexidade, camadas envolvidas, regras de negócio]
**Dependências:** [Nenhuma / US-YYY]

#### Rastreabilidade (vault)
- SPEC: `04_desenvolvimento/specs/SPEC_{FUNCIONALIDADE}.md`
- Refinamento: `02_discovery/refinamentos/REFINAMENTO_{X}.md`
- Jornada / Design: `DESIGN.md` — Jornada de [Nome]
- INTENT: `CONTEXT.md` > INTENT DO PROJETO

#### Descrição
Como um **[persona]**, eu quero **[ação]** para **[benefício de negócio]**.

[Regras de negócio relevantes, extraídas do refinamento — não inventadas aqui.]

**Referência:** Refinamento > Regra de Negócio RN-00X.

#### Critérios de Aceite (BDD/Gherkin)

​```gherkin
Cenário: [caminho feliz]
  Dado que [pré-condição]
  E [dado adicional]
  Quando [ação do usuário]
  Então [resultado esperado]

Cenário: [caminho de erro]
  Dado que [pré-condição de erro]
  Quando [ação do usuário]
  Então [erro esperado]
  E [efeito colateral esperado, ex.: não persiste duplicata]
​```

#### Definição de Pronto (DoD — FASE 4)
- [ ] Código implementado e revisado (code review humano)
- [ ] Testes unitários dos critérios de aceite passando, cobertura mínima do `AGENT_RULES.md`
- [ ] Build limpo, sem warnings de lint
- [ ] Quality gate aprovado (conforme ferramenta definida em `AGENT_RULES.md`)
- [ ] Publicado no ambiente de DEV
- [ ] Validação do designer com base no `DESIGN.md`
- [ ] `CONTEXT.md` atualizado (status da funcionalidade)

#### Tarefas Técnicas (Subtasks)

| # | Tarefa | Componente | Estimativa | Elegível IA? | Justificativa |
|---|--------|------------|------------|--------------|---------------|
| 1 | [Backend] Migration/schema da entidade | Backend | [Xh] | Sim | Migration padrão, schema no SPEC |
| 2 | [Backend] Model/entidade com validações | Backend | [Xh] | Sim | Validação padrão descrita no SPEC |
| 3 | [Backend] Regra de negócio central | Backend | [Xh] | Parcial | Regra com impacto de negócio exige revisão |
| 4 | [Backend] Endpoint REST | Backend | [Xh] | Sim | Controller REST padrão (DTO) |
| 5 | [Frontend] Tela/formulário | Frontend | [Xh] | Sim | Formulário com design system |
| 6 | [Teste] Unitários backend | Backend | [Xh] | Sim | Testes padrão dos critérios de aceite |
| 7 | [Teste] E2E do fluxo | Frontend | [Xh] | Sim | Fluxo determinístico |

#### Notas Técnicas
[Stack alvo, padrões de API, restrições de UI — todos extraídos do `AGENT_RULES.md`/`CONTEXT.md` do projeto real, nunca assumidos.]
```

---

## Exemplo: História de Integração Externa (mockada no MVP)

```markdown
### [EPIC-Y] US-010: Consulta a [serviço externo] em [gatilho de negócio]

**Tipo:** Story
**Épico:** [Nome do Épico]
**Sprint:** Bolt N
**Componente:** Backend
**Prioridade (MoSCoW):** Must Have · Priority: Highest
**Story Points:** [N] — integração (mockada no MVP) com múltiplos cenários
**Dependências:** [US-YYY, US-ZZZ]

#### Rastreabilidade (vault)
- SPEC: `04_desenvolvimento/specs/SPEC_{FUNCIONALIDADE}.md`
- Riscos: `_risks/REGISTRO_RISCOS_INICIAL.md` (risco de integração externa)
- Escopo: `CONTEXT.md` — chamada **simulada com mock** no MVP

#### Descrição
Como o **sistema**, ao [gatilho de negócio], eu quero **consultar [serviço externo]** para [efeito esperado].

No MVP a chamada é **mockada**; a integração real é fase posterior e depende de documento de arquitetura aprovado.

#### Tarefas Técnicas (Subtasks)

| # | Tarefa | Componente | Estimativa | Elegível IA? | Justificativa |
|---|--------|------------|------------|--------------|---------------|
| 1 | [Backend] Service com provider mockável | Backend | [Xh] | Não | Contrato de integração externa; requer decisão de arquitetura |
| 2 | [Backend] Mapear cenários de resposta | Backend | [Xh] | Parcial | Regra com impacto de negócio; checkpoint humano |
| 3 | [Frontend] Feedback visual do resultado | Frontend | [Xh] | Sim | UI com design system |
| 4 | [Teste] Testes com mock do provider | Backend | [Xh] | Parcial | Estrutura padrão, cenários específicos |
```

---

## Exemplo: História de UI/Frontend

```markdown
### [EPIC-Z] US-020: Dashboard de [indicadores do domínio]

**Tipo:** Story
**Épico:** [Nome do Épico]
**Sprint:** Bolt N
**Componente:** Frontend
**Prioridade (MoSCoW):** Should Have · Priority: High
**Story Points:** [N] — múltiplos componentes visuais e dados agregados
**Dependências:** [US-YYY — API de indicadores]

#### Rastreabilidade (vault)
- SPEC: `04_desenvolvimento/specs/SPEC_{FUNCIONALIDADE}.md`
- Design: `DESIGN.md` — Jornada Dashboard
- Métricas: `_metrics/METRICAS_SUCESSO_INICIAIS.md`

#### Descrição
Como um **[persona]**, eu quero ver **[indicadores]** em um dashboard para [objetivo de acompanhamento].

Indicadores alinhados aos OKRs do projeto, conforme `_metrics/`.

#### Tarefas Técnicas (Subtasks)

| # | Tarefa | Componente | Estimativa | Elegível IA? | Justificativa |
|---|--------|------------|------------|--------------|---------------|
| 1 | [Frontend] Layout responsivo do dashboard | Frontend | [Xh] | Sim | Layout com design system |
| 2 | [Frontend] Componente de indicador | Frontend | [Xh] | Sim | Componente reutilizável simples |
| 3 | [Frontend] Gráfico(s) | Frontend | [Xh] | Sim | Dados formatados, lib aprovada |
| 4 | [Backend] Endpoint REST de resumo | Backend | [Xh] | Sim | Query agregada, padrão REST |
| 5 | [Teste] Unitários de renderização | Frontend | [Xh] | Sim | Testes padrão |
```

---

## Formato Compacto para Criação Rápida de História no Jira

Quando solicitado, gere um formato enxuto para copy-paste direto na história do Jira (sintaxe wiki):

```
---
**Summary:** [EPIC-X] US-YYY: Título
**Issue Type:** Story
**Epic Link:** Nome do Épico
**Sprint:** Bolt N
**Priority:** Highest | High | Medium | Lowest
**Story Points:** N
**Component/s:** Backend | Frontend | Fullstack | Infra
**Labels:** ai-eligible | ai-partial | ai-manual
**Linked Issues:** is blocked by US-NNN (se houver)

**Description:**

_Rastreabilidade (vault):_
- SPEC: specs/SPEC_{FUNCIONALIDADE}.md
- Refinamento: 02_discovery/refinamentos/REFINAMENTO_{X}.md
- Design: DESIGN.md — Jornada {X}

Como [persona], eu quero [ação] para [benefício].

[Contexto e regras de negócio]

h3. Critérios de Aceite

{code:gherkin}
Cenário: ...
  Dado ...
  Quando ...
  Então ...
{code}

h3. Notas Técnicas
[Padrões, NFRs e regras de segurança do AGENT_RULES.md]

*Subtasks:*
1. [Componente] Tarefa — Xh — IA: Sim/Parcial/Não
---
```

---

## Checklist de Qualidade do Backlog

Antes de entregar o backlog, verifique:

- [ ] Toda história aponta para SPEC e DOCUMENTO DE REFINAMENTO (rastreabilidade vault ↔ Jira ↔ GitHub)
- [ ] Nenhuma funcionalidade entra em sprint/bolt sem SPEC
- [ ] Todo critério de aceite está em BDD/Gherkin, testável sem perguntas
- [ ] Toda tarefa tem nível de autonomia AI-DLC (Sim/Parcial/Não) com justificativa
- [ ] Dependências mapeadas como Linked Issues (is blocked by), sem ciclos
- [ ] Story points em Fibonacci (1, 2, 3, 5, 8, 13); nenhuma história com 13 (quebrar)
- [ ] Prioridade MoSCoW mapeada para o campo Priority do Jira
- [ ] Componentes corretos no campo Component/s (Backend/Frontend/Fullstack/Infra)
- [ ] DoD alinhado à FASE 4 (DEV, cobertura, build limpo, review cruzado, validação do designer)
- [ ] Regras de negócio e de UI específicas do projeto respeitadas, conforme `AGENT_RULES.md`
- [ ] Riscos associados verificados no REGISTRO DE RISCOS
- [ ] Perguntas em aberto listadas separadamente (não preencher com suposições)
- [ ] Sugestão de ordem de sprint/bolt coerente com dependências

---

## Adaptações ao Dojo (mantendo o Jira)

- **Três camadas:** o **Jira** segue como ferramenta de gestão do backlog (épicos, histórias, subtasks, sprints); o **GitHub** é a execução de código (branches, commits, PRs, releases); o **vault** é a memória e fonte de verdade.
- **Sprints = Bolts:** cada sprint do Jira corresponde a um **bolt** (ciclo semanal do AI-DLC).
- **Rastreabilidade tripla:** toda história do Jira liga-se aos artefatos do vault (SPEC, refinamento, `CONTEXT.md`, riscos) e ao PR do GitHub; a chave da história (ex.: `{PROJETO}-123`) aparece na branch/commit.
- **Elegibilidade IA:** reinterpretada como nível de autonomia do agente no AI-DLC, com checkpoints humanos obrigatórios em pontos críticos.
- **Definição de Pronto:** alinhada aos critérios da FASE 4 (publicação em DEV, build limpo, code review cruzado por segundo agente, validação do designer via `DESIGN.md`).
- **Idioma:** artefatos em português, salvo indicação diferente do projeto.
