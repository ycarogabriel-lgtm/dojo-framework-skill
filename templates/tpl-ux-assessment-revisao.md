---
phase: 02_discovery
deliverable: Documento de revisão da avaliação heurística de UX (gate de aprovação humana antes do XLSX/HTML finais)
owner: [responsável pela avaliação — Performa_IT]
status: draft
source: [screenshots reais das telas avaliadas; vídeos de walkthrough (opcional); fluxo Figma (opcional) — ver skills/ux-assessment-heuristico/references/captura_evidencias.md]
related_issues:
version: 0.1
last_review: [data]
---

# Documento de Revisão — UX Assessment [Produto] ([Cliente])

Gerado pela skill `ux-assessment-heuristico`, Etapa 3 (documento de revisão / gate humano). Este
documento **não é o entregável final** — é o ponto de aprovação antes de gerar a planilha XLSX e
o HTML final (`skills/ux-assessment-heuristico/SKILL.md`, seção "Os 3 entregáveis, na ordem
certa"). Toda avaliação registrada aqui deve estar ancorada em evidência real (screenshot, frame
de vídeo, medição de contraste) — nunca em achado genérico ou suposição.

## Contexto da avaliação

| Campo | Valor |
|---|---|
| Cliente | [nome do cliente] |
| Produto avaliado | [nome do produto/sistema] |
| Consultoria | [ex. Performa.it] |
| Avaliadores | [nome — papel — e-mail; um por linha] |
| Data da avaliação | [data ou período] |
| Público | [ex. operação e atendimento] |
| Telas avaliadas | [lista das telas cobertas nesta rodada] |

## Estrutura por tela

> Repita a seção abaixo (cabeçalho + as 5 tabelas de área) uma vez para cada tela avaliada. Cada
> linha das tabelas corresponde a uma avaliação criada pelo helper `R()` de
> `scripts/data_exemplo.py` — 3 critérios por área, 15 avaliações por tela no total, incluindo as
> marcadas "Nenhum" (sem quebra), que ficam registradas aqui mesmo sem entrar no HTML final.

### Tela: [Nome da Tela]

**Screenshot:** [caminho relativo para o arquivo de imagem real, ex. `./screenshots/dashboard.png` — nunca um placeholder]

**Erro% consolidado da tela:** [percentual] · **Nota total:** [valor] · **Critérios com problema:** [N] de [total]

#### Conteúdo

| Tema | Importância (0-3) | Quebra | Nota | Base teórica | Problema identificado | Solução proposta | Justificativa | Contraste medido (Lc) | Evidência narrada |
|---|---|---|---|---|---|---|---|---|---|
| [tema avaliado] | [0-3] | [Nenhum / Ruído / Obstáculo / Obstrução / Barreira] | [Importância × fator de Quebra] | [ex. Nielsen (1994) — Heurística N] | [descrição do problema, ou vazio se Quebra = Nenhum] | [solução recomendada, ou vazio se Quebra = Nenhum] | [por que essa Importância e esse fator de Quebra — nunca deixar em branco quando Quebra ≠ Nenhum] | [Lc medido via APCA, só quando o achado for de contraste/legibilidade] | ["trecho transcrito" — vídeo N, tela X, se houver] |

#### Arquitetura da Informação

| Tema | Importância (0-3) | Quebra | Nota | Base teórica | Problema identificado | Solução proposta | Justificativa | Contraste medido (Lc) | Evidência narrada |
|---|---|---|---|---|---|---|---|---|---|
| [tema avaliado] | [0-3] | [Nenhum / Ruído / Obstáculo / Obstrução / Barreira] | [Nota] | [base] | [problema] | [solução] | [justificativa] | [Lc] | [evidência] |

#### Design

| Tema | Importância (0-3) | Quebra | Nota | Base teórica | Problema identificado | Solução proposta | Justificativa | Contraste medido (Lc) | Evidência narrada |
|---|---|---|---|---|---|---|---|---|---|
| [tema avaliado] | [0-3] | [Nenhum / Ruído / Obstáculo / Obstrução / Barreira] | [Nota] | [base] | [problema] | [solução] | [justificativa] | [Lc — obrigatório quando o achado for de contraste/legibilidade, ver `references/apca_contraste.md`] | [evidência] |

#### Tecnologia

| Tema | Importância (0-3) | Quebra | Nota | Base teórica | Problema identificado | Solução proposta | Justificativa | Contraste medido (Lc) | Evidência narrada |
|---|---|---|---|---|---|---|---|---|---|
| [tema avaliado] | [0-3] | [Nenhum / Ruído / Obstáculo / Obstrução / Barreira] | [Nota] | [base] | [problema] | [solução] | [justificativa] | [Lc] | [evidência] |

#### Negócios

| Tema | Importância (0-3) | Quebra | Nota | Base teórica | Problema identificado | Solução proposta | Justificativa | Contraste medido (Lc) | Evidência narrada |
|---|---|---|---|---|---|---|---|---|---|
| [tema avaliado] | [0-3] | [Nenhum / Ruído / Obstáculo / Obstrução / Barreira] | [Nota] | [Framework próprio Performa.it — lente de negócio] | [problema] | [solução] | [justificativa] | [Lc, se aplicável] | [evidência] |

<!-- Repetir bloco "### Tela: [...]" acima para cada tela adicional avaliada -->

## Síntese de diagnóstico

> Sobre o produto como um todo, não a soma das telas isoladas — ver `references/metodo_pontuacao.md`,
> seção "Síntese de diagnóstico é sobre jornada, não só notas por tela".

**A ferramenta atual:** [existe uma jornada única que atravessa as telas avaliadas, ou cada tela é
um destino isolado? Nomeie explicitamente.]

**A necessidade do negócio:** [o que a operação/o negócio precisa que a ferramenta hoje não
entrega — vocabulário visual, confiabilidade percebida, continuidade de jornada, etc.]

**Erro% consolidado geral:** [percentual] (Importância total [valor] · Nota total [valor])

## Oportunidades já atendidas

- [funcionalidade ou fluxo que já funciona bem, como contraponto aos achados]

## Oportunidades não atendidas

- [lacuna real identificada, sem quebra associada a uma tela específica]

## Aprovação

| Campo | Valor |
|---|---|
| Status | [Pendente de revisão / Aprovado / Ajustes solicitados] |
| Revisado por | [nome de quem aprova] |
| Data da revisão | [data] |
| Ajustes solicitados | [lista de ajustes, se houver — a Etapa 4 (XLSX/HTML final) só começa após aprovação explícita] |
