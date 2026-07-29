---
name: dojo
description: Use when working inside a Performa_IT Dojo Framework project vault — analyzing, planning, updating, or implementing work involving the Obsidian-style project vault, GitHub traceability, phase artifacts (pré-venda through AMS), AI-DLC/BOLT workflows, CONTEXT.md, AGENT_RULES.md, or SPEC files. Also use when bootstrapping a brand-new Dojo vault, or when you need to determine whether the current workspace is a docs vault, an FE prototype, a real FE codebase, or a real BE codebase before proposing or implementing anything.
---

# Dojo Framework

Use this skill to keep work aligned with the Dojo Framework operating model: Obsidian (or an equivalent markdown vault) is the project memory, GitHub is the execution and code-versioning layer, and AI agents act only from approved context. This skill is project-agnostic — it must never carry over content, product anchors, or terminology from a specific client engagement.

## Step 0 — Identify the Workspace

Before proposing or implementing anything, determine what kind of directory you're actually in: a Dojo docs vault, an FE prototype, a real FE codebase, or a real BE codebase. Each has different rules about whether code may be touched at all. Read `references/workspace-detection.md` and run its checklist first.

## Start From Local Truth

Once you know you're in a Dojo vault, inspect current files before relying on memory or prior summaries — never assume a fixed layout:

- If a `vault/` subdirectory exists at the workspace root, treat it as the vault root; otherwise the workspace root itself is the vault.
- Start with (paths relative to the vault root): `produto/visao/visao-do-produto.md` (or equivalent product-vision doc), `04_desenvolvimento/contexto-agentes/CONTEXT.md`, `04_desenvolvimento/contexto-agentes/AGENT_RULES.md`.
- For phase mechanics, read the source files under `_assets/`, especially `FASE 1 - PREVENDA.md` through `FASE 4 - DESENVOLVIMENTO.md`.
- Treat any project-specific "team" or "roster" doc as optional context, not a hard requirement — its filename and location vary per project.

If a public or authenticated Dojo site is mentioned, treat it as source material only after the user confirms access constraints. The local vault and `_assets` files are always the stronger truth source.

## Working Workflow

1. Identify the current phase, deliverable, and requested artifact before changing anything.
2. Load the phase-specific source docs and any linked product, design, architecture, risk, or meeting notes.
3. If the request affects code or implementation, require approved `CONTEXT.md`, `AGENT_RULES.md`, the relevant `SPEC_{FUNCIONALIDADE}.md`, and architecture/design references before editing code.
4. Ask targeted questions when product, architecture, security, integration, or scope decisions are missing.
5. Propose a concrete plan before implementation work unless the user already supplied an approved plan.
6. Update the vault when decisions, specs, risks, refinements, or implementation behavior change.
7. Keep GitHub and vault traceability explicit: important vault notes should link to issues, PRs, milestones, or releases when they exist; important execution items should link back to the vault.

## Populate a New Project

If the current workspace has no Dojo vault yet and the user wants one, read `references/project-bootstrap.md` and follow its scaffolding procedure. Never invent client-specific content (personas, product vision, specs) during bootstrap — only the generic phase-folder skeleton and methodology assets get created; real project content is filled in as the actual project phases produce it.

## Output Rules

- Prefer concrete workspace artifacts over generic advice.
- Preserve the project's own working language (e.g. Portuguese) for project artifacts unless the source material requires another language.
- Keep solutions simple and aligned to MVP scope; do not import a third-party tool's complexity (e.g. Jira) into a project's own design without a clear, project-specific justification.
- Read the current project's own product-vision doc for product anchors (scope, differentiators, MVP exclusions) — never carry over anchors from a different project or engagement.
- Separate bug, improvement, new feature, and scope change.
- Do not assume external integrations without an approved architecture document.
- When the user says the work is a first step, make the narrow concrete change first.

## Reference

- `references/operating-model.md` — phase map, required artifacts, and the AI-agent development gate.
- `references/workspace-detection.md` — how to classify the current workspace before touching anything.
- `references/project-bootstrap.md` — how to scaffold a brand-new Dojo vault.
