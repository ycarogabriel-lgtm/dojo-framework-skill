# Project Bootstrap

How to scaffold a brand-new Dojo vault from scratch. Use this only after `workspace-detection.md` confirms there's no vault here yet and the user actually wants one initialized — never scaffold over an existing vault or a real codebase.

## Procedure

1. **Ask for the project/client name** before creating anything — it fills the placeholders in the generated `CLAUDE.md`/`AGENTS.md` and the project key (`PIPROJETO-XXXX` convention from `FASE 1 - PREVENDA.md`).
2. **Create the phase-folder skeleton** at the vault root:
   ```
   01_pre-venda/{insumos,intent,memoria-do-projeto,proposta-comercial,qualificacao}
   02_discovery/{design-system,funcionalidades,jornadas,kickoff,personas,prototipos,refinamentos}
   03_arquitetura/{adr,ambientes,c4,infra,sad}
   04_desenvolvimento/{backlog,bolts,contexto-agentes,sessoes-ia,specs}
   05_testes-funcionais/{defeitos,evidencias,planos,relatorios}
   06_review/{aceites,atas,feedbacks,pautas}
   07_ajustes-pos-review/{go-no-go,itens,validacoes}
   08_deploy/{comunicacoes,planos,rollback}
   09_hyper-care/{correcoes,encerramento,ocorrencias}
   10_ams/{chamados,slas,transicao}
   produto/visao/
   _decisions/
   _ai-sessions/
   _meetings/
   _risks/
   _metrics/
   _templates/
   _assets/
   ```
   Each phase folder and subfolder gets a short `README.md` stub describing its purpose (see the Phase Map in `operating-model.md` for the one-line purpose of each top-level folder).
3. **Populate `_templates/`** with the repeatable templates shipped alongside this skill (`../../templates/` in this package) — each used every time a new artifact of that type is created: `tpl-adr.md`, `tpl-evidencia-teste.md`, `tpl-funcionalidade.md`, `tpl-reuniao.md`, `tpl-risco.md`, `tpl-guia-refinamento.md`, `tpl-documento-refinamento.md`, `tpl-spec-funcionalidade.md`, `tpl-roteiro-entrevista.md`, `tpl-ux-assessment-revisao.md` (one per screen/product assessed, if the team uses the `ux-assessment-heuristico` skill).
4. **Populate `_assets/`** with only the methodology assets shipped in this package (`../../assets/`): the four `FASE N - *.md` guides and the three AI-DLC pre-sales agent specs (`SPEC_IntentListener.md`, `SPEC_IntentRefiner.md`, `SPEC_PersonaGenerator.md`). Do **not** create any client-specific document here — there isn't one yet.
5. **Add `_decisions/README.md`** and **`_ai-sessions/README.md`** with the standard conventions: ADRs and product decisions go through `tpl-adr.md` (register product decisions as hypotheses first, promote only after human approval); AI session records capture prompts, plans, decisions, and results.
6. **Generate the root `CLAUDE.md` and `AGENTS.md`** by copying `../../templates/CLAUDE.md.template` and `../../templates/AGENTS.md.template` and substituting `{{PROJECT_NAME}}` with the project/client name. Do not freehand these files or reconstruct them from memory — the templates are the source of truth for the vault map, templates table, development-gate rules, and agent-conduct rules; drifting from them across projects is exactly the duplication problem this package exists to avoid.
7. **Set up Obsidian, without versioning it.** Create a `.obsidian/` folder at the vault root and copy the three files shipped at `../../assets/obsidian-config/` (`app.json`, `core-plugins.json`, `appearance.json`) into it — this enables the plugins the vault actually relies on (`templates` pointed at `_templates/`, `daily-notes`, `canvas`, `bases`, `graph`, ...) without any manual setup. Then add `.obsidian/` to the new project's `.gitignore`, with a comment explaining why (e.g. `# Obsidian local editor settings (UI pessoal, não artefato do projeto)`).
   - **Never copy `workspace.json` or `graph.json`** from another vault, and never version them in the new one — they hold instance-specific state (open tabs, exact file paths, graph view tuning) and always leak whatever vault they came from into the new one. Every project is its own vault; Obsidian regenerates these files locally the first time someone opens it, and they must never be shared or synced across vaults.
   - Community plugins (e.g. `obsidian-git`, `obsidian-advanced-uri`, `buttons`) are not bundled here — their code isn't vendored in this package. If the team wants them, install through Obsidian's own community plugin browser and let `.gitignore` keep `.obsidian/` out of version control either way.
8. **Make the skill available in the new project**, in one of two ways:
   - If this plugin is installed at the user level, nothing else is needed — the skill is already available in any workspace.
   - Otherwise, copy `skills/dojo/` (and any of the auxiliary skills the team wants — `normalizacao-transcricao`, `geracao-backlog`, `geracao-ata-reuniao`, `consolidacao-pos-reuniao-inicial`, `preparacao-refinamento-demanda`, `cbs-completo`, `design-md-generator`, `ux-assessment-heuristico`) into the new project's `.claude/skills/` and, if the team also uses Codex, into `.agents/skills/` as well.
9. **Never invent client content.** Personas, product vision, specs, and real risks only get created as the actual project phases (pré-venda, discovery, ...) produce them — bootstrap only creates the generic skeleton and methodology assets. Do **not** pre-create `01_pre-venda/proposta-comercial/PROPOSTA_COMERCIAL.md`, `01_pre-venda/memoria-do-projeto/MEMORIA_DO_PROJETO.md`, `01_pre-venda/insumos/SINTESE_REUNIOES_CLIENTE.md`, `produto/visao/visao-do-produto.md`, `_risks/REGISTRO_RISCOS_INICIAL.md`, `_metrics/METRICAS_SUCESSO_INICIAIS.md`, `04_desenvolvimento/contexto-agentes/{CONTEXT,AGENT_RULES}.md`, or `produto/glossario/{GLOSSARIO,PARTICIPANTES,NORMALIZACAO}.md` at bootstrap time — they hold real client content that doesn't exist yet.

## First real deliverables (not part of bootstrap)

When the project's actual work produces these documents for the first time — later, during `01_pre-venda`/`02_discovery`/`04_desenvolvimento`, never at bootstrap — start from the matching template in `../../templates/` instead of freehanding the structure. Each of these is created once per project and then maintained/updated in place (unlike the repeatable templates in step 3, which get a new file per artifact). Cross-project use confirms these shapes (including the shared frontmatter convention — see `operating-model.md`) are genuine Dojo conventions, not one-off habits:

| First real deliverable | Template |
|---|---|
| `01_pre-venda/proposta-comercial/PROPOSTA_COMERCIAL.md` | `tpl-proposta-comercial.md` |
| `01_pre-venda/memoria-do-projeto/MEMORIA_DO_PROJETO.md` (only once the project is approved — see `FASE 1 - PREVENDA.md`) | `tpl-memoria-projeto.md` |
| `01_pre-venda/insumos/SINTESE_REUNIOES_CLIENTE.md` | `tpl-sintese-reunioes-cliente.md` |
| `01_pre-venda/insumos/PREPARACAO_REFINAMENTO_{PROJETO}.md` (prep for the Refinamento da Demanda meeting) | `tpl-preparacao-refinamento.md` |
| `01_pre-venda/qualificacao/HIPOTESES_ESTRATEGICAS_{PROJETO}.md` | `tpl-hipoteses-estrategicas.md` |
| `01_pre-venda/qualificacao/LACUNAS_ENTENDIMENTO_{PROJETO}.md` | `tpl-lacunas-entendimento.md` |
| `01_pre-venda/qualificacao/LOG_DECISOES_{PROJETO}.md` | `tpl-log-decisoes.md` |
| `01_pre-venda/qualificacao/GO_NO_GO_{PROJETO}.md` | `tpl-go-no-go.md` |
| `01_pre-venda/qualificacao/NIVEL_CONFIANCA_{PROJETO}.md` | `tpl-confidence-score.md` |
| `01_pre-venda/qualificacao/PAUTA_REFINAMENTO_DEMANDA_{PROJETO}.md` | `tpl-pauta-refinamento-demanda.md` |
| Cost Breakdown Structure, `CBS_{PROJETO}_resumo_v1.md` (+ CSV) — see `skills/cbs-completo/SKILL.md` | `tpl-cbs.md` |
| `entregaveis_{PROJETO}_v1.md` (pre-refinement Épico/Feature working list feeding the CBS and the commercial proposal) | `tpl-entregaveis-candidatos.md` |
| `produto/visao/visao-do-produto.md` | `tpl-visao-produto.md` |
| `_risks/REGISTRO_RISCOS_INICIAL.md` | `tpl-registro-riscos.md` |
| `_metrics/METRICAS_SUCESSO_INICIAIS.md` | `tpl-metricas-sucesso.md` |
| `04_desenvolvimento/contexto-agentes/CONTEXT.md` (initial, pre-architecture shape) | `tpl-context-inicial.md` |
| `04_desenvolvimento/contexto-agentes/AGENT_RULES.md` (base rule set) | `tpl-agent-rules.md` |
| `02_discovery/design-system/DESIGN.md` (project-wide design tokens + rationale — vault-tracked copy; see `skills/design-md-generator/SKILL.md` for the operational copy kept in the code repo root) | `tpl-design.md` (final) / `tpl-design-draft.md` (draft) |
| `produto/glossario/GLOSSARIO.md` | `tpl-glossario.md` |
| `produto/glossario/PARTICIPANTES.md` | `tpl-participantes.md` |
| `produto/glossario/NORMALIZACAO.md` | `tpl-normalizacao.md` |

These templates hold bracketed placeholders (`[...]`), never invented content — fill them in only with what the real project actually produced.

One more real document from the Development Gate is repeatable, not one-time, and belongs with step 3 instead: `SPEC_{FUNCIONALIDADE}.md` (one per functionality per BOLT — `tpl-spec-funcionalidade.md`, the technical **HOW**, distinct from the `DOCUMENTO DE REFINAMENTO`'s **WHAT**).
