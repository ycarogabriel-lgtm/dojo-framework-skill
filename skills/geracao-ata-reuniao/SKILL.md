---
name: geracao-ata-reuniao
description: Use quando um documento `*- Estruturado.md` de reunião do projeto precisar virar uma ATA de reunião em formato executivo, normalmente como `*- ATA.docx` em `_assets/docs/`. Dispara com "gerar ata", "converter Estruturado em ATA", "criar ATA de reunião", "ATA no modelo do projeto" ou pedidos para transformar o documento estruturado em ata.
---

# Geração de ATA de Reunião

Converte o documento estruturado de uma reunião em uma ATA executiva no padrão
usado pelo projeto.

## Qual ATA este documento é

O vault tem **dois artefatos de ata**, com propósitos distintos:

| Artefato | Onde | Formato | Para quê |
|---|---|---|---|
| **ATA executiva** | `_assets/docs/<base> - ATA.docx` | DOCX | Entregável enviado ao cliente |
| **Ata de reunião** | `_meetings/<data>-<tema>.md` | Markdown com frontmatter | Memória do vault, template `_templates/tpl-reuniao.md` |

**Esta skill gera apenas o primeiro.** A ata do `_meetings/` é outro documento,
com outra estrutura, e não é substituída por esta.

## Precedente de formato

Antes de gerar uma ATA nova, procure em `_assets/docs/` a ATA executiva mais
recente já entregue neste projeto e siga o formato dela — cabeçalho, ordem de
seções e agrupamento de participantes evoluem com o tempo, e a versão mais
recente é sempre a referência, não a mais antiga. Se houver mais de uma
geração de formato no vault, confirme com o usuário qual delas é a atual
antes de usá-la como modelo.

Para consultar um modelo em `.docx`, converta-o com o script da skill de
normalização:

```bash
python .claude/skills/normalizacao-transcricao/scripts/docx_to_text.py \
  "_assets/docs/<modelo>.docx"
```

Se nenhum modelo existir ainda, siga o formato textual descrito nesta skill e
avise no relatório que não havia precedente no vault.

## Princípio inegociável

**ATA não é nova interpretação da transcrição.** Use o `*- Estruturado.md` como
fonte factual. O trabalho é reformatar, consolidar e tornar o documento
executivo, sem inventar presença, decisão, responsável, status ou prazo.

Quando o Estruturado trouxer ambiguidade, preserve a ambiguidade como
`Ponto em aberto` ou registre no relatório final. Não complete lacunas com
inferência.

## Insumos obrigatórios

Carregar antes de gerar a ATA:

| Arquivo | Uso |
|---|---|
| `produto/glossario/GLOSSARIO.md` | Vocabulário canônico de negócio do projeto |
| `produto/glossario/PARTICIPANTES.md` | Nome, empresa/organização e papel canônicos |
| `produto/glossario/NORMALIZACAO.md` | Variações aceitas e correções de termo |
| `_assets/docs/<base> - Estruturado.md` | Fonte factual da ata |
| Precedente mais recente em `_assets/docs/*- ATA.docx` | Modelo de formato e tom |

## Saída esperada

**Dois arquivos irmãos do Estruturado**, com o mesmo radical:

```text
<Projeto> - <Base> - Estruturado.md    (fonte)
<Projeto> - <Base> - ATA.md            (ATA versionável, fonte da verdade)
<Projeto> - <Base> - ATA.docx          (entregável para o cliente)
```

O `.md` é gerado primeiro e **fica no vault**: é diffável, pesquisável no
Obsidian e legível por agentes. O `.docx` é derivado dele. Sem o `.md`, uma
correção futura na ata seria invisível ao `git diff` e ilegível para a próxima
sessão.

O radical deve ser **idêntico** ao do Estruturado, byte a byte — é assim que o
pareamento entre os três arquivos é feito programaticamente.

## Formato da ATA

Seguir esta ordem:

```text
ATA DE REUNIÃO – <NOME DO PROJETO>
<Assunto / título executivo da reunião>

Data: <data por extenso ou "não informada na transcrição de origem">
Duração: <duração, quando houver>
Projeto: <Nome do Projeto>
Tipo de Reunião: <tipo factual do tema>

Participantes
<Organização 1>
<Nome> — <Papel>

<Organização 2>
<Nome> — <Papel>

Resumo
<2 a 4 parágrafos executivos>

1. <Capítulo>
1.1 <Subcapítulo>
- <ponto objetivo>

<N>. Tarefas Definidas / Pendências por Pessoa
<Pessoa> (<Organização> — <Papel>)
| Status | Ação |
|---|---|
| Pendente | <ação> |

<N+1>. Próximos Passos
- <passo consolidado>

Documento gerado com base na transcrição da reunião <...>.
```

**Numeração dinâmica.** `Tarefas` e `Próximos Passos` são as **duas últimas**
seções: se houver 6 capítulos temáticos, elas são a 7 e a 8. Nunca fixe um
número de seção a priori — conte os capítulos reais do documento.

**Travessões.** Use `–` (travessão curto) no título e `—` (travessão
longo) entre nome e papel. Não substituir por hífen.

**Duração.** Nem toda ATA tem o campo. Se o Estruturado não informar, omita a
linha em vez de escrever "não informada".

## Regras de transformação

### 1. Cabeçalho

- Título fixo: `ATA DE REUNIÃO – <NOME DO PROJETO>` (travessão curto, não hífen).
- Subtítulo: derivar do H1 do Estruturado, removendo o prefixo do nome do
  projeto e tornando o assunto mais executivo quando o próprio texto já
  sustentar isso.
- `Data` e `Duração`: copiar do cabeçalho do Estruturado. Se o modelo/usuário
  fornecer uma data corrigida, usar a corrigida e registrar no relatório.
- `Projeto`: sempre o nome canônico do projeto atual.
- `Tipo de Reunião`: usar categoria factual do tema, por exemplo
  `Alinhamento Técnico`, `Refinamento de Negócio`, `Review` ou
  `Governança`. Se não estiver claro, usar `não informado`.

### 2. Participantes

- Reorganizar a linha `Participantes` do Estruturado por organização, usando
  `PARTICIPANTES.md` para preencher papel canônico.
- Grupos: um por organização/empresa envolvida no projeto (ex.: consultoria e
  cliente), na ordem que o vault já usa em ATAs anteriores. A forma canônica
  do nome de cada organização é a que está em `PARTICIPANTES.md` — se as ATAs
  antigas usarem uma grafia diferente (hífen vs. underscore, abreviação vs.
  nome completo), corrigir para a forma canônica.
- Não incluir pessoa citada em terceira pessoa como participante.
- **Empresa/organização e papel vêm de `PARTICIPANTES.md`, não da ATA
  anterior.** ATAs já existentes podem conter atribuições incorretas. Ao
  regenerar uma ATA antiga, isso pode mudar empresa e cargo de pessoas num
  documento possivelmente já enviado ao cliente — **avisar o usuário antes**,
  não corrigir silenciosamente.
- Se alguém estiver no Estruturado com papel genérico ou divergente, preservar
  o nome e registrar a divergência no relatório.
- Remover parênteses descritivos do cabeçalho quando o papel canônico já
  resolver a informação.

### 3. Resumo

- Reusar o conteúdo de `## Resumo`, removendo marcação Markdown.
- Manter 2 a 4 parágrafos, com tom executivo e leitura fluida.
- Preservar decisões, consensos, riscos e pontos em aberto relevantes.
- Não usar negrito do Markdown no DOCX; transformar em texto normal com termos
  canônicos.

### 4. Capítulos e tópicos

- Converter `## Capítulos e Tópicos` em seções numeradas de ATA.
- Transformar bullets em bullets do Word, removendo `**`, crases e citações
  Markdown.
- Manter tabelas que representem comparação real, como prazos, fluxo, stack ou
  matriz de decisão.
- Converter blocos `> **Ponto em aberto:**` em parágrafo destacado começando
  por `Ponto em aberto:`.
- Não copiar separadores `---`.

### 5. Tarefas e pendências

- Converter cada pessoa/grupo de `## Tarefas Definidas / Pendências por Pessoa`
  em subtítulo seguido de tabela:

```text
<Nome> (<Organização> — <Papel>)
| Status | Ação |
|---|---|
| Pendente | ação de item `- [ ]` |
| Concluído | ação de item `- [x]` |
```

- Status aceitos: `Pendente`, `Concluído`, `Em aberto` quando o item não tiver
  checkbox claro.
- Manter grupo conjunto, como `Equipes <Org A> e <Org B> (conjunto)`, quando
  a responsabilidade for compartilhada.
- Só entra como tarefa o que já estiver explicitamente atribuído no
  Estruturado.

### 6. Próximos passos

- Criar seção final `Próximos Passos`.
- Preferir copiar a seção `### Próximos Passos` do Estruturado, quando existir.
- Se não existir, consolidar a partir das tarefas pendentes mais estruturantes,
  sem criar novas obrigações.

### 7. Rodapé textual

Encerrar com uma frase de origem:

```text
Documento gerado com base na transcrição da reunião <descrição>. Data e duração exatas não constavam na transcrição de origem.
```

Adaptar a segunda frase quando data e duração constarem no Estruturado.

## Geração do DOCX

Escreva primeiro o ` - ATA.md` e converta com o script da skill. Ele usa apenas
a biblioteca padrão do Python 3 — **não** requer `python-docx`, `pandoc` nem
LibreOffice:

```bash
python .claude/skills/geracao-ata-reuniao/scripts/md_to_docx.py \
  "_assets/docs/<base> - ATA.md" -o "_assets/docs/<base> - ATA.docx"
```

Markdown suportado pelo conversor: `#`/`##`/`###`, bullets `-`, tabelas
`| a | b |` (primeira linha vira cabeçalho), `**negrito**` e parágrafos.
Escrever a ATA dentro desse subconjunto.

Regras visuais:

- Documento limpo e formal, sem capa.
- Título principal (`#`) no topo, subtítulo logo abaixo como parágrafo.
- Metadados em linhas simples.
- Participantes em listas por organização.
- Capítulos com títulos numerados (`##`), subcapítulos com `###`.
- Tarefas em tabelas `Status | Ação`.
- Zero emojis.

### Reconstruir o `- ATA.md` de uma ATA legada

Quando existir `- ATA.docx` sem o `- ATA.md` correspondente, **extraia** o
Markdown do DOCX em vez de regerar a partir do Estruturado — regerar produziria
um `.md` que contradiz o `.docx` já entregue ao cliente:

```bash
python .claude/skills/geracao-ata-reuniao/scripts/docx_to_md.py \
  "_assets/docs/<base> - ATA.docx" -o "_assets/docs/<base> - ATA.md"
```

O extrator recupera títulos (por ranking de tamanho de fonte dentro do próprio
arquivo), bullets, tabelas e negrito. Confira o resultado: ATAs antigas podem
variar de estrutura interna — algumas trazem a lista inteira de participantes
num único parágrafo separado por quebras de linha.

### Verificação obrigatória

Depois de gerar, faça o round-trip e confira o resultado:

```bash
python .claude/skills/normalizacao-transcricao/scripts/docx_to_text.py \
  "_assets/docs/<base> - ATA.docx"
```

O texto extraído deve conter todas as seções na ordem esperada. Se algo sumiu,
o Markdown de origem saiu do subconjunto suportado.

## Relatório ao usuário

Depois de gerar a ATA, informar:

- arquivos criados (`- ATA.md` e `- ATA.docx`);
- Estruturado usado como fonte;
- se a data/duração foram copiadas, corrigidas ou permaneceram ausentes;
- participantes agrupados por organização;
- pendências/tarefas convertidas por status;
- divergências de nome, papel, termo ou ponto ambíguo;
- se a renderização/QA visual do DOCX foi concluída.

## O que a skill não faz sozinha

- Não volta à transcrição bruta para reinterpretar a reunião, salvo se o usuário
  pedir auditoria.
- Não altera o glossário sem aval explícito.
- Não cria backlog, SPEC, ADR ou decisão arquitetural a partir da ATA; apenas
  sinaliza impactos para decisão do usuário.
- Não apaga nem substitui o `*- Estruturado.md`.
