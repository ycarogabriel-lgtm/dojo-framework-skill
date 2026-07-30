---
phase: 01_pre-venda
deliverable: Entregáveis candidatos (pré-refinamento)
owner: Performa_IT
status: draft
source: [transcript Demanda Inicial; transcript Refinamento da Demanda]
related_issues:
version: 0.1
last_review: [data]
---

# Entregáveis Candidatos - [Nome do Projeto]

> Documento de trabalho, orientado a estimativa, produzido na ETAPA B da
> skill `cbs-completo` (ou pela skill `preparacao-refinamento-demanda`) —
> ver `skills/cbs-completo/SKILL.md`. Agrupa as funcionalidades levantadas
> nas conversas com o cliente em Épicos e Features candidatas, com
> profundidade suficiente para estimar horas FE/BE no CBS.
>
> **Não confundir com `tpl-funcionalidade.md`:** aquele template é o
> aprofundamento de **uma única** funcionalidade, produzido na FASE 2 —
> Discovery, **depois** do refinamento com o cliente, com Propósito, Persona,
> Regras de negócio, Permissões, Dados e Critérios de aceite testáveis. Este
> documento é anterior a isso: cobre **várias** features de uma vez, ainda em
> nível de pré-venda, e existe para dar insumo ao CBS (`templates/tpl-cbs.md`)
> e à seção "Entregáveis" de `templates/tpl-proposta-comercial.md` — não para
> orientar o desenvolvimento.

## Critérios de agrupamento

- Coesão funcional (mesma jornada de usuário ou módulo)
- Independência suficiente para entrega incremental
- Orientação a valor de negócio
- Granularidade: 1 Feature = 1 entregável testável pelo usuário

## Épicos e Features

### Épico 1: [Nome do Épico]

#### 1.1 — [Nome da Feature]

**Tipo:** [Nova | Ativa]
**Situação:** [Ativa]
**Descrição:** [O que entrega, fluxos principais, campos relevantes, regras de negócio]
**Observações:** [Dependências, riscos, integrações]
**Premissas:** [O que precisa ser verdadeiro para esta estimativa ser válida]

#### 1.2 — [Nome da Feature]

**Tipo:** [Nova | Ativa]
**Situação:** [Ativa]
**Descrição:** [O que entrega, fluxos principais, campos relevantes, regras de negócio]
**Observações:** [Dependências, riscos, integrações]
**Premissas:** [O que precisa ser verdadeiro para esta estimativa ser válida]

### Épico 2: [Nome do Épico]

#### 2.1 — [Nome da Feature]

**Tipo:** [Nova | Ativa]
**Situação:** [Ativa]
**Descrição:** [O que entrega, fluxos principais, campos relevantes, regras de negócio]
**Observações:** [Dependências, riscos, integrações]
**Premissas:** [O que precisa ser verdadeiro para esta estimativa ser válida]

## Integrações externas sinalizadas

- [Sistema/API] — [documentada? disponível? impacto na estimativa]

## Dependências entre Épicos/Features

- [Feature X depende de Feature Y — motivo]

## Próximo passo

Este documento alimenta diretamente a ETAPA C da skill `cbs-completo`
(geração do CBS — ver `templates/tpl-cbs.md`). Validar com o cliente antes de
consolidar a `PROPOSTA COMERCIAL`.
