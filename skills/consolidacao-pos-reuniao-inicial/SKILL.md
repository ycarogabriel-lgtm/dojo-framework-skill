---
name: consolidacao-pos-reuniao-inicial
description: "Use após a Demanda Inicial (Reunião 1 da FASE 1 - PREVENDA) para consolidar transcript, notas e observações do primeiro contato com o cliente em memória operacional estruturada de pré-venda: contexto do cliente, resumo estratégico, hipóteses estratégicas, lacunas de entendimento, log de decisões, análise de go/no-go, nível de confiança do entendimento e pauta da Refinamento da Demanda (Reunião 2). Alimenta o Passo 1 do Intent Listener — não o substitui, nem substitui o Persona Generator ou o Intent Refiner. Dispara com \"consolidar a reunião inicial\", \"consolidar a demanda inicial\", \"gerar contexto pós-reunião\", \"preparar a refinamento da demanda\", \"montar a pauta da reunião 2\", \"avaliar go/no-go da oportunidade\", \"qual o nível de confiança do que entendemos até aqui\"."
---

# Consolidação de Contexto Estratégico Pós-Reunião Inicial

## Missão da Skill

A missão desta skill é transformar a primeira conversa com o cliente em memória operacional estruturada para o AI-DLC.

Esta skill deve ser utilizada quando:

* a reunião realizada foi a **Demanda Inicial** — a PRIMEIRA interação relevante com o cliente,
* existe pouco ou nenhum contexto prévio,
* e a conversa precisa ser consolidada em artefatos reutilizáveis para continuidade da pré-venda.

A skill deve:

* consolidar o transcript da reunião,
* estruturar entendimento estratégico,
* identificar dores,
* detectar riscos,
* estruturar hipóteses,
* reduzir ambiguidades,
* preparar a Reunião 2 — Refinamento da Demanda,
* e gerar memória persistente do cliente.

---

## Papel da Skill no AI-DLC

Esta skill atua no fluxo:

```text
DEMANDA INICIAL (Reunião 1 — FASE 1 - PREVENDA, Etapa 1)
↓
[SKILL] CONSOLIDAÇÃO DE CONTEXTO ESTRATÉGICO PÓS-REUNIÃO INICIAL
↓ (alimenta o Passo 1 do Intent Listener — ver SPEC_IntentListener.md, SPEC_PersonaGenerator.md, SPEC_IntentRefiner.md)
OUTPUTS ESTRUTURADOS DE PRÉ-VENDA
↓
REFINAMENTO DA DEMANDA (Reunião 2 — FASE 1 - PREVENDA)
```

Ela funciona como:

* consolidadora de contexto,
* analista de pré-venda,
* organizadora de memória,
* estruturadora de hipóteses,
* e preparadora do Refinamento da Demanda.

### Relação com os Agentes AI-DLC de Pré-Venda

Esta skill **não substitui** e **não compete com** a cadeia `SPEC_IntentListener.md` (Momento 1) → `SPEC_PersonaGenerator.md` (Momento 1.5) → `SPEC_IntentRefiner.md` (Momento 2). As duas coisas são complementares e operam na mesma janela da FASE 1 — entre a Demanda Inicial e a Refinamento da Demanda —, mas com papéis diferentes:

* O `CONTEXTO_CLIENTE_{PROJETO}.md`, o `RESUMO_ESTRATEGICO_{PROJETO}.md`, o `HIPOTESES_ESTRATEGICAS_{PROJETO}.md` e o `LACUNAS_ENTENDIMENTO_{PROJETO}.md` produzidos por esta skill são **insumo bruto** para o Passo 1 (Leitura e Extração) do Intent Listener — nunca o substituem, e nunca são tratados no vault como se já fossem o `RASCUNHO_INTENT.md`.
* O Intent Listener continua sendo o único agente que produz o `RASCUNHO_INTENT.md`; o Persona Generator continua sendo o único que produz `PERSONA_*.md`; o Intent Refiner continua sendo o único que produz o `INTENT_REFINADO.md`.
* O `GO_NO_GO_{PROJETO}.md`, o `NIVEL_CONFIANCA_{PROJETO}.md`, o `LOG_DECISOES_{PROJETO}.md` e o `PAUTA_REFINAMENTO_DEMANDA_{PROJETO}.md` são artefatos **sem equivalente** na cadeia Intent Listener/Persona Generator/Intent Refiner — cobrem a camada de qualificação comercial da oportunidade (viabilidade, confiança, decisões e pauta da próxima reunião), não a camada de captura de intent.

---

## Inputs da Skill

Sempre que existir, use como fonte factual primária `_assets/docs/<base> - Estruturado.md` (gerado pela skill `normalizacao-transcricao`) em vez de reprocessar a transcrição bruta — para não divergir de nomes e termos já normalizados no restante do vault. Se a Demanda Inicial ocorreu sem gravação ou transcrição formal (ex.: e-mail, reunião presencial sem ata), opere diretamente sobre notas e observações disponíveis e registre essa exceção no relatório final.

### Obrigatórios

* transcript da reunião (ou `_assets/docs/<base> - Estruturado.md`, quando existir),
* notas da reunião,
* observações do consultor/comercial.

### Opcionais

* gravação resumida,
* documentos enviados durante a reunião,
* apresentações,
* e-mails,
* screenshots,
* links compartilhados,
* materiais institucionais.

---

## Princípio Central

A primeira reunião gera contexto bruto.

A missão da skill é:

* transformar conversa em estrutura,
* transformar sinais em entendimento,
* transformar hipóteses em memória operacional,
* e transformar ambiguidades em backlog de refinamento.

---

## Objetivos da Skill

A skill deve:

* consolidar entendimento estratégico,
* estruturar dores e impactos,
* identificar stakeholders,
* detectar riscos,
* inferir entregáveis candidatos,
* identificar lacunas,
* estruturar insumos para o RASCUNHO_INTENT do Intent Listener,
* preparar a Refinamento da Demanda,
* e avaliar viabilidade da oportunidade.

---

## O que a Skill Deve Extrair

Toda inferência produzida nesta seção é provisória, marcada `[INFERIDO]`, e nunca substitui o trabalho de espelho estrito que o Intent Listener realiza sobre o mesmo transcript (ver `SPEC_IntentListener.md`, seção "Restrições Absolutas") — as duas leituras coexistem, uma não invalida a outra.

### 1. Contexto do Negócio

Extrair:

* segmento,
* operação principal,
* áreas envolvidas,
* contexto estratégico,
* iniciativas relacionadas,
* momento da empresa,
* sinais de crescimento,
* transformação em andamento,
* pressões operacionais.

Inferir:

* maturidade operacional,
* maturidade digital,
* prioridades executivas,
* drivers estratégicos.

---

### 2. Problemas e Dores

Extrair:

* dores explícitas,
* dores implícitas,
* gargalos,
* retrabalho,
* processos manuais,
* dependências humanas,
* problemas recorrentes,
* limitações de escala.

Separar:

* sintomas,
* causas,
* consequências.

Classificar:

* operacional,
* financeiro,
* estratégico,
* tecnológico,
* organizacional.

---

### 3. Impactos

Extrair:

* impacto operacional,
* impacto financeiro,
* impacto em produtividade,
* impacto em SLA,
* impacto em governança,
* impacto em experiência,
* impacto em escala.

Inferir:

* urgência real,
* custo da inação,
* criticidade.

---

### 4. Processo Operacional Macro

Extrair:

* fluxo principal,
* áreas envolvidas,
* sistemas citados,
* operações manuais,
* aprovações,
* dependências,
* integrações mencionadas,
* gargalos percebidos.

A skill NÃO deve aprofundar microdetalhes nesta etapa.

---

### 5. Objetivos e Resultados Esperados

Extrair:

* objetivos explícitos,
* metas,
* expectativas,
* quick wins,
* percepção de sucesso,
* ganhos esperados.

Inferir:

* métricas de sucesso candidatas,
* indicadores relevantes.

---

### 6. Stakeholders

Extrair:

* sponsor,
* decisores,
* influenciadores,
* áreas impactadas,
* responsáveis operacionais,
* participantes relevantes.

Detectar:

* ausência de sponsor,
* desalinhamento,
* múltiplos decisores,
* riscos políticos.

---

### 7. Timeline e Prioridade

Extrair:

* urgência,
* prazos,
* restrições,
* eventos importantes,
* dependências externas.

Inferir:

* pressão política,
* risco de prazo,
* prioridade real.

---

### 8. Entregáveis Candidatos

A skill deve inferir:

* blocos coesos de valor,
* possíveis módulos,
* oportunidades de automação,
* integrações relevantes,
* quick wins,
* MVPs naturais.

Os entregáveis devem:

* ser desacopláveis,
* possuir propósito claro,
* permitir evolução incremental,
* ser orientados a valor.

---

## O que a Skill Deve Gerar

Os itens abaixo marcados com **Salvar em:** são artefatos rastreados do vault e levam o frontmatter padrão de deliverable de `01_pre-venda` (ver qualquer `templates/tpl-*.md`):

```yaml
---
phase: 01_pre-venda
deliverable: [nome do artefato]
owner: Performa_IT
status: draft
source: [transcript/notas da Reunião 1 — Demanda Inicial]
related_issues:
version: 0.1
last_review: [data]
---
```

Os demais itens (item 3 e os redirecionamentos dos itens 5 e 6) **não** geram arquivo próprio — ver a instrução específica de cada um.

### 1. Contexto Consolidado do Cliente

Arquivo: `CONTEXTO_CLIENTE_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/CONTEXTO_CLIENTE_{PROJETO}.md`

Ver também `templates/tpl-sintese-reunioes-cliente.md` — mesma família de conteúdo; esta versão cobre apenas a Demanda Inicial (Reunião 1), sem os "temas recorrentes" entre múltiplas entrevistas que a síntese de reuniões consolida mais adiante no discovery.

Conteúdo:

* contexto do negócio,
* estrutura organizacional,
* sistemas conhecidos,
* áreas envolvidas,
* stakeholders,
* histórico inicial,
* restrições percebidas.

---

### 2. Resumo Estratégico

Arquivo: `RESUMO_ESTRATEGICO_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/RESUMO_ESTRATEGICO_{PROJETO}.md`

Conteúdo:

* problema principal,
* dores,
* impactos,
* urgência,
* contexto consolidado,
* drivers estratégicos.

---

### 3. Insumos para o RASCUNHO_INTENT

Este conteúdo **não é salvo como arquivo próprio** e não é um deliverable rastreado independente. Ele é entregue como insumo bruto ao Passo 1 (Leitura e Extração) do Intent Listener (ver `SPEC_IntentListener.md`) — que é o único agente responsável por produzir o `RASCUNHO_INTENT.md` formal do projeto. Não nomeie, não versione e não trate este conteúdo como se fosse "o intent" do projeto.

Conteúdo a levantar (para entrega ao Intent Listener):

* propósito do projeto,
* problema principal,
* objetivos de negócio,
* resultado esperado,
* hipótese de solução,
* limites iniciais de escopo,
* stakeholders principais.

---

### 4. Hipóteses Estratégicas

Arquivo: `HIPOTESES_ESTRATEGICAS_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/HIPOTESES_ESTRATEGICAS_{PROJETO}.md`
Template: `templates/tpl-hipoteses-estrategicas.md`

Conteúdo:

* hipóteses de automação,
* hipóteses de IA,
* hipóteses de integração,
* hipóteses de gargalos,
* hipóteses de MVP,
* hipóteses de entregáveis.

Toda hipótese deve ser explicitamente marcada.

---

### 5. Métricas de Sucesso Iniciais

**Não criar arquivo próprio.** Popular/atualizar diretamente `_metrics/METRICAS_SUCESSO_INICIAIS.md`, usando `templates/tpl-metricas-sucesso.md` — não criar um arquivo `-v1` paralelo.

Conteúdo a extrair: métricas qualitativas, KPIs mencionados, ganhos esperados, indicadores candidatos — mapeados para as tabelas "Métricas recomendadas para a POC/MVP" e "Métricas candidatas para projeto completo" do template.

---

### 6. Riscos Estratégicos

**Não criar arquivo próprio.** Popular/atualizar diretamente `_risks/REGISTRO_RISCOS_INICIAL.md`, usando `templates/tpl-registro-riscos.md` — não criar um arquivo `-v1` paralelo.

Cada risco deve conter: descrição, impacto, nível percebido, categoria — mapeados para as colunas da tabela "Riscos" do template.

Categorias:

* político,
* operacional,
* comercial,
* integração,
* escopo,
* prioridade.

---

### 7. Lacunas de Entendimento

Arquivo: `LACUNAS_ENTENDIMENTO_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/LACUNAS_ENTENDIMENTO_{PROJETO}.md`
Template: `templates/tpl-lacunas-entendimento.md`

Cada lacuna deve conter:

**Prioridade**

* BLOCKER
* HIGH RISK
* IMPORTANT
* NICE TO HAVE

**Status**

* CONFIRMADO
* HIPÓTESE
* INFERIDO
* PENDENTE DE VALIDAÇÃO

A skill deve identificar:

* ambiguidades,
* conflitos,
* dependências obscuras,
* pontos não respondidos.

---

### 8. Log de Decisões

Arquivo: `LOG_DECISOES_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/LOG_DECISOES_{PROJETO}.md`
Template: `templates/tpl-log-decisoes.md`

Registrar:

* decisões explícitas,
* prioridades confirmadas,
* direcionamentos,
* restrições acordadas,
* mudanças relevantes de entendimento.

---

### 9. Análise de Go / No-Go

Arquivo: `GO_NO_GO_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/GO_NO_GO_{PROJETO}.md`
Template: `templates/tpl-go-no-go.md`

A skill deve recomendar:

* GO
* GO WITH CAUTION
* DISCOVERY PAGO NECESSÁRIO
* NO-GO

A decisão deve considerar:

* clareza,
* risco,
* complexidade,
* dependências,
* confiança da estimativa,
* alinhamento dos stakeholders.

Esta é uma recomendação estruturada para o responsável pelo projeto decidir — nunca uma decisão automática da skill.

---

### 10. Nível de Confiança do Entendimento

Arquivo: `NIVEL_CONFIANCA_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/NIVEL_CONFIANCA_{PROJETO}.md`
Template: `templates/tpl-confidence-score.md`

A skill deve atribuir:

* LOW
* MEDIUM
* HIGH

para:

* entendimento do problema,
* entendimento operacional,
* entendimento técnico,
* entendimento de integrações,
* entendimento organizacional.

---

### 11. Preparação da Reunião de Refinamento da Demanda

Arquivo: `PAUTA_REFINAMENTO_DEMANDA_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/PAUTA_REFINAMENTO_DEMANDA_{PROJETO}.md`
Template: `templates/tpl-pauta-refinamento-demanda.md`

Consolida três blocos internos num único artefato:

#### Foco do Refinamento da Demanda

Conteúdo:

* ambiguidades prioritárias,
* riscos que precisam aprofundamento,
* integrações críticas,
* stakeholders faltantes,
* pontos bloqueadores,
* tópicos obrigatórios da reunião.

#### Perguntas Prioritárias do Refinamento da Demanda

As perguntas devem:

* reduzir risco,
* destravar estimativa,
* validar entregáveis,
* esclarecer dependências,
* confirmar integrações,
* reduzir ambiguidades críticas.

A skill deve evitar:

* redundância,
* perguntas já respondidas,
* microdetalhamento técnico.

#### Pauta da Reunião de Refinamento da Demanda

Conteúdo:

* sequência ideal da conversa,
* tópicos obrigatórios,
* ambiguidades prioritárias,
* riscos relevantes,
* perguntas críticas,
* blocos de refinamento.

A pauta deve:

* caber entre 90–120 min,
* manter foco executivo,
* evitar workshop técnico profundo.

---

### 12. Diagrama Macro da Demanda

Arquivo: `DIAGRAMA_MACRO_{PROJETO}.md`
Salvar em: `01_pre-venda/qualificacao/DIAGRAMA_MACRO_{PROJETO}.md`

Corresponde ao output "Diagrama de entendimento macro da demanda" da FASE 1 - PREVENDA, Etapa 1.

Representar:

* atores,
* sistemas,
* áreas,
* fluxo principal,
* integrações,
* dependências,
* macroprocesso.

Pode usar:

* Mermaid,
* C4 simplificado,
* fluxograma textual.

---

## Comportamento Esperado

A skill deve:

* operar como analista de pré-venda senior,
* estruturar memória persistente,
* detectar inconsistências,
* inferir padrões,
* reduzir trabalho manual,
* minimizar perda de contexto,
* preparar continuidade da oportunidade.

---

## A Skill Nunca Deve

* assumir hipóteses como fatos,
* gerar backlog detalhado,
* definir implementação,
* produzir arquitetura final,
* aprofundar microrrequisitos,
* transformar levantamento em workshop técnico,
* substituir o Intent Listener, o Persona Generator ou o Intent Refiner — os outputs desta skill alimentam o Passo 1 desses agentes, nunca os substituem,
* gerar arquivos chamados `RASCUNHO_INTENT.md` ou `INTENT_REFINADO.md` — esses nomes são exclusivos do Intent Listener e do Intent Refiner,
* criar arquivos `-v1` paralelos onde já existe artefato do vault (`_risks/REGISTRO_RISCOS_INICIAL.md`, `_metrics/METRICAS_SUCESSO_INICIAIS.md`) — atualizar o existente.

---

## Classificação Obrigatória

Toda informação relevante deve ser marcada como:

* `[CONFIRMADO]`
* `[HIPÓTESE]`
* `[INFERIDO]`
* `[PENDENTE DE VALIDAÇÃO]`

### Equivalência com o Intent Listener / Intent Refiner

Esta skill mantém seu próprio vocabulário de marcadores — não é o mesmo sistema `[LACUNA]`/`[RESPOSTA]`/`[RECOMENDAÇÃO — {Persona}]` do Intent Listener e do Intent Refiner (ver `SPEC_IntentListener.md`, "Sistema de Marcadores" no `SPEC_IntentRefiner.md`). A tabela abaixo traduz um sistema no outro sempre que conteúdo desta skill precisar entrar no `RASCUNHO_INTENT.md`:

| Marcador desta skill | Equivalente no Intent Listener / Intent Refiner |
|---|---|
| `[CONFIRMADO]` | `[RESPOSTA]` |
| `[HIPÓTESE]` | `[RECOMENDAÇÃO — Analista de Pré-Venda]` |
| `[INFERIDO]` | `[RECOMENDAÇÃO — Analista de Pré-Venda]` (sem persona nomeada) |
| `[PENDENTE DE VALIDAÇÃO]` | `[LACUNA]` |

Ao alimentar o `RASCUNHO_INTENT.md`, traduza os marcadores conforme esta tabela — o Intent Listener nunca deve receber `[HIPÓTESE]` ou `[INFERIDO]` como se fossem `[RESPOSTA]`.

---

## Princípios Importantes

* Contexto antes de detalhamento.
* Hipóteses antes de conclusões.
* Impacto antes de funcionalidade.
* Entregáveis antes de features.
* Clareza antes de profundidade.
* Redução contínua de ambiguidade.
* Memória persistente como ativo estratégico.
