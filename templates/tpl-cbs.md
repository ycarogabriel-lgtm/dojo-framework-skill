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
| C | `Épico (número e nome)` | Ex: `Épico 1: Gestão de Agenda` |
| D | `Feature/Entregável (número e nome)` | Ex: `1.1 Agenda Diária e Semanal` |
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

## Tabelas de referência para estimativas FE

| Tipo de tela / componente | FE horas (com IA) |
|---|---|
| Tela de listagem simples (tabela + filtros básicos) | 8–12h |
| Tela de listagem com filtros complexos + export | 12–18h |
| Formulário simples (até 10 campos) | 8–12h |
| Formulário complexo (múltiplas abas, validações, 20+ campos) | 16–24h |
| Modal / drawer de detalhe | 6–10h |
| Dashboard / painel com gráficos e indicadores | 16–24h |
| Fluxo multi-step / wizard (3–5 etapas) | 20–30h |
| Agenda / calendário interativo | 30–50h |
| Timeline cronológica | 12–18h |
| Tela de prescrição / editor texto livre | 12–20h |
| Integração de componente externo (embed/iframe) | 8–16h |
| Painel de exibição em TV / display tempo real | 12–20h |
| Upload + preview de arquivo/imagem | 8–14h |
| Notificações e toasts | 4–6h |
| Componentes compartilhados reutilizáveis | 6–12h |
| Configuração / cadastro simples | 8–14h |

> **Sem screenshots/timestamps:** aumentar FE em 10–15% e registrar nas
> Observações: "Estimativa FE baseada em descrição textual — sem gravação do
> sistema atual."

## Tabelas de referência para estimativas BE

| Tipo de operação | BE horas (com IA) |
|---|---|
| CRUD simples (1 entidade, sem regras complexas) | 8–12h |
| CRUD com regras de negócio (validações, workflows) | 12–20h |
| Integração com API externa simples (REST documentada) | 8–16h |
| Integração com API externa complexa (bidirecional, webhooks) | 20–40h |
| Motor de regras de negócio | 20–40h |
| Relatório / query analítica complexa | 12–24h |
| Sistema de notificações (push/email/SMS/WhatsApp) | 12–20h |
| Sistema de permissões / RBAC | 16–24h |
| Upload e processamento de arquivos | 8–16h |
| Pipeline ETL / migração de dados | 24–80h (por entidade) |
| Autenticação e gestão de sessão | 12–20h |
| WebSocket / atualização em tempo real | 12–20h |
| Geração de PDF / documentos | 8–16h |

## Regras de granularidade

- **1 linha = 1 feature** — nunca agregar features distintas
- **Feature grande:** se FE > 40h **ou** BE > 60h, registrar nas Observações:
  "Recomendado dividir em sub-features no backlog"
- Épicos numerados sequencialmente sem pular; Features numeradas N.1, N.2...

## Validações antes de salvar

- [ ] Nenhuma linha com horas = 0 sem justificativa
- [ ] Horas Totais = FE + BE em todas as linhas
- [ ] Todos os épicos numerados sequencialmente
- [ ] Nenhuma feature sem descrição
- [ ] Features `Nova` com descrição ampliada
- [ ] Features com integração externa têm Premissas preenchidas

## Arquivo de resumo

**Arquivo:** `CBS_[nome-do-projeto]_resumo_v1.md`

### Totais por épico

| Épico | Horas FE | Horas BE | Horas Totais | Dias (8h/dia) |
|---|---|---|---|---|
| [Épico 1: Nome] | [FE] | [BE] | [Total] | [Dias] |

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

### Features sinalizadas para divisão no backlog

- [Feature] — [motivo: FE > 40h / BE > 60h]

### Decisões abertas que afetam o escopo

- [Decisão pendente e quem precisa validá-la]

## Premissas globais

- Estimativa em horas com IA; **8h = 1 dia útil**
- Produtividade com IA já incorporada nas estimativas de referência
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
