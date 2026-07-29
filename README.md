# Dojo Framework Skill

Pacote genérico do **Dojo Framework** da Performa_IT: metodologia de projeto (pré-venda a AMS), gate de desenvolvimento, bootstrap de vault, detecção de tipo de workspace e três skills auxiliares (normalização de transcrição, geração de backlog, geração de ata de reunião). Nenhum arquivo aqui menciona um cliente específico — isso é o que permite reusar o pacote em qualquer projeto novo sem contaminar o contexto do agente com dados de outro cliente.

## Por que este repositório existe

Antes deste pacote, a skill `dojo` (e as três skills auxiliares) viviam duplicadas dentro de cada vault de cliente, copiadas manualmente projeto a projeto. Isso gerava contaminação cruzada real: uma skill copiada de um projeto trazia nomes de cliente, glossário e stack de um domínio completamente diferente, hardcoded no meio da lógica genérica. Este repositório é a fonte única e genérica; cada vault de cliente consome dele, nunca o contrário.

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
| `skills/normalizacao-transcricao/` | Converte transcrição bruta de reunião (Teams, `.docx`/`.txt`) no documento estruturado padrão do vault. |
| `skills/geracao-backlog/` | Estrutura refinamentos e SPECs como histórias de backlog rastreáveis (Jira), com elegibilidade AI-DLC. |
| `skills/geracao-ata-reuniao/` | Converte o documento estruturado de uma reunião em ATA executiva (`.docx`). |
| `templates/` | Os 6 templates reutilizáveis do vault (ADR, reunião, risco, funcionalidade, specs, evidência de teste) + `CLAUDE.md.template`/`AGENTS.md.template` para o root do projeto novo (placeholder `{{PROJECT_NAME}}`). |
| `assets/` | Guias de fase (FASE 1–4), specs dos agentes AI-DLC de pré-venda (Intent Listener/Refiner, Persona Generator), template de roteiro de entrevista e config genérica do Obsidian (`obsidian-config/`). |

## Bootstrap de um projeto novo

Veja `skills/dojo/references/project-bootstrap.md` para o procedimento completo de scaffolding de um vault novo (estrutura de pastas de fase, templates, assets, `CLAUDE.md`/`AGENTS.md`, config inicial do Obsidian) sem inventar conteúdo de cliente. `.obsidian/` é sempre gerado localmente e nunca versionado — segue a convenção já usada no vault do SAV (config de editor é pessoal, não é artefato do projeto).
