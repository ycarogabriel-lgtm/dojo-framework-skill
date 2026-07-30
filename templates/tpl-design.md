---
phase: 02_discovery
deliverable: Design System do projeto (tokens e racional)
owner: [designer responsável]
status: draft
source: [design-md-draft.md revisado; design system em arquivo / brand book / site de referência / transcrição de reunião / referências visuais]
related_issues:
version: 0.1
last_review: [data]
---

> **Nota sobre as duas camadas de front matter deste arquivo:** o bloco YAML acima é o front matter de rastreamento do Dojo Framework (fase, dono, status, versão) — usado para governança do vault, igual a qualquer outro artefato rastreado. O DESIGN.md real do projeto, gerado pela skill `design-md-generator`, contém um SEGUNDO bloco YAML — mostrado logo abaixo como bloco de código `yaml` — que é o front matter definido pelo spec design.md (tokens machine-readable: cores, tipografia, arredondamento, espaçamento, componentes). Ao gerar o DESIGN.md definitivo do projeto, esse segundo bloco vira o front matter real do arquivo (não um bloco de código) — ele é representado aqui como código apenas porque um mesmo arquivo Markdown não pode ter duas seções de front matter `---` sequenciais. Os dois blocos servem propósitos diferentes e não devem ser fundidos.

# DESIGN.md — [Nome do Projeto]

Documento formatado para consumo direto por agentes de código (Claude Code, Cursor, v0, Stitch) durante a implementação — gerado pela skill `design-md-generator` (ver `skills/design-md-generator/SKILL.md`). Documenta a **intenção e o rationale** das decisões que o Design System do projeto já tomou; não define o DS nem toma decisões de design em nome do time.

Este documento é o Design System do projeto como um todo — criado uma vez a partir do "DESIGN SYSTEM inicial" da Etapa 2 de `assets/FASE 2 - DISCOVERY.md` e atualizado incrementalmente conforme novas jornadas são prototipadas, em vez de recriado do zero por jornada. Cada jornada prototipada referencia os tokens e componentes definidos aqui na sua própria tabela "Componentes do Design System utilizados".

**Onde este arquivo vive:** a cópia operacional (consumida em tempo real pelos agentes de FASE 4) fica na raiz do repositório de código. Esta cópia, aqui no vault em `02_discovery/design-system/DESIGN.md`, é a fonte rastreável/de governança — mantenha as duas sincronizadas; em caso de divergência, esta é a autoritativa.

## Front matter de tokens (machine-readable)

```yaml
---
version: alpha
name: [nome do projeto]
description: [descrição opcional]
colors:
  [token-name]: "[hex]"
typography:
  [token-name]:
    fontFamily: [string]
    fontSize: [Dimension]              # px, em, rem
    fontWeight: [number]               # numérico: 400, 600, 700 — não string
    lineHeight: [Dimension | number]   # unitless recomendado: 1.5
    letterSpacing: [Dimension]         # opcional
rounded:
  [scale-level]: [Dimension]           # ex: sm: 4px / md: 8px / full: 9999px
spacing:
  [scale-level]: [Dimension | number]  # number = razão ou contagem de colunas
components:                           # opcional — apenas se o DS define tokens de componente
  [component-name]:
    backgroundColor: [Color | {path.to.token}]
    textColor: [Color | {path.to.token}]
    typography: [{path.to.token}]
    rounded: [Dimension | {path.to.token}]
    padding: [Dimension]
    size: [Dimension]
    height: [Dimension]
    width: [Dimension]
  [component-name]-hover:               # variantes de estado como chaves separadas
    backgroundColor: [Color | {path.to.token}]
---
```

## Overview

[Personalidade, público, resposta emocional desejada. Texto autoral validado pelo designer — funciona como fallback de decisão do agente quando não há token ou regra explícita para o caso.]

## Colors

> Uma linha por token, com papel semântico e contexto de uso declarado pelo DS. Não renomear os tokens para se conformar a convenções externas.

| Token (nome do DS) | Hex | Papel / contexto de uso |
|---|---|---|
| [nome exato do DS] | #XXXXXX | [papel e onde é usado] |

**Contraste (APCA):** [Limiares Lc adotados e origem da decisão — se definida pelo DS, referenciar a decisão; se estabelecida neste documento, sinalizar explicitamente como decisão tomada aqui. Ver algoritmo APCA em `skills/design-md-generator/SKILL.md`.]

## Typography

> Por nível do DS, com justificativa de uso — não apenas os valores.

| Token (nome do DS) | Fonte | Tamanho | Peso (número) | Line-height | Papel e justificativa de uso |
|---|---|---|---|---|---|
| [nome do DS] | | | | | |

## Layout

[Grid, escala de espaçamento, breakpoints, densidade e estratégia responsiva, com contexto de uso.]

## Elevation & Depth

[Estratégia — sombra / flat / tonal — com justificativa. Se flat, descrever a alternativa (contraste de superfície, bordas sutis, escala de cor).]

## Shapes

[Linguagem de formas e o que ela comunica sobre o produto, seguida dos valores de border-radius por tipo de elemento — botão, card, input, badge, modal, pill.]

## Components

> Omitir esta seção se o DS não define tokens de componente. Incluir variantes de estado (hover, active, disabled, focus, error) como entradas separadas.

[Componentes-chave com os tokens mapeados no front matter acima.]

## Do's and Don'ts

> Formato de tabela — mínimo 4 linhas em cada coluna. Incluir obrigatoriamente: decisão de contraste APCA, uso de emoji, biblioteca de ícones.

| Do | Don't |
|---|---|
| [sempre fazer] | [nunca fazer] |

## Agent Prompt Guide

> Seção opcional — incluir quando o DESIGN.md for lido por Claude Code, Cursor ou agente similar.

**Exemplos de prompt de componente:**
- [Ex: "Crie um botão primário usando o token de ação e o radius do DS"]

**Guia de iteração:**
1. [Passo a passo de como o agente deve iterar sobre um componente sem ambiguidade]
