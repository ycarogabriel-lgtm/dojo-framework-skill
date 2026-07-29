---
phase: produto
deliverable: Roster canônico de participantes
owner: Performa_IT
status: draft
source: [atas em `_meetings/`, documentos estruturados em `_assets/docs/`]
related_issues:
version: 0.1
last_review: [data]
---

# Participantes — [Nome do Projeto]

Nomes canônicos das pessoas do projeto. Toda transcrição normalizada deve usar
a coluna **Nome canônico**, exatamente como escrita aqui.

A coluna **Variantes** lista as formas já observadas em transcrições (apelidos
usados em call, nomes parciais, erros de transcrição). Ela alimenta a
normalização — ver [NORMALIZACAO.md](NORMALIZACAO.md).

## Performa_IT

| Nome canônico | Papel | Variantes observadas |
|---|---|---|
| [Nome completo] | [Papel no projeto] | [Apelidos/formas curtas observadas] |

## [Organização do cliente]

| Nome canônico | Papel | Variantes observadas |
|---|---|---|
| [Nome completo] | [Papel no projeto] | [Apelidos/formas curtas observadas] |

---

## Homônimos — regra obrigatória de desambiguação

Se duas pessoas do projeto compartilham primeiro nome ou apelido, registrar
aqui explicitamente qual delas cada artefato existente já assume por padrão, e
qual sinal de contexto aponta para a outra pessoa. Sem essa seção, uma skill de
normalização não tem como saber qual delas está sendo citada quando o nome
aparece isolado.

| Quem | Onde aparece |
|---|---|
| [Pessoa A] | [Contexto em que "Nome" isolado aponta para essa pessoa] |
| [Pessoa B] | [Contexto em que aponta para a outra] |

## Menções resolvidas

Registrar aqui casos em que um nome citado em transcrição estava **errado na
origem** (o falante trocou o nome), não apenas mal transcrito — e a evidência
usada para resolver. Isso importa porque corrigir esses casos silenciosamente
pode mudar responsável/empresa/cargo em documentos já entregues ao cliente.

### "[Nome citado incorretamente]" → [Nome canônico correto]

[Evidência: trecho da transcrição, data, e por que a atribuição original estava errada.]

**Lição para a skill:** um nome dito em call pode estar errado na origem, não
só mal transcrito. Nome de pessoa associado a organização externa deve ser
conferido contra este roster antes de virar responsável por item de ação.

## Notas de padronização

- **Preposições em minúsculas** em nomes compostos (ex.: "... **da** ...", "... **dos** ..."). Ferramentas de transcrição costumam gravar com maiúscula — corrigir.
- Apelidos e sobrenomes usados como tratamento são **forma curta válida em prosa**; o nome completo é obrigatório apenas em listas de participantes e cabeçalhos.
- Ao normalizar, sempre grafar o nome completo na linha de participantes do cabeçalho; no corpo, a forma curta é aceitável desde que não seja ambígua.
