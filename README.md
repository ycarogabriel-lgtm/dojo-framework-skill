# Dojo Framework Skill

Pacote genérico do **Dojo Framework** da Performa_IT: metodologia de projeto (pré-venda a AMS), gate de desenvolvimento, bootstrap de vault, detecção de tipo de workspace e oito skills auxiliares cobrindo pré-venda, discovery e desenvolvimento. Nenhum arquivo aqui menciona um cliente específico — isso é o que permite reusar o pacote em qualquer projeto novo sem contaminar o contexto do agente com dados de outro cliente.

## Por que este repositório existe

Antes deste pacote, a skill `dojo` (e as skills auxiliares) viviam duplicadas dentro de cada vault de cliente, copiadas manualmente projeto a projeto. Isso gerava contaminação cruzada real: uma skill copiada de um projeto trazia nomes de cliente, glossário e stack de um domínio completamente diferente, hardcoded no meio da lógica genérica — inclusive nomes reais de pessoas e de clientes distintos (confirmado em múltiplas skills durante a integração deste pacote). Este repositório é a fonte única e genérica; cada vault de cliente consome dele, nunca o contrário.

## Instalação

**Opção A — plugin (recomendado para o time, uso recorrente):** a partir de um checkout local deste repositório, ou depois de subi-lo para um remoto próprio (Bitbucket/GitHub):

```bash
claude plugin marketplace add /caminho/para/dojo-framework-skill
claude plugin install dojo-framework-skill@dojo-framework-skill
```

Uma vez instalado (a nível de usuário ou de projeto), a skill `dojo` — e as skills auxiliares — ficam disponíveis automaticamente em qualquer workspace, sem precisar copiar arquivos para dentro do repositório do cliente. Vantagem real sobre cópia manual: versionamento (bump no `plugin.json`, todo mundo atualiza) e instalação com um comando, sem precisar transferir arquivo nenhum manualmente uma vez que o repo esteja num remoto acessível ao time.

**Opção B — arquivo único (`.skill`), para compartilhamento pontual:** este repositório também pode ser exportado como um `.zip` renomeado para `.skill` (ex. `dojo-framework.skill`) — não é um formato oficial do Claude Code, só uma convenção de nome para deixar claro o que é o arquivo. Quem recebe extrai o zip e usa como plugin local (opção A) ou copia manualmente as pastas de `skills/` para dentro de `.claude/skills/` do próprio vault. Útil antes de existir um remoto compartilhado com o time.

Alternativa sem plugin nem zip: copiar manualmente a pasta de uma skill (ex. `skills/dojo/`) para `.claude/skills/dojo/` (e, se o time também usa Codex, para `.agents/skills/dojo/`) dentro do vault do cliente.

## O que está aqui

| Pasta | Conteúdo |
|---|---|
| `skills/dojo/` | Metodologia central: mapa de fases, gate de desenvolvimento, detecção de tipo de workspace (`workspace-detection.md`) e bootstrap de projeto novo (`project-bootstrap.md`). |
| `skills/consolidacao-pos-reuniao-inicial/` | Consolida a Demanda Inicial (1ª reunião) em memória operacional de pré-venda: contexto do cliente, hipóteses estratégicas, lacunas, log de decisões, análise de go/no-go e nível de confiança, além de preparar a pauta da Refinamento da Demanda. Complementar ao Intent Listener/Persona Generator/Intent Refiner, não um substituto. |
| `skills/preparacao-refinamento-demanda/` | Sintetiza o contexto de pré-venda já coletado (INTENT DO PROJETO, discovery, histórico do cliente) para preparar objetivamente a reunião de Refinamento da Demanda. |
| `skills/cbs-completo/` | Orquestrador fino que encadeia as duas skills acima e adiciona a análise de navegação de telas + geração do CBS (Cost Breakdown Structure): CSV de horas FE/BE pronto para embasar a proposta comercial. Estima na régua **IA-DLC** — ver a nota abaixo. |
| `skills/design-md-generator/` | Gera o `DESIGN.md` do projeto (Design System em tokens machine-readable + racional) referenciado pela FASE 2 (Etapa 4) e por `templates/tpl-design.md`. |
| `skills/ux-assessment-heuristico/` | Avaliação heurística de UX de um produto existente: pontuação por 5 áreas fixas, matriz de risco 2×2, e os 3 entregáveis sequenciais (revisão em Markdown → matriz XLSX → HTML final), com gate de aprovação humana entre eles. |
| `skills/normalizacao-transcricao/` | Converte transcrição bruta de reunião (Teams, `.docx`/`.txt`) no documento estruturado padrão do vault. |
| `skills/geracao-backlog/` | Estrutura refinamentos e SPECs como histórias de backlog rastreáveis (Jira), com elegibilidade AI-DLC. |
| `skills/geracao-ata-reuniao/` | Converte o documento estruturado de uma reunião em ATA executiva (`.docx`). |
| `templates/` | Ver tabela abaixo. |
| `assets/` | Guias de fase (FASE 1–4), specs dos agentes AI-DLC de pré-venda (Intent Listener/Refiner, Persona Generator) e config genérica do Obsidian (`obsidian-config/`). |
| `docs/adr/` | Decisões de arquitetura **do próprio framework** (não de projeto de cliente) — o porquê de mudanças estruturais no pacote. |

## Régua de estimativa do CBS (a partir da v0.2.0)

O CBS deixou de usar uma tabela plana rotulada "com IA" e passou a estimar por um **modelo de alavancagem explícito**: cada tipo de tela/operação tem uma coluna `Base` (convencional) e uma coluna `IA-DLC`, com o fator entre elas visível na própria linha. O fator varia por categoria de trabalho — de **0,35×** onde a IA colapsa o esforço (auth, CRUD, formulário, listagem) a **0,75×** onde o gargalo é externo e empírico (migração de dados, integração complexa com terceiro) — em vez de um desconto único e opaco.

Três guardas acompanham a régua nova: um **fator de reúso** (o 4º componente do mesmo padrão custa metade do 1º), um **piso de 2h por camada tocada** (ler a SPEC, revisar o que o agente gerou, validar e aprovar não desaparece) e um **gate de pré-condições** — a coluna IA-DLC só vale se `DESIGN.md`, `CONTEXT.md`/`AGENT_RULES.md`, SPEC por funcionalidade e time treinado em AI-DLC estiverem no lugar. O que falhar no gate volta para a coluna Base. É isso que torna o número baixo defensável: ele é o preço de um caminho de entrega específico, não otimismo.

**Atenção ao comparar propostas:** CBS gerado antes da v0.2.0 está em outra régua. Proposta em aberto estimada na régua antiga não deve ser reemitida sem revisão. Racional completo, alternativas descartadas e o plano de recalibração por realizado em [`docs/adr/ADR-001-calibracao-ia-dlc-cbs.md`](docs/adr/ADR-001-calibracao-ia-dlc-cbs.md).

### `templates/`

| Grupo | Arquivos | Quando usar |
|---|---|---|
| Repetíveis (vão para `_templates/` do vault) | `tpl-adr.md`, `tpl-evidencia-teste.md`, `tpl-funcionalidade.md`, `tpl-reuniao.md`, `tpl-risco.md`, `tpl-guia-refinamento.md`, `tpl-documento-refinamento.md`, `tpl-spec-funcionalidade.md`, `tpl-roteiro-entrevista.md`, `tpl-ux-assessment-revisao.md` | Toda vez que se cria um novo artefato daquele tipo. |
| Root do projeto (bootstrap) | `CLAUDE.md.template`, `AGENTS.md.template` | Uma vez, ao inicializar o vault (placeholder `{{PROJECT_NAME}}`). |
| Primeiro entregável real (não é bootstrap, um documento por projeto, mantido no lugar) | `tpl-proposta-comercial.md`, `tpl-memoria-projeto.md`, `tpl-visao-produto.md`, `tpl-context-inicial.md`, `tpl-agent-rules.md`, `tpl-registro-riscos.md`, `tpl-metricas-sucesso.md`, `tpl-sintese-reunioes-cliente.md`, `tpl-preparacao-refinamento.md`, `tpl-hipoteses-estrategicas.md`, `tpl-lacunas-entendimento.md`, `tpl-log-decisoes.md`, `tpl-go-no-go.md`, `tpl-confidence-score.md`, `tpl-pauta-refinamento-demanda.md`, `tpl-cbs.md`, `tpl-entregaveis-candidatos.md`, `tpl-design.md` + `tpl-design-draft.md`, `tpl-glossario.md`, `tpl-participantes.md`, `tpl-normalizacao.md` | Quando o projeto real produz esses documentos pela primeira vez (pré-venda/discovery/desenvolvimento) — nunca preenchidos com conteúdo inventado no bootstrap. Ver `skills/dojo/references/project-bootstrap.md`. |

`tpl-guia-refinamento.md` é novo: a FASE 2 (Etapa 2) sempre descreveu o `GUIA DE REFINAMENTO` como saída obrigatória, gerada automaticamente pelo agente antes de cada sessão de refinamento, mas o pacote nunca teve um template para ele — a estrutura foi extraída de um guia de refinamento real já usado em projeto, generalizada e limpa de qualquer conteúdo específico de cliente.

`tpl-documento-refinamento.md` substitui o antigo `tpl-specs.md`: apesar do nome antigo, ele sempre gerou o `DOCUMENTO DE REFINAMENTO` da FASE 2 (o **O QUE**), não a `SPEC_{FUNCIONALIDADE}.md` da FASE 4 (o **COMO** técnico) — que agora tem seu próprio template, `tpl-spec-funcionalidade.md`.

`tpl-design.md` deixou de ser "por jornada": a skill `design-md-generator` confirmou que é um documento único por projeto (Design System completo — tokens + racional), criado uma vez e atualizado incrementalmente, não recriado a cada jornada — por isso mudou de grupo (era listado como repetível antes desta skill existir).

Os seis templates novos de pré-venda (`tpl-hipoteses-estrategicas.md`, `tpl-lacunas-entendimento.md`, `tpl-log-decisoes.md`, `tpl-go-no-go.md`, `tpl-confidence-score.md`, `tpl-pauta-refinamento-demanda.md`) vieram da skill `consolidacao-pos-reuniao-inicial` — GO/NO-GO e nível de confiança não existiam na FASE 1 - PREVENDA.md original; foram adotados como conceito oficial do Dojo Framework, não apenas desta skill.

Documentos de arquitetura (SAD, C4, padrões de código, infra) e conteúdo pontual (GAP reports de um épico específico, cenários de teste de uma feature específica) **não** têm template aqui — são decisões e conteúdo genuinamente específicos de cada projeto; `tpl-adr.md` já cobre o formato recorrente de registro de decisão.

## Bootstrap de um projeto novo

Veja `skills/dojo/references/project-bootstrap.md` para o procedimento completo de scaffolding de um vault novo (estrutura de pastas de fase, templates, assets, `CLAUDE.md`/`AGENTS.md`, config inicial do Obsidian) sem inventar conteúdo de cliente. `.obsidian/` é sempre gerado localmente e nunca versionado — config de editor é pessoal, não é artefato do projeto.
