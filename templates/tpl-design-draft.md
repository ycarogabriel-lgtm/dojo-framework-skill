---
phase: 02_discovery
deliverable: Rascunho do Design System do projeto (revisão do designer antes do DESIGN.md final)
owner: [designer responsável]
status: draft
source: [design system em arquivo (.json/.css/tokens/Tailwind) / brand book / site de referência / transcrição de reunião / referências visuais]
related_issues:
version: 0.1
last_review: [data]
---

# Draft para geração do DESIGN.md

> Revise todos os campos. Corrija o que estiver errado.
> Preencha os `[PENDENTE]`. Valide e reescreva os `[RASCUNHO-DESIGNER]` com sua voz.
> Devolva este arquivo revisado para que o DESIGN.md final seja gerado (ver `tpl-design.md`).

---

## Identidade do projeto

**Nome:** [EXTRAÍDO / PENDENTE]
**Descrição:** [EXTRAÍDO / PENDENTE]
**Agente principal de destino:** [PENDENTE — Claude Code / Cursor / v0 / Stitch / outro]
**DS em código já existe?** [EXTRAÍDO: sim — qual / não]
**Stack/framework:** [EXTRAÍDO / PENDENTE]

---

## Overview
> Esta seção é autoral — documenta a intenção e personalidade do produto.
> O rascunho abaixo foi gerado a partir dos insumos como ponto de partida.
> **Obrigatoriamente reescrita ou validada pelo designer antes de gerar o DESIGN.md.**

[RASCUNHO-DESIGNER]
_Base: [listar fontes usadas para gerar o rascunho]_

---

## Cores

> Os nomes de token abaixo espelham os nomes do DS do projeto.
> Não renomeie para se conformar a convenções externas.

| Token (nome do DS) | Hex | Papel / contexto de uso declarado | Status |
|---|---|---|---|
| [nome exato do DS] | #XXXXXX | [papel e onde é usado] | [EXTRAÍDO / INFERIDO / PENDENTE-INTENCIONALIDADE] |

**Contraste (APCA):**
> APCA (Accessible Perceptual Contrast Algorithm) é o padrão adotado em vez do WCAG 2.x.
> Razão: o WCAG 2.x usa uma fórmula de ratio linear derivada de pesquisas dos anos 80, que não modela
> corretamente a percepção humana em telas modernas — aprova combinações ilegíveis e reprova
> combinações que funcionam bem. O APCA produz valores Lc baseados em peso, tamanho e polaridade
> do texto, sendo muito mais preciso para decisões reais de design.
> Referência: https://www.myndex.com/APCA/

- DS define combinações de contraste validadas? [EXTRAÍDO: sim / não / PENDENTE]
- Se sim, documentar: [combinações e Lc mínimo adotado]
- Se não, o MD deve estabelecer os limiares. Proposta da skill para revisão do designer:
  - Texto corpo (≥16px, peso 400): Lc ≥ 75
  - Texto label (≥12px, peso 600): Lc ≥ 60
  - Texto grande / headline (≥24px, peso 700): Lc ≥ 45
  - [PENDENTE-DESIGNER: confirmar, ajustar ou substituir esses valores]

**Tema escuro:** [EXTRAÍDO / PENDENTE]
**Combinações proibidas identificadas nos insumos:** [EXTRAÍDO / PENDENTE]

---

## Tipografia

> Os nomes de nível abaixo espelham os nomes do DS.
> Acrescentar a justificativa de uso de cada nível — isso é o que diferencia o MD de uma tabela de tokens.

| Token (nome do DS) | Fonte | Tamanho | Peso (número) | Line-height | Papel e justificativa de uso | Status |
|---|---|---|---|---|---|---|
| [nome do DS] | | | | | | |

**Restrições tipográficas identificadas:** [EXTRAÍDO / PENDENTE]

---

## Layout

**Grid base:** [EXTRAÍDO / INFERIDO / PENDENTE]
**Container máximo:** [EXTRAÍDO / INFERIDO / PENDENTE]
**Densidade:** [INFERIDO / PENDENTE] — justificativa: [contexto do usuário, uso em campo, especialista, etc.]

| Breakpoint | Largura | Comportamento principal |
|---|---|---|
| Mobile | | |
| Tablet | | |
| Desktop | | |
| Wide | | |

**Estratégia responsiva:** [EXTRAÍDO / INFERIDO / PENDENTE]

---

## Elevation & Depth

**Estratégia:** [EXTRAÍDO: usa sombras / flat / tonal / PENDENTE]

| Token sombra (nome do DS) | Valor CSS | Papel e quando usar |
|---|---|---|
| | | |

**Alternativa à sombra (se flat):** [EXTRAÍDO / INFERIDO / PENDENTE]
_Ex: contraste de superfície, bordas sutis, escala de cor_

---

## Shapes

**Linguagem de formas:** [INFERIDO / PENDENTE]
_O que a linguagem de formas comunica sobre o produto (ex: angular = precisão técnica; arredondado = acolhedor)_

| Elemento | Token radius (nome do DS) | Valor | Justificativa |
|---|---|---|---|
| Botão | | | |
| Card / painel | | | |
| Input | | | |
| Badge / chip | | | |
| Modal | | | |
| Pill | | | |

---

## Componentes-chave

> Preencher apenas se o DS define tokens de componente.
> Variantes de estado (hover, active, disabled, focus, error) são chaves separadas no YAML.

| Componente | backgroundColor | textColor | typography | rounded | padding | Status |
|---|---|---|---|---|---|---|
| [nome]-default | | | | | | |
| [nome]-hover | | | | | | |
| [nome]-disabled | | | | | | |

---

## Do's and Don'ts

**Extraídos dos insumos:**
- Do: [EXTRAÍDO]
- Don't: [EXTRAÍDO]

**A confirmar / complementar:**
- Uso de emojis: [ ] Nunca [ ] Apenas em: ___________ [ ] Sim
- Biblioteca de ícones: [PENDENTE]
- Estilo de ícone: [ ] Outline [ ] Filled [ ] Duotone — justificativa: [PENDENTE]
- Restrições de acessibilidade específicas do contexto de uso: [PENDENTE]
  _Ex: usuários idosos, uso em campo, alta exposição à luz solar, operação com luvas_
- Algo que o agente nunca deve decidir sozinho neste produto: [PENDENTE]

---

## Agent Prompt Guide (opcional)

> Seção para uso quando o MD será lido por Claude Code, Cursor ou agente similar.
> Ajuda o agente a aplicar o sistema sem ambiguidade.

**Exemplos de prompt de componente:**
- [PENDENTE — designer preenche com exemplos do produto]
  _Ex: "Crie um botão primário usando o token de ação e o radius do DS"_

**Guia de iteração:**
1. [PENDENTE]
