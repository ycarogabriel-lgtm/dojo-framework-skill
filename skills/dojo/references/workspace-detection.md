# Workspace Detection

Run this before proposing or implementing anything. The same instructions that apply to a documentation vault do not apply to a real codebase, and a throwaway prototype does not deserve the same rigor as production code. Getting this wrong means either editing a vault as if it were code, or skipping the development gate on real application code.

## The four workspace types

| Type | Signals | Rule |
|---|---|---|
| **Docs vault (Dojo)** | Numbered phase folders (`01_..` through `10_..`), `_assets/`, `_templates/`, `produto/`; a root `CLAUDE.md`/`AGENTS.md` stating the repo is a project vault; content is overwhelmingly `.md`/`.docx`/`.pdf`/`.xlsx`; no `package.json` or other build manifest. | Never implement application code here. Only produce documents, specs, decisions, and templates. |
| **FE prototype** | A design-tool export (Figma, Stitch, v0, Lovable, Claude Design, or similar), static HTML/CSS/JS or a minimal SPA with no real backend integration, hardcoded/mock data, no test suite, no CI. Often referenced from a vault's `02_discovery/prototipos/`. | Exempt from the Development Gate — it's disposable discovery material. Label it explicitly as a prototype (in the README, commit messages, or vault link) so it's never mistaken for production code or treated as the source of truth for business rules. |
| **Real FE codebase** | A `package.json` (or equivalent manifest) with an actual frontend framework dependency (React, Vue, Next, Angular, ...), a `src/` with routing/state management, calls to a real or documented-mock API, a test suite, build/CI configuration. Often a sibling repo referenced by the vault's `CONTEXT.md`. | Subject to the full Development Gate: do not edit without approved `CONTEXT.md`, `AGENT_RULES.md`, the relevant `SPEC_{FUNCIONALIDADE}.md`, and an approved design reference. |
| **Real BE codebase** | Server/API project structure (controllers/routes, models/entities, migrations), backend framework dependencies, infra/deploy configuration, a test suite. | Same Development Gate as the real FE codebase. |

## Procedure

1. Check for docs-vault signals first. If present, stop here — this is a vault, not a codebase.
2. If there's no vault signal, look for a build/dependency manifest (`package.json`, `pom.xml`, `go.mod`, `requirements.txt`, `*.csproj`, etc.).
   - No manifest, mostly static assets or a design-tool export → FE prototype.
   - Manifest present → inspect its dependencies and folder structure to decide FE vs BE (a monorepo may contain both; evaluate each side independently against the Development Gate).
3. If the signals are mixed or ambiguous, ask the user directly rather than guessing. A wrong classification either blocks legitimate work (treating real code as untouchable) or skips a gate that exists specifically to prevent ungrounded changes.
