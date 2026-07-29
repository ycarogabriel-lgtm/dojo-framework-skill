# Project Bootstrap

How to scaffold a brand-new Dojo vault from scratch. Use this only after `workspace-detection.md` confirms there's no vault here yet and the user actually wants one initialized — never scaffold over an existing vault or a real codebase.

## Procedure

1. **Ask for the project/client name** before creating anything — it fills the placeholders in the generated `CLAUDE.md`/`AGENTS.md` and the project key (`PIPROJETO-XXXX` convention from `FASE 1 - PREVENDA.md`).
2. **Create the phase-folder skeleton** at the vault root:
   ```
   01_pre-venda/{insumos,intent,memoria-do-projeto,proposta-comercial}
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
3. **Populate `_templates/`** with the six templates shipped alongside this skill (`../../templates/` in this package): `tpl-adr.md`, `tpl-evidencia-teste.md`, `tpl-funcionalidade.md`, `tpl-reuniao.md`, `tpl-risco.md`, `tpl-specs.md`.
4. **Populate `_assets/`** with only the methodology assets shipped in this package (`../../assets/`): the four `FASE N - *.md` guides and the three AI-DLC pre-sales agent specs (`SPEC_IntentListener.md`, `SPEC_IntentRefiner.md`, `SPEC_PersonaGenerator.md`). Do **not** create any client-specific document here — there isn't one yet.
5. **Add `_decisions/README.md`** and **`_ai-sessions/README.md`** with the standard conventions: ADRs and product decisions go through `tpl-adr.md` (register product decisions as hypotheses first, promote only after human approval); AI session records capture prompts, plans, decisions, and results.
6. **Generate the root `CLAUDE.md` and `AGENTS.md`**, substituting the project/client name into the project description, and keeping the rest of the structure (vault map, templates table, development-gate rules, agent conduct rules) identical to what's in this skill's own reference docs.
7. **Make the skill available in the new project**, in one of two ways:
   - If this plugin is installed at the user level, nothing else is needed — the skill is already available in any workspace.
   - Otherwise, copy `skills/dojo/` (and any of the auxiliary skills the team wants — `normalizacao-transcricao`, `geracao-backlog`, `geracao-ata-reuniao`) into the new project's `.claude/skills/` and, if the team also uses Codex, into `.agents/skills/` as well.
8. **Never invent client content.** Personas, product vision, specs, and real risks only get created as the actual project phases (pré-venda, discovery, ...) produce them — bootstrap only creates the generic skeleton and methodology assets.
