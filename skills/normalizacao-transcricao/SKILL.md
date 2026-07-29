---
name: normalizacao-transcricao
description: Use quando uma transcrição de reunião entrar no vault do projeto (arquivos .docx, .txt ou .md em `_assets/docs/`, transcrições do Teams, gravações de call) e precisar ser convertida no documento estruturado padrão — normalizando nomes de participantes, termos de domínio e erros de transcrição automática contra o glossário do vault e as transcrições já estruturadas. Dispara com "normalizar transcrição", "estruturar transcrição", "coloquei a transcrição da reunião", "processar a gravação", "gerar o Estruturado", "atualizar o glossário com os termos da reunião".
---

# Normalização de Transcrições

Converte uma transcrição bruta de reunião no documento estruturado padrão do
vault, usando o glossário do projeto e as transcrições anteriores como
referência de vocabulário e de nomes.

## Princípio inegociável

**Normalizar não é interpretar.** A skill corrige grafia, nomes e ruído de
transcrição automática, e organiza o conteúdo — mas nunca inventa fato,
decisão, responsável ou prazo que não esteja na transcrição. Quando algo estiver
ambíguo ou inaudível, registrar como pendência explícita, não preencher com
suposição.

Da mesma forma: a skill **não inventa termo canônico**. Termo novo ou ambíguo
vai para o relatório final e aguarda decisão do usuário antes de entrar no
glossário.

## Insumos obrigatórios

Carregar antes de processar qualquer coisa:

| Arquivo | Uso |
|---|---|
| `produto/glossario/GLOSSARIO.md` | Vocabulário canônico de negócio do projeto |
| `produto/glossario/PARTICIPANTES.md` | Roster canônico de pessoas do projeto |
| `produto/glossario/NORMALIZACAO.md` | Mapa variante → canônico e ruídos a remover |
| `_assets/docs/*- Estruturado.md` | Precedente de formato e de vocabulário |
| `_templates/tpl-reuniao.md` | Template caso o usuário também queira a ata |

Se algum dos três arquivos de glossário não existir, **criar antes** a partir
das transcrições estruturadas já presentes — não prosseguir sem eles.

## Pipeline

### 1. Localizar e converter

Transcrições brutas vivem em `_assets/docs/`. O documento normalizado é irmão
do bruto, com o sufixo ` - Estruturado.md`:

```
<Projeto> - <Tema da Reunião>.docx
<Projeto> - <Tema da Reunião> - Estruturado.md
```

Para descobrir o que está pendente, listar os brutos (`.docx`, `.txt`) sem
`- Estruturado.md` correspondente.

`.docx` é convertido sem dependência externa:

```bash
python .claude/skills/normalizacao-transcricao/scripts/docx_to_text.py \
  "_assets/docs/<arquivo>.docx" -o "<destino>.txt"
```

Escrever o `.txt` intermediário no scratchpad da sessão, **nunca** no vault.

### 2. Reconhecer o formato de entrada

Dois formatos aparecem hoje:

**Teams (via .docx)** — cabeçalho com título, data e duração, depois falas com
timestamp:

```
Refinamento de negócio ...-20260713_150304-Gravação de Reunião
13 de julho de 2026, 06:03PM
1h 8m 32s

Elaine Cristina Pinto   0:03
texto da fala
```

**Linha por fala (.txt)**:

```
[Leonardo]: texto da fala
```

Do cabeçalho do Teams saem a data e a duração do documento final. Para conferir
a data, use os metadados do pacote — mais confiáveis que o cabeçalho em texto,
que depende do fuso de quem gravou:

```bash
python .claude/skills/normalizacao-transcricao/scripts/docx_to_text.py \
  "_assets/docs/<arquivo>.docx" --meta
```

No formato `[Falante]:`, se não houver data, escrever `não informada na
transcrição de origem` — nunca deduzir a data do nome do arquivo ou do commit.

> **A transcrição não contém lista de presença.** Nem o texto nem os metadados
> do `.docx` registram quem participou em silêncio: só quem falou. Isso define
> a regra de participantes abaixo.

### 3. Normalizar

Nesta ordem:

1. **Participantes** — a linha `**Participantes:**` lista **quem participou da
   reunião, tenha falado ou não**. Como a transcrição só registra falantes, ela
   fornece o piso da lista, nunca a lista completa:

   - Extrair os falantes distintos e resolver cada um contra `PARTICIPANTES.md`.
   - **Perguntar ao usuário** quem mais participou sem falar, apresentando os
     falantes detectados. Sem essa resposta, montar a linha só com os falantes e
     dizer explicitamente no relatório que a presença silenciosa não foi
     confirmada.
   - **Nunca inferir presença.** Estar citado em terceira pessoa ("o Fernando
     vai levantar isso") não é evidência de presença — é evidência do contrário
     com a mesma frequência.
   - Falante não identificado vira `Participante não identificado` e entra no
     relatório. Falante novo, com nome legível, entra no relatório como sugestão
     de inclusão no roster.
   - **Contas genéricas** (`Desenvolvimento 01` e similares) são pessoas reais
     atrás de um recurso compartilhado. Resolver pela tabela "Contas genéricas"
     do `NORMALIZACAO.md`; se não estiver lá, reportar — nunca deduzir.

   Ao detectar falantes, não presuma a forma do nome: o Teams grava nomes em
   minúsculas e contas de recurso com dígitos (`Desenvolvimento 01`).
   O padrão confiável é "qualquer texto seguido de timestamp no fim da linha".

   Para quem recebe tarefa mas não esteve na reunião, o vault já tem convenção:
   anotar `(<Empresa> — <Papel>, não presente)` no cabeçalho da seção de tarefas.
2. **Termos** — aplicar `NORMALIZACAO.md`. Substituições de escopo `sempre` são
   diretas; as de escopo `contexto` exigem ler a frase e decidir. Termos com ⚠️
   no glossário **não são substituídos** — são sinalizados.
3. **Ruído** — remover timestamps, linhas de sistema, muletas e falas de
   coordenação, conforme a seção "Ruídos a remover" do `NORMALIZACAO.md`.
4. **Precedente** — antes de fechar, comparar o vocabulário resultante com os
   `- Estruturado.md` anteriores. Se o mesmo conceito aparecer aqui com outra
   grafia, prevalece a grafia do glossário; se o glossário for omisso, prevalece
   a do documento anterior e o caso vai para o relatório.

### 4. Gerar o documento estruturado

Formato consolidado nos documentos já existentes — seguir exatamente:

```markdown
# <Nome do Projeto> — <Título da Reunião>
**Data:** <por extenso> | **Duração:** <hh h mm min ss s>
**Participantes:** <todos os presentes, falantes ou não> · ...

---

## Resumo

<2 a 4 parágrafos. O que se discutiu e o que ficou decidido. Termos de
domínio em negrito.>

---

## Tarefas Definidas / Pendências por Pessoa

### <Nome canônico> (<Empresa> — <Papel>)
- [ ] <ação explicitamente atribuída na reunião>

---

## Capítulos e Tópicos

### 1. <Tema>

#### 1.1 <Subtema>
- <fatos em bullets, termos canônicos em negrito>

**Ponto em aberto:** <quando a reunião não fechou o assunto>
```

Regras de conteúdo:

- Só entra em "Tarefas" o que foi atribuído explicitamente a alguém. Ação sem
  dono vira `**Ponto em aberto:**` no capítulo correspondente.
- `**Ponto em aberto:**` é o marcador padrão do vault para assunto não fechado.
- Preservar o português e o registro dos documentos existentes.
- Zero emojis no corpo do documento.

### 5. Relatório ao usuário

Depois de escrever o arquivo, **sempre** apresentar:

- **Falantes detectados** — quem falou, mapeado para qual nome canônico.
- **Presença silenciosa** — se foi confirmada pelo usuário, quem entrou na
  lista sem ter falado; se não, dizer que a lista contém apenas falantes e
  pode estar incompleta.
- **Participantes não resolvidos** — falantes que não bateram com o roster.
- **Termos novos** — recorrentes e ausentes do glossário, com contagem e a frase
  de contexto.
- **Conflitos** — mesmo conceito com grafias divergentes entre glossário,
  documentos anteriores e esta transcrição.
- **Trechos duvidosos** — inaudíveis ou incoerentes que podem esconder um termo
  de domínio.

Perguntar então se as entradas novas devem ser gravadas no glossário. Só depois
do aval, atualizar `GLOSSARIO.md`, `PARTICIPANTES.md` ou `NORMALIZACAO.md`,
subindo `version` e `last_review` no frontmatter.

## O que a skill não faz sozinha

- Não gera a ata em `_meetings/` — é outro artefato, com outro template
  (`_templates/tpl-reuniao.md`). Oferecer, não assumir.
- Não altera SPECs, backlog ou CONTEXT.md a partir da transcrição. Se a reunião
  mudar comportamento previsto, apontar o impacto e deixar a decisão com o
  usuário.
- Não apaga a transcrição bruta. O bruto é a evidência; o estruturado é a
  memória.
