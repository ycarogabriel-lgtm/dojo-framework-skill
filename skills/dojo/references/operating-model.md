# Dojo Framework Operating Model

This reference captures the validated operating model for a Dojo Framework project vault. Prefer current vault files over this summary when exact wording or current status matters. This document must stay project-agnostic — it never names a specific client, product, or domain.

## Source Order

1. Current workspace files (vault root, or `vault/` if that subdirectory exists).
2. Phase source notes under `_assets/`.
3. Product and implementation context under:
   - `produto/visao/visao-do-produto.md` (or the project's equivalent product-vision doc)
   - `04_desenvolvimento/contexto-agentes/CONTEXT.md`
   - `04_desenvolvimento/contexto-agentes/AGENT_RULES.md`
4. Prior memory or summaries.
5. Authenticated external site pages, only when the user explicitly wants them checked and the session/access constraint is handled.

## Core Model

- Obsidian (or an equivalent markdown vault) stores living memory: decisions, meetings, risks, refinements, specs, context, metrics, and AI sessions.
- GitHub stores execution: issues, milestones, pull requests, releases, code, tests, and technical evidence.
- Important vault notes should include phase, deliverable, owner/status when useful, and links to execution artifacts when available.
- Important GitHub items should link back to the relevant vault artifact.
- A feature should not enter a BOLT without a spec.
- An agent should not edit code without approved project context, approved agent rules, a relevant spec, and a plan.
- The agent proposes, the human approves, the agent executes.

## Phase Map

| Phase | Purpose | Key artifacts |
|---|---|---|
| `01_pre-venda` | Understand the client need with minimum viable effort before sale. Create a durable project key such as `PIPROJETO-XXXX`. | `INTENT DO PROJETO`, macro solution, success metrics, commercial proposal, initial risk register, project memory. |
| `02_discovery` | Convert project memory into personas, functionalities, journeys, refinements, and design system. Runs as a continuous wave and can overlap development. | Kickoff notes, personas, functionality list, journey diagrams, `DESIGN.md`, refinement guide, refinement documents, prototypes. |
| `03_arquitetura` | Define the technical truth for development. Runs in parallel with Discovery after commercial approval. | SAD, ADRs, Mermaid C4 diagrams, NFRs, security rules, approved dependencies, environments, repo/branch strategy, CI/CD, initial `CONTEXT.md` and `AGENT_RULES.md`. |
| `04_desenvolvimento` | Deliver in weekly BOLTs using AI-DLC. | Final `CONTEXT.md`, final `AGENT_RULES.md`, backlog, `SPEC_{FUNCIONALIDADE}.md`, implementation plan, tests, updated docs, AI session records. |
| `05_testes-funcionais` | Validate delivered behavior against functional criteria. | Test plans, evidence, defects, reports. |
| `06_review` | Run client/team review and formalize feedback or acceptance. | Agendas, minutes, feedback, acceptance notes. |
| `07_ajustes-pos-review` | Handle post-review changes and go/no-go validation. | Adjustment items, validations, go/no-go records. |
| `08_deploy` | Prepare and execute release. | Deploy plans, rollback plans, communications. |
| `09_hyper-care` | Monitor early production use and close immediate issues. | Occurrences, corrections, closure notes. |
| `10_ams` | Transition to support and ongoing service. | Transition notes, tickets, SLAs. |

## Development Gate

Before implementation with an AI agent, verify the following inputs:

- `CONTEXT.md`: project intent, architecture summary, modules, integrations, relevant risks, references, and current status.
- `AGENT_RULES.md`: architecture, NFR, security, quality, test, dependency, and documentation rules.
- `SPEC_{FUNCIONALIDADE}.md`: purpose, refinement reference, design reference, technical approach, NFR/security considerations, and test scenarios.
- Design reference: `DESIGN.md`, prototype, screenshot, Figma/Stitch/Claude Design artifact, or equivalent.
- Architecture reference: SAD, ADRs, C4 diagrams, infra/environment notes, approved dependencies.
- Risk and decision references when the feature touches scope, integration, security, performance, data, or customer commitments.

If any required input is missing or inconsistent, ask precise questions or update the vault artifact before editing code. See `workspace-detection.md` for when this gate applies (real FE/BE codebases) versus when it doesn't (docs vault, throwaway FE prototypes).

## Document Frontmatter

Vault documents that represent a tracked deliverable (product vision, `CONTEXT.md`, risk register, success metrics, glossary, synthesis docs, etc.) use a consistent YAML frontmatter — confirmed across every real project this framework has run in:

```yaml
---
phase: 01_pre-venda
deliverable: <what this document is>
owner: Performa_IT
status: draft | aberto | em revisão | aprovado
source: <what fed this document — meeting notes, prior artifacts>
related_issues:
version: 0.1
last_review: <date>
---
```

Bump `version` and `last_review` whenever the document changes meaningfully, not on every typo fix. This applies to the first-real-deliverable templates referenced from `project-bootstrap.md` (product vision, initial context, risk register, success metrics, meeting synthesis, glossary/participants/normalization) — not to the six repeatable `_templates/` artifacts, which carry their own frontmatter conventions per template.

## Agent Conduct

- Read the relevant vault context before proposing changes.
- Surface gaps before making product or architecture decisions.
- Keep solutions aligned with the project's own MVP scope — read that scope from the current project's product-vision doc, never assumed or carried over from another engagement.
- Register meaningful decisions in `_decisions`.
- Update specs when implementation changes expected behavior.
- Add or update tests when behavior changes.
- Preserve traceability between vault artifacts and execution artifacts.
