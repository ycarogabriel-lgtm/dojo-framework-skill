---
phase: produto
deliverable: Dicionário de normalização de transcrições
owner: Performa_IT
status: draft
source: [transcrições brutas em `_assets/docs/`]
related_issues:
version: 0.1
last_review: [data]
---

# Dicionário de Normalização

Mapa **variante → canônico** aplicado pela skill `normalizacao-transcricao`.
Este é o artefato **operacional**: existe para a máquina corrigir transcrições,
não para leitura de negócio. O vocabulário de negócio está em
[GLOSSARIO.md](GLOSSARIO.md); as pessoas, em [PARTICIPANTES.md](PARTICIPANTES.md).

## Como ler

- **Variante**: forma como o termo saiu da transcrição automática.
- **Canônico**: forma que deve aparecer no documento normalizado.
- **Escopo**: `sempre` = substituição segura em qualquer contexto;
  `contexto` = só substituir quando o assunto for o indicado, porque a variante
  também é uma palavra legítima do português.

> Substituições de escopo `contexto` **nunca** devem ser aplicadas por regex
> cega. O agente decide caso a caso lendo a frase.

## Termos

| Variante | Canônico | Escopo | Nota |
|---|---|---|---|
| [forma incorreta observada] | [forma canônica] | sempre / contexto | [quando aplicar, e exceções conhecidas] |

## Pessoas

Fonte: [PARTICIPANTES.md](PARTICIPANTES.md). Repetido aqui só o que exige
decisão de máquina (apelidos ambíguos, contas genéricas, homônimos).

| Variante | Canônico | Escopo | Nota |
|---|---|---|---|
| [apelido/variante] | [nome canônico] | sempre / contexto | [nota] |

## Contas genéricas do Teams (ou equivalente)

Nem todo falante da transcrição tem nome de pessoa. Ferramentas de
videoconferência às vezes gravam o **nome de exibição da conta**, que pode ser
um recurso compartilhado — sala de reunião, estação de trabalho, usuário de
setor.

Conhecidas até hoje:

| Nome de exibição | Pessoa | Onde apareceu |
|---|---|---|
| [`Nome genérico da conta`] | [Pessoa real por trás da conta] | [Onde/quando apareceu] |

Regra: conta genérica **nunca** vira participante com esse nome no documento
final. Se não estiver mapeada aqui, entra no relatório como falante não
resolvido — não inventar quem é.

## Ruídos a remover

Padrões da transcrição automática que não devem sobreviver ao documento
normalizado:

- Linhas de sistema: `<Nome> começou a transcrição`, `<Nome> parou a transcrição`.
- Timestamps por fala (`Nome   0:03`) — a duração total vai para o cabeçalho.
- Marcadores de participante entrando/saindo da reunião.
- Repetições de gaguejo e muletas (`né`, `assim`, `tipo`, `então assim`) quando
  não carregarem significado.
- Falas de coordenação sem conteúdo ("tá me ouvindo?", "vou compartilhar a tela").

## Termos novos

Quando a skill encontrar um termo recorrente que não está aqui nem no glossário,
ela **não inventa**: registra na seção abaixo e reporta ao usuário para decisão.

*Nenhum termo aguardando decisão.*
