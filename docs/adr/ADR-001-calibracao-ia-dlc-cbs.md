---
scope: framework
deliverable: Architecture Decision Record
owner: Performa_IT
status: proposed
source: [skills/cbs-completo/SKILL.md; templates/tpl-cbs.md; assets/FASE 4 - DESENVOLVIMENTO.md]
related_issues:
version: 0.1
last_review: 2026-08-06
---

# ADR-001 — Calibração das estimativas do CBS para desenvolvimento AI-DLC

## Status

**Proposed** — aguardando aprovação do dono do repositório.

## Contexto

O CBS (Cost Breakdown Structure) gerado pela skill `cbs-completo` (ETAPA C) é o
insumo direto da `PROPOSTA COMERCIAL`. Hoje ele estima horas a partir de duas
tabelas de referência fixas (uma de FE, uma de BE), rotuladas "com IA" e
replicadas em `skills/cbs-completo/SKILL.md` e `templates/tpl-cbs.md`.

O problema reportado pelo time: **as estimativas estão saindo altas demais** em
relação ao esforço real de entrega, num contexto em que o desenvolvimento é
feito com **uso massivo de IA**. Isso custa competitividade em proposta e, pior,
cria uma discrepância entre o número vendido e o número realizado que corrói a
confiança na própria ferramenta de estimativa.

Ao analisar as tabelas atuais, o problema não é só a magnitude — é o **modelo**:

1. **O fator de IA é opaco.** As tabelas dizem "com IA" e a premissa global diz
   "produtividade com IA já incorporada", mas nenhum lugar explicita *quanto* de
   ganho foi assumido nem *por quê*. Sem isso, o estimador ancora nos números
   convencionais que conhece e a "incorporação" da IA vira um desconto tímido e
   arbitrário. Não há como auditar, contestar ou corrigir uma premissa que não
   está escrita.
2. **O ganho é tratado como uniforme.** Autenticação, CRUD e formulário — onde a
   IA gera código quase pronto a partir de padrões amplamente representados —
   recebem o mesmo tratamento implícito que migração de dados sujos e integração
   com API de terceiro não documentada, onde o gargalo é descoberta empírica e
   negociação com o mundo externo, não velocidade de digitação. Uma tabela plana
   necessariamente superestima o primeiro grupo e subestima o segundo.
3. **Os buffers só somam, nunca subtraem.** Existe "+10–15% sem gravação" e
   "+30–50% API não documentada", mas nada reconhece as condições *favoráveis*
   que o próprio Dojo Framework produz (DESIGN.md aprovado, CONTEXT.md e
   AGENT_RULES.md preenchidos, SPEC por funcionalidade antes do bolt). O viés do
   modelo é estruturalmente para cima.
4. **Não há curva de reúso.** A 5ª tela de listagem de um projeto custa uma
   fração da 1ª — o design system já existe, os componentes já existem, o agente
   já tem exemplos no repositório. A tabela cobra as cinco pelo mesmo preço, e é
   exatamente esse efeito que a IA mais amplifica.
5. **A metodologia e a estimativa estão desalinhadas.** A `FASE 4 —
   DESENVOLVIMENTO` já define o AI-DLC como o modelo de entrega, com o agente
   propondo planos e gerando implementações completas e o engenheiro atuando
   como validador. O CBS ainda precifica um caminho convencional com desconto.

Força contrária, que qualquer solução precisa respeitar: **estimativa baixa
demais é tão cara quanto estimativa alta demais.** Alta perde a venda; baixa
ganha a venda e queima o projeto. E parte do esforço é irredutível — ler a SPEC,
revisar o código gerado, validar com o cliente, ajustar, aprovar o PR — mesmo
quando o código sai pronto de primeira.

## Decisão

Substituir a tabela plana "com IA" por um **modelo de alavancagem explícito**,
com três componentes e um gate de pré-condições:

```
Horas = Base_convencional × Fator_IA(categoria) × Fator_Reúso(ordinal)
        respeitado o piso de overhead humano por feature
```

1. **Tabelas com duas colunas** — `Base (convencional)` e `IA-DLC`, lado a lado,
   com o fator implícito visível. O estimador vê o número de onde partiu, o
   número que vai usar e o desconto assumido, tudo na mesma linha.
2. **Fator de IA diferenciado por categoria de trabalho** — de **0,35×** (código
   padrão, amplamente representado: auth, CRUD, formulário, toasts) a **0,75×**
   (trabalho onde o gargalo é externo ou empírico: migração de dados, integração
   complexa com terceiro). Média em torno de 0,5×.
3. **Fator de reúso** — 1ª ocorrência de um padrão no projeto 1,0×; 2ª–3ª 0,7×;
   4ª em diante 0,5×, aplicado sobre a coluna IA-DLC.
4. **Piso de overhead humano** — nenhuma feature abaixo de 2h FE ou 2h BE. É o
   custo irredutível de ler a SPEC, revisar o que o agente gerou, validar e
   aprovar. Impede que a composição dos fatores leve o número a zero.
5. **Gate de pré-condições de alavancagem** — a coluna IA-DLC só é válida se as
   condições que a sustentam forem verdadeiras (DESIGN.md aprovado, CONTEXT.md +
   AGENT_RULES.md preenchidos, SPEC por funcionalidade, stack conhecida, base de
   código com testes ou greenfield, time treinado em AI-DLC). Se alguma falhar,
   a orientação é explícita: usar a coluna Base para a parte afetada.

O gate é o que torna o número baixo **defensável**: ele não é otimismo, é o
preço de um caminho de entrega específico que o Dojo Framework produz. Se o
projeto não seguir esse caminho, a estimativa não se aplica.

## Alternativas consideradas

### Opção A — Desconto linear único sobre as tabelas atuais

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo de implementação | Uma linha de premissa |
| Precisão | Baixa |
| Auditabilidade | Baixa |

**Prós:** resolve o sintoma imediatamente; nada a manter.
**Contras:** mantém os quatro defeitos estruturais do modelo. Superestima o
trabalho de alta alavancagem e subestima migração e integração — os dois itens
que mais estouram na prática. Um desconto global esconde onde está o risco.

### Opção B — Fator de alavancagem diferenciado por categoria (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo de implementação | Reescrita das tabelas nos dois arquivos |
| Precisão | Alta (e corrigível por realizado) |
| Auditabilidade | Alta — cada fator é visível e contestável |

**Prós:** o desconto fica onde é real e não fica onde não é; qualquer número
pode ser contestado linha a linha em revisão; o gate de pré-condições dá
argumento comercial para o número baixo; cria o gancho de calibração por dados
reais (estimado × realizado por bolt).
**Contras:** duas colunas por tabela custam leitura; exige disciplina de manter
`SKILL.md` e `tpl-cbs.md` em sincronia; os fatores iniciais são julgamento de
engenharia, não medição — precisam ser corrigidos por realizado.

### Opção C — Abandonar horas por feature e estimar por capacidade de bolt

| Dimensão | Avaliação |
|---|---|
| Complexidade | Alta |
| Custo de implementação | Alto — muda CBS, proposta comercial e backlog |
| Precisão | Alta depois de calibrado, imprevisível antes |
| Auditabilidade | Média |

**Prós:** alinhado com o AI-DLC de verdade — o time entrega por bolt, não por
hora; elimina a ficção da hora-feature.
**Contras:** o CSV do CBS alimenta a proposta comercial e o Jira, ambos
ancorados em horas; a mudança se propagaria por `tpl-proposta-comercial.md`,
`tpl-memoria-projeto.md` e o fluxo de backlog. Não resolve o problema reportado
(número alto) — só troca a unidade. Vale reavaliar quando houver histórico de
velocidade real por bolt.

### Opção D — Manter as tabelas e aplicar desconto comercial no preço

| Dimensão | Avaliação |
|---|---|
| Complexidade | Nenhuma no framework |
| Custo de implementação | Zero |
| Precisão | Inalterada (errada) |
| Auditabilidade | N/A |

**Prós:** não toca em nada técnico; a decisão fica com quem precifica.
**Contras:** trata como problema comercial o que é problema de modelo de
estimativa. O time continua planejando bolts com números inflados, e a margem
some no desconto em vez de aparecer como ganho de produtividade real.

## Análise de trade-offs

O eixo central é **precisão × custo de manutenção**. A Opção A é grátis e
imprecisa; a C é precisa e cara, e exige um histórico que ainda não existe. A B
compra a maior parte do ganho de precisão ao custo de manter duas tabelas
sincronizadas — um custo real, mas contido, porque as tabelas já viviam
duplicadas nos mesmos dois arquivos antes desta mudança.

O segundo eixo é **risco comercial**. Baixar número sem explicar por quê
transfere risco para a entrega. O gate de pré-condições e o piso de overhead
humano existem para conter exatamente isso: o número baixo vem acompanhado da
condição que o torna verdadeiro, e há um chão abaixo do qual a composição de
fatores não passa.

Assumido explicitamente: **os fatores desta primeira versão são julgamento de
engenharia, não medição.** A calibração por dados reais (estimado × realizado ao
fim de cada bolt) está prevista nas ações abaixo e é o que transforma este
modelo de hipótese em ferramenta.

## Consequências

**O que fica mais fácil**
- Propostas competitivas sem desconto comercial artificial mascarando a margem.
- Contestar uma estimativa em revisão: o fator está escrito e é discutível.
- Diferenciar risco no CBS — migração e integração agora aparecem como os itens
  caros que de fato são, em vez de diluídos numa média.
- Justificar o número para o cliente: ele vem com as pré-condições anexadas.

**O que fica mais difícil**
- Manter `skills/cbs-completo/SKILL.md` e `templates/tpl-cbs.md` sincronizados —
  toda mudança de tabela precisa acontecer nos dois.
- Estimar projeto que não segue o Dojo Framework: exige escolher conscientemente
  a coluna Base, e alguém vai esquecer.
- Comparar CBS novo com CBS antigo: os números não são da mesma régua. Propostas
  em aberto geradas com a régua antiga não devem ser reemitidas sem revisão.

**O que vamos precisar revisitar**
- Os fatores, depois de 3 a 5 projetos com realizado medido.
- O piso de 2h por feature — pode estar alto para features triviais em projeto
  maduro, ou baixo se o ciclo de validação com cliente for pesado.
- A Opção C (estimativa por bolt), quando houver histórico de velocidade real.

## Ações

1. [ ] Reescrever as tabelas FE/BE em `skills/cbs-completo/SKILL.md` com as duas
       colunas e o fator por categoria.
2. [ ] Espelhar em `templates/tpl-cbs.md` (fonte única do artefato versionado).
3. [ ] Adicionar o gate de pré-condições, o fator de reúso e o piso de overhead
       humano às duas fontes.
4. [ ] Atualizar as Premissas Globais para declarar a régua IA-DLC e as
       condições que a sustentam.
5. [ ] Registrar no resumo do CBS a seção "Fatores aplicados", para que cada
       proposta carregue a rastreabilidade do desconto assumido.
6. [ ] Bump de versão do plugin (mudança de comportamento, não de conteúdo).
7. [ ] **Pendente de dono do projeto:** instrumentar estimado × realizado por
       bolt na FASE 4 e revisar os fatores após 3–5 projetos.
8. [ ] **Pendente de decisão comercial:** definir o que fazer com propostas em
       aberto estimadas com a régua anterior.

## Links

- `skills/cbs-completo/SKILL.md` — ETAPA C, geração do CBS
- `templates/tpl-cbs.md` — template do artefato versionado
- `templates/tpl-proposta-comercial.md` — consumidor direto das horas do CBS
- `assets/FASE 1 - PREVENDA.md` — Etapas 1 e 2, onde o CBS é produzido
- `assets/FASE 4 - DESENVOLVIMENTO.md` — modelo AI-DLC que sustenta a régua
