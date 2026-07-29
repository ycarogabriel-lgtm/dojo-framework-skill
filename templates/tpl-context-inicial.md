---
phase: 04_desenvolvimento
deliverable: Contexto de desenvolvimento para agentes de IA
owner: Performa_IT
status: draft
source: [ex.: 01_pre-venda/intent/RASCUNHO_INTENT_{PROJETO}.md; entrevistas relevantes; _metrics/METRICAS_SUCESSO_INICIAIS.md]
related_issues:
version: 0.1
last_review: [data]
---

# CONTEXT.md — [Nome do Projeto]

> Rascunho criado para viabilizar a primeira POC/MVP. Ainda não passou por
> discovery completo (personas/jornadas formais) nem por arquitetura aprovada.
> Tratar como contexto de trabalho, não como baseline definitivo.

## Intent resumido

[2-4 frases: o que o projeto busca reduzir/aumentar/resolver, e para qual dor concreta. Apontar para o intent completo.]

## Escopo da POC/MVP

Foco: [o que exatamente está sendo automatizado/entregue nesta primeira fatia, e para qual usuário/persona].

Dentro do escopo:
- [item 1]
- [item 2]
- [item 3]

Fora do escopo (ver intent, seção de exclusões):
- [item explicitamente fora]
- [item explicitamente fora]

## Usuária/usuário de referência

[Persona principal, papel, e a dor concreta que hoje consome tempo/atenção dela — números aproximados quando existirem, ex.: "gasta ~1h por ciclo fazendo X manualmente".]

## Métricas de sucesso da POC/MVP (hipóteses, a validar com cliente)

Ver `_metrics/METRICAS_SUCESSO_INICIAIS.md`. Destaques usados para guiar a UI:
- [métrica 1]
- [métrica 2]

## Stack da POC/MVP

[Front-end/back-end/dados usados nesta fase — ser explícito sobre o que é mock e o que é real. Se o código vive em repositório separado do vault, citar o nome do repositório irmão aqui.]

## Lacunas conhecidas

[O que ainda não foi confirmado pelo cliente e que esse contexto assume como hipótese — apontar para a seção correspondente do intent.]

---

> **Nota para quando o projeto avançar para arquitetura/desenvolvimento pleno:**
> este CONTEXT.md tende a crescer com novas seções à medida que a arquitetura,
> os módulos, as integrações, os fluxos de navegação e o status de implementação
> ficam definidos (ex.: `## ARQUITETURA`, `## MÓDULOS`, `## INTEGRAÇÕES`,
> `## STATUS DE IMPLEMENTAÇÃO`). Essa evolução é orgânica e específica de cada
> projeto — não existe uma forma fixa para essas seções além do que a
> arquitetura aprovada do projeto realmente definir. Não adicione essas seções
> especulativamente; adicione-as quando o conteúdo real existir.
