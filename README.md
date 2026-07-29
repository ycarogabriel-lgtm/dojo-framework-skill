# Dojo Framework Skill

Pacote genérico do **Dojo Framework** da Performa_IT: metodologia de projeto (pré-venda a AMS), gate de desenvolvimento, bootstrap de vault, detecção de tipo de workspace e três skills auxiliares (normalização de transcrição, geração de backlog, geração de ata de reunião). Nenhum arquivo aqui menciona um cliente específico — isso é o que permite reusar o pacote em qualquer projeto novo sem contaminar o contexto do agente com dados de outro cliente.

## Por que este repositório existe

Antes deste pacote, a skill `dojo` (e as três skills auxiliares) viviam duplicadas dentro de cada vault de cliente, copiadas manualmente projeto a projeto. Isso gerava contaminação cruzada real: uma skill copiada de um projeto trazia nomes de cliente, glossário e stack de um domínio completamente diferente, hardcoded no meio da lógica genérica. Este repositório é a fonte única e genérica; cada vault de cliente consome dele, nunca o contrário.

## Instalação

Como plugin do Claude Code, a partir de um checkout local deste repositório:

```bash
claude plugin marketplace add /caminho/para/dojo-framework-skill
claude plugin install dojo-framework-skill@dojo-framework-skill
```

Uma vez instalado (a nível de usuário ou de projeto), a skill `dojo` — e as skills auxiliares — ficam disponíveis automaticamente em qualquer workspace, sem precisar copiar arquivos para dentro do repositório do cliente.

Alternativa sem plugin: copiar manualmente a pasta de uma skill (ex. `skills/dojo/`) para `.claude/skills/dojo/` (e, se o time também usa Codex, para `.agents/skills/dojo/`) dentro do vault do cliente.

## O que está aqui

| Pasta | Conteúdo |
|---|---|
| `skills/dojo/` | Metodologia central: mapa de fases, gate de desenvolvimento, detecção de tipo de workspace (`workspace-detection.md`) e bootstrap de projeto novo (`project-bootstrap.md`). |
| `skills/normalizacao-transcricao/` | Converte transcrição bruta de reunião (Teams, `.docx`/`.txt`) no documento estruturado padrão do vault. |
| `skills/geracao-backlog/` | Estrutura refinamentos e SPECs como histórias de backlog rastreáveis (Jira), com elegibilidade AI-DLC. |
| `skills/geracao-ata-reuniao/` | Converte o documento estruturado de uma reunião em ATA executiva (`.docx`). |
| `templates/` | Os 6 templates reutilizáveis do vault (ADR, reunião, risco, funcionalidade, specs, evidência de teste). |
| `assets/` | Guias de fase (FASE 1–4), specs dos agentes AI-DLC de pré-venda (Intent Listener/Refiner, Persona Generator) e template de roteiro de entrevista. |

## Bootstrap de um projeto novo

Veja `skills/dojo/references/project-bootstrap.md` para o procedimento completo de scaffolding de um vault novo (estrutura de pastas de fase, templates, assets, `CLAUDE.md`/`AGENTS.md`) sem inventar conteúdo de cliente.
