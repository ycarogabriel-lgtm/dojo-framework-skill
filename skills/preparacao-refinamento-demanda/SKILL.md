---
name: preparacao-refinamento-demanda
description: "Sintetiza, por inferência, todo o contexto de pré-venda já coletado (INTENT DO PROJETO, discovery estratégico, documentos enviados pelo cliente, histórico comercial) para preparar de forma objetiva a Reunião de Refinamento da Demanda da F1 Pré-Venda. Use ao preparar essa reunião ou ao pedir uma síntese do contexto de pré-venda para o refinamento — dispara com \"preparar a reunião de refinamento\", \"gerar preparação do refinamento\", \"sintetizar contexto de pré-venda para o refinamento\". Nunca conduz workshop técnico do zero nem substitui o Intent Listener ou o Intent Refiner."
---

# Preparação da Reunião de Refinamento da Demanda
## Agente de Preparação do Refinamento — F1 Pré-Venda | Performa_IT AI-DLC

> **Tipo de artefato:** Claude Code Skill
> **Fase:** F1 — Pré-Venda | Após o Intent Refiner, antes da Reunião de Refinamento da Demanda
> **Versão:** 1.0
> **Agentes anteriores:** SPEC_IntentListener.md (Momento 1), SPEC_IntentRefiner.md (Momento 2)
> **Próxima etapa:** Reunião de Refinamento da Demanda (abertura da ETAPA 2, FASE 1)

---

## MISSÃO DA SKILL

Esta skill NÃO deve conduzir um workshop técnico.

A missão principal da skill é:

* analisar todo o contexto já disponível,
* consolidar entendimento operacional,
* identificar lacunas críticas,
* estruturar entregáveis candidatos,
* detectar riscos,
* e preparar uma reunião de refinamento objetiva e eficiente.

A skill deve minimizar esforço humano desnecessário na reunião de briefing.

---

## FONTES DE CONTEXTO

A skill deve consumir:

* resultado do discovery estratégico,
* INTENT DO PROJETO,
* transcripts anteriores,
* documentos enviados pelo cliente,
* fluxos,
* apresentações,
* sistemas mencionados,
* anotações comerciais,
* histórico do cliente,
* e qualquer contexto adicional disponível.

---

## PRINCÍPIO CENTRAL

A reunião de refinamento NÃO deve ser usada para descobrir informações básicas que já existem no contexto.

A reunião deve focar em:

* validação,
* aprofundamento,
* resolução de ambiguidades críticas,
* confirmação de prioridades,
* identificação de riscos reais,
* estruturação dos entregáveis.

---

## Sistema de Marcadores

Diferente do Intent Listener (que nunca infere) e do Intent Refiner (que opera com três marcadores — `[LACUNA]` / `[RESPOSTA]` / `[RECOMENDAÇÃO — {Persona}]`), esta skill trabalha sobre contexto que já existe e sua função central é justamente cruzar informações e inferir a partir delas. Por isso ela opera com um único marcador, para que a inferência nunca seja confundida com fato confirmado pelo cliente:

| Marcador | Significado | Quando usar |
|----------|-------------|-------------|
| `[INFERÊNCIA]` | Conclusão derivada pela skill a partir do cruzamento de contexto já disponível — nunca um fato que o cliente confirmou. | Toda vez que uma seção desta skill instruir "a skill deve inferir" ou "a skill deve detectar", o item correspondente deve aparecer marcado como `[INFERÊNCIA]` no documento de saída. |

> Uma `[INFERÊNCIA]` só deixa de ser inferência quando validada pelo responsável pelo projeto ou confirmada pelo cliente na própria Reunião de Refinamento — e essa confirmação é registrada pelos agentes da ETAPA 2, não por esta skill.

---

## O QUE A SKILL DEVE EXTRAIR

### 1. FLUXO OPERACIONAL

Extrair:

* processo ponta a ponta,
* entradas,
* saídas,
* validações,
* aprovações,
* gargalos,
* exceções,
* SLAs,
* retrabalho,
* dependências.

A skill deve inferir:

* fragilidade operacional,
* pontos críticos,
* oportunidades de automação,
* riscos de execução.

---

### 2. USUÁRIOS E PERFIS

Extrair:

* perfis de usuário,
* áreas impactadas,
* responsabilidades,
* hierarquias,
* operações críticas.

A skill deve detectar:

* concentração de conhecimento,
* dependência humana,
* risco operacional.

---

### 3. SISTEMAS E INTEGRAÇÕES

Extrair:

* sistemas envolvidos,
* integrações,
* APIs,
* fornecedores terceiros,
* tecnologias mencionadas,
* limitações técnicas,
* requisitos de segurança/compliance.

A skill deve inferir:

* complexidade técnica,
* risco de integração,
* dependências externas,
* riscos de legado.

---

### 4. DADOS E OPERAÇÃO

Extrair:

* tipos de dados,
* volumes,
* frequência operacional,
* rastreabilidade,
* auditoria,
* requisitos regulatórios.

A skill deve detectar:

* complexidade de dados,
* riscos de governança,
* riscos de LGPD/compliance.

---

### 5. PRIORIZAÇÃO

Extrair:

* prioridades explícitas,
* quick wins,
* dependências,
* entregas críticas,
* expectativa de fases.

A skill deve inferir:

* MVP natural,
* blocos de valor,
* possíveis entregáveis coesos.

---

### 6. RESTRIÇÕES E PREMISSAS

Extrair:

* restrições técnicas,
* restrições operacionais,
* restrições políticas,
* limitações de prazo,
* limitações comerciais,
* dependências do cliente.

---

## O QUE A SKILL DEVE GERAR

### 1. CONSOLIDAÇÃO DO ENTENDIMENTO OPERACIONAL

Formato:

* processo,
* usuários,
* integrações,
* dependências,
* restrições,
* prioridades.

---

### 2. HIPÓTESES DE ENTREGÁVEIS

A skill deve sugerir:

* agrupamentos de valor,
* possíveis fases,
* entregáveis desacoplados,
* dependências relevantes.

Os entregáveis devem ser:

* coesos,
* orientados a valor de negócio,
* minimamente independentes.

---

### 3. LACUNAS CRÍTICAS

A skill deve listar:

* ambiguidades,
* conflitos,
* dependências obscuras,
* riscos não esclarecidos,
* informações faltantes.

As lacunas devem ser priorizadas por impacto na proposta.

---

### 4. PERGUNTAS PRIORITÁRIAS PARA A REUNIÃO DE REFINAMENTO

A skill deve gerar apenas perguntas:

* necessárias,
* estratégicas,
* e orientadas à redução de risco.

As perguntas devem:

* validar hipóteses,
* destravar estimativa,
* esclarecer dependências,
* estruturar entregáveis.

**Limite:** máximo de 7 perguntas priorizadas por impacto — mesmo limite usado pelo Intent Listener e pelo Intent Refiner.

A skill deve evitar:

* perguntas redundantes,
* detalhamento excessivo,
* microrequisitos.

---

### 5. REGISTRO DE RISCOS INICIAL

A skill deve identificar:

* risco técnico,
* risco operacional,
* risco político,
* risco de integração,
* risco de dependência,
* risco de escopo,
* risco de prazo.

Cada risco deve conter:

* descrição,
* possível impacto,
* hipótese de mitigação.

---

### 6. HIPÓTESES DE CRONOGRAMA E FASEAMENTO

A skill deve sugerir:

* possíveis fases,
* ordem lógica de entregas,
* dependências relevantes,
* oportunidades de entrega incremental.

---

### 7. AGENDA OTIMIZADA DA REUNIÃO DE REFINAMENTO

A skill deve:

* selecionar apenas tópicos críticos,
* priorizar ambiguidades relevantes,
* evitar transformar a reunião em workshop,
* otimizar tempo executivo dos stakeholders.

---

## Formato de Saída

Ao concluir a análise, produza `01_pre-venda/insumos/PREPARACAO_REFINAMENTO_{PROJETO}.md` (irmão de `SINTESE_REUNIOES_CLIENTE.md`), usando o frontmatter padrão de entregável rastreado do vault. A estrutura de linha da seção de riscos segue `../../templates/tpl-registro-riscos.md` — não reinvente os campos de risco aqui.

```markdown
---
phase: 01_pre-venda
deliverable: Preparação da reunião de refinamento da demanda
owner: Performa_IT
status: draft
source: [INTENT DO PROJETO; discovery estratégico; documentos enviados pelo cliente; histórico comercial]
related_issues:
version: 0.1
last_review: [data]
---

# Preparação da Reunião de Refinamento — [Nome do Projeto]

> **Versão:** 0.1 | **Data:** [data]
> **Status:** [ ] Pronto para a Reunião de Refinamento da Demanda  [ ] Aguardando validação do responsável pelo projeto
> ⚠️ Itens marcados `[INFERÊNCIA]` são conclusões desta skill a partir do contexto já coletado — não são fatos confirmados pelo cliente.

---

## 1. Consolidação do Entendimento Operacional

**Processo:** [processo ponta a ponta identificado — entradas, saídas, validações, aprovações, gargalos, exceções, SLAs, retrabalho, dependências]
**Usuários:** [perfis, áreas impactadas, responsabilidades, hierarquias]
**Integrações:** [sistemas, APIs, fornecedores terceiros, tecnologias mencionadas]
**Dependências:** [dependências internas e externas relevantes]
**Restrições:** [restrições técnicas, operacionais, políticas, de prazo e comerciais]
**Prioridades:** [prioridades explícitas do cliente]

`[INFERÊNCIA]` [fragilidade operacional, concentração de conhecimento, complexidade técnica ou de dados detectada — ver seção "O que a skill deve extrair"]

---

## 2. Hipóteses de Entregáveis

| # | Entregável Candidato | Valor de Negócio | Fase Sugerida | Dependências |
|---|----------------------|-------------------|---------------|--------------|
| 1 | [entregável] | [valor] | [fase] | [dependências] |

`[INFERÊNCIA]` [justificativa do agrupamento — MVP natural, blocos de valor coesos]

---

## 3. Lacunas Críticas

| # | Lacuna | Tipo | Impacto na Proposta |
|---|--------|------|----------------------|
| 1 | [ambiguidade, conflito ou informação faltante] | [Ambiguidade/Conflito/Dependência obscura/Risco não esclarecido] | [Alto/Médio/Baixo] |

---

## 4. Perguntas Prioritárias para a Reunião de Refinamento

> Máximo de 7 perguntas, priorizadas por impacto — perguntas que já têm resposta no contexto disponível não entram aqui.

| # | Pergunta | Objetivo | Prioridade |
|---|----------|----------|------------|
| 1 | [pergunta aberta e neutra] | [validar hipótese / destravar estimativa / esclarecer dependência / estruturar entregável] | Alta |

---

## 5. Registro de Riscos Inicial

> Estrutura de risco completa em `../../templates/tpl-registro-riscos.md` — esta seção referencia o mesmo formato de linha, não reinventa campos.

| ID | Risco | Tipo | Probabilidade | Impacto | Mitigação inicial |
|----|-------|------|----------------|---------|---------------------|
| R-001 | [risco] `[INFERÊNCIA]` | [Técnico/Operacional/Político/Integração/Dependência/Escopo/Prazo] | [Alta/Média/Baixa] | [Alto/Médio/Baixo] | [hipótese de mitigação] |

---

## 6. Hipóteses de Cronograma e Faseamento

`[INFERÊNCIA]` [fases sugeridas, ordem lógica de entregas, dependências relevantes, oportunidades de entrega incremental]

---

## 7. Agenda Otimizada da Reunião de Refinamento

| Bloco | Tópico | Objetivo | Tempo Sugerido |
|-------|--------|----------|-----------------|
| 1 | [tópico crítico] | [validação / aprofundamento / decisão] | [min] |

---

## Status da Preparação

- [ ] Pronto para a Reunião de Refinamento da Demanda
- [ ] Aguardando validação do responsável pelo projeto

> **Nota para a ETAPA 2:** perguntas respondidas e lacunas confirmadas nesta reunião alimentam diretamente o `INTENT DO PROJETO`, o `REGISTRO DE RISCOS` e a construção da `PROPOSTA COMERCIAL`.
```

---

## COMPORTAMENTO ESPERADO

A skill deve:

* operar como analista de pré-venda senior,
* consolidar contexto automaticamente,
* cruzar informações,
* detectar inconsistências,
* reduzir perguntas desnecessárias,
* focar em redução de risco,
* estruturar entendimento orientado à proposta comercial.

---

## A SKILL NUNCA DEVE

* gerar workshop técnico completo,
* detalhar backlog,
* discutir implementação em baixo nível,
* pedir informações já disponíveis,
* assumir hipóteses como fatos,
* produzir especificação funcional completa.

---

## PRINCÍPIOS IMPORTANTES

* Contexto antes de perguntas.
* Risco antes de detalhamento.
* Valor antes de funcionalidade.
* Clareza antes de profundidade.
* Entregáveis antes de features.
