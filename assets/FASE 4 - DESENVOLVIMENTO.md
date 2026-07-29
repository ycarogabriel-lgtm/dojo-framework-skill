# FASE 4 - DESENVOLVIMENTO

Esta fase tem início quando dois pré-requisitos estão atendidos: os protótipos das primeiras jornadas foram validados pelo cliente na [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md) e o ambiente de desenvolvimento está devidamente preparado conforme a [FASE 3 - ARQUITETURA](FASE%203%20-%20ARQUITETURA.md). O desenvolvimento acontece em ciclos semanais curtos — chamados aqui de **BOLTS**, em referência ao conceito do **AI-DLC (AI-Driven Development Lifecycle)** —, com foco máximo em entrega de valor e mínimo de rituais. A equipe trabalha em contato constante e reserva no máximo **3 a 4 horas por semana** para ritos formais (reuniões e cerimônias), sendo que a única reunião recorrente com o cliente é a **REVIEW SEMANAL**.

A filosofia central desta fase é a do **AI-DLC**: o agente de IA não é apenas um assistente que responde perguntas — ele é um **colaborador ativo que propõe planos, faz perguntas, decompõe tarefas e gera implementações completas**. Cabe ao engenheiro o papel de validador, aprovador e guardião da qualidade técnica e da arquitetura. O engenheiro inicia a conversa com intenção e contexto; o agente assume a condução, propõe o caminho e executa após aprovação humana.

> **Referência:** Este processo é baseado nos princípios do [AI-DLC (AI-Driven Development Lifecycle)](https://prod.d13rzhkk8cj2z0.amplifyapp.com), metodologia que reimagina o ciclo de desenvolvimento de software com IA como protagonista e o ser humano como aprovador em pontos críticos de decisão.

---

## ETAPA 1: Finalização do Contexto e Preparação do Backlog

Esta etapa acontece **uma única vez**, no início da fase de desenvolvimento. O `CONTEXT.md` e o `AGENT_RULES.md` foram inicializados em conjunto pelo arquiteto e pelo engenheiro na [FASE 3 - ARQUITETURA](FASE%203%20-%20ARQUITETURA.md) Etapa 6. Cabe agora ao engenheiro **complementar e finalizar** esses dois documentos com todos os artefatos produzidos nas fases anteriores, tornando-os prontos para consumo pelos agentes de IA ao longo de todo o desenvolvimento.

### 1.1 — Finalização do `CONTEXT.md`

O `CONTEXT.md` é o **fio condutor** do projeto para os agentes de IA — o documento que garante que o agente compreenda o projeto como um todo, independentemente da funcionalidade que estiver sendo trabalhada. Deve ser finalizado com base em todos os artefatos gerados nas fases anteriores e conter, no mínimo:

1. **INTENT DO PROJETO** — a declaração formal de propósito extraída da [FASE 1](FASE%201%20-%20PREVENDA.md), que ancora todas as decisões do projeto
2. **Propósito e contexto do projeto** — o problema que a solução resolve e o valor de negócio esperado
3. **Lista de Jornadas e Funcionalidades** — completa, com status de cada item (pendente / em desenvolvimento / concluída), extraída dos documentos da [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md)
4. **Referências ao Design do Projeto** — links diretos para os `DESIGN.md` de cada jornada e para os arquivos de design no Google Stitch, Figma Make ou Claude Design
5. **Visão macro da arquitetura e tecnologias** — resumo objetivo das decisões de arquitetura, linguagens, frameworks e serviços principais, com referência ao **DOCUMENTO DE ARQUITETURA DO PROJETO** completo
6. **Riscos relevantes** — síntese dos riscos do **REGISTRO DE RISCOS** que têm impacto direto no desenvolvimento, para que o agente os considere nas implementações
7. **Referências cruzadas** — links para todos os documentos relevantes do projeto (`SPEC_*.md`, `AGENT_RULES.md`, DOCUMENTO DE ARQUITETURA DO PROJETO, DOCUMENTOS DE REFINAMENTO)

O `CONTEXT.md` é um **documento vivo**: o agente de IA deve atualizá-lo ao longo do projeto sempre que uma nova funcionalidade for concluída (atualizando o status) ou quando houver mudanças de escopo aprovadas. O engenheiro revisa e valida cada atualização feita pelo agente.

### 1.2 — Finalização do `AGENT_RULES.md`

O `AGENT_RULES.md` configura o comportamento e as restrições do agente de IA para o projeto. Foi inicializado na [FASE 3](FASE%203%20-%20ARQUITETURA.md) com as regras arquiteturais — cabe ao engenheiro complementá-lo com as regras de processo e qualidade. O documento final deve conter:

1. **Regras de arquitetura** — padrões obrigatórios extraídos do DOCUMENTO DE ARQUITETURA DO PROJETO: estrutura de pastas, nomenclatura, padrões de design obrigatórios (ex: CQRS, Repository Pattern), serviços e bibliotecas aprovados
2. **NFRs como restrições de implementação** — os Requisitos Não-Funcionais definidos na arquitetura (tempos de resposta, limites de carga, estratégias de escalabilidade) devem ser tratados pelo agente como restrições a respeitar em cada implementação
3. **Regras de segurança** — padrões obrigatórios de segurança vindos da arquitetura: estratégia de autenticação/autorização, gerenciamento de secrets, criptografia, validação de entradas, headers de segurança de API
4. **Regras de qualidade** — critérios mínimos de cobertura de testes unitários, ausência de warnings de lint, build limpo obrigatório
5. **Instruções de teste** — o agente deve sempre criar testes unitários baseados nos critérios de aceite e cenários de teste definidos na `SPEC_{FUNCIONALIDADE}.md`
6. **Instrução de code review cruzado** — ao finalizar a implementação, o agente aciona um segundo modelo de IA para revisão de código (ex: desenvolvido com Claude Sonnet → revisado pelo Codex), registrando apontamentos e resoluções
7. **Instruções de atualização de documentos** — o agente deve atualizar o `CONTEXT.md` ao concluir cada funcionalidade
8. **Dependências proibidas** — tecnologias, bibliotecas ou padrões que não devem ser utilizados no projeto, conforme definido na arquitetura

### 1.3 — Criação do Backlog Inicial

Com base nos **DOCUMENTOS DE REFINAMENTO** por funcionalidade produzidos na [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md), o engenheiro — com apoio do agente de IA — cria o **backlog inicial** do projeto. O agente lê todos os documentos de refinamento disponíveis e organiza os itens de backlog com uma ordenação lógica baseada em dependências técnicas entre funcionalidades e prioridades de negócio. O resultado deve ser um backlog estruturado em ferramenta de gestão de projetos (ex: Jira), com cada funcionalidade representada como um item rastreável, ligado à sua jornada e ao seu entregável correspondente.

* **INPUTS:**
  - **MEMÓRIA DO PROJETO** e **INTENT DO PROJETO** da [FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md)
  - **REGISTRO DE RISCOS** (versão mais recente)
  - **DOCUMENTOS DE REFINAMENTO** por funcionalidade da [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md)
  - `DESIGN.md` de cada jornada prototipada ([FASE 2](FASE%202%20-%20DISCOVERY.md))
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** da [FASE 3 - ARQUITETURA](FASE%203%20-%20ARQUITETURA.md)
  - `CONTEXT.md` e `AGENT_RULES.md` inicializados na [FASE 3](FASE%203%20-%20ARQUITETURA.md)

* **OUTPUTS:**
  - `CONTEXT.md` — finalizado e pronto para uso pelos agentes (documento vivo)
  - `AGENT_RULES.md` — finalizado com todas as regras de arquitetura, NFRs, segurança, qualidade e processo
  - Backlog inicial estruturado com todas as funcionalidades priorizadas

---

## ETAPA 2: Planejamento do Bolt Semanal

No início de cada semana o engenheiro seleciona do backlog as funcionalidades a serem desenvolvidas naquele **BOLT** (ciclo semanal). A seleção considera a prioridade de negócio, as dependências técnicas entre funcionalidades e a capacidade realista de entrega em uma semana. O planejamento do bolt não exige cerimônia formal — é uma decisão técnica do engenheiro, alinhada com o designer quando houver dependência de novos protótipos ou validações de UX.

* **INPUTS:**
  - Backlog priorizado
  - Resultado da **REVIEW SEMANAL** anterior (feedbacks, ajustes de prioridade, novos refinamentos)

* **OUTPUTS:**
  - Lista de funcionalidades a desenvolver no bolt atual, com critérios de aceite claros

---

## ETAPA 3: Especificação da Funcionalidade (Etapa Recorrente)

Para cada funcionalidade a ser desenvolvida no bolt, o engenheiro cria o documento `SPEC_{FUNCIONALIDADE}.md` — a tradução do **O QUE** (definido no **DOCUMENTO DE REFINAMENTO** da [FASE 2](FASE%202%20-%20DISCOVERY.md)) para o **COMO** (definição técnica de implementação). Este é o principal documento de entrada do agente de IA para o desenvolvimento de cada funcionalidade.

A especificação deve conter:

1. **Propósito e contexto** — o que esta funcionalidade faz e qual problema resolve, alinhado ao **INTENT DO PROJETO**
2. **Referência ao DOCUMENTO DE REFINAMENTO** — link direto ao documento estruturado da funcionalidade produzido na [FASE 2](FASE%202%20-%20DISCOVERY.md), que contém regras de negócio, permissões, entradas/saídas e critérios de aceite
3. **Referência ao design e protótipo** — link para o `DESIGN.md` da jornada correspondente e para os arquivos de design no Google Stitch, Figma Make ou Claude Design
4. **Definição técnica de como será construída** — arquitetura interna da funcionalidade: componentes, serviços, chamadas de API, modelos de dados, padrões aplicados
5. **Considerações de NFRs e segurança** — restrições específicas desta funcionalidade derivadas dos NFRs e das regras de segurança definidas na arquitetura (ex: "esta API deve responder em até 200ms", "este endpoint requer autenticação JWT com perfil X")
6. **Cenários de teste** — casos de teste derivados dos critérios de aceite do DOCUMENTO DE REFINAMENTO, que o agente transformará em testes unitários automatizados

Antes de iniciar o desenvolvimento com o agente, o engenheiro revisa a especificação para garantir completude e aderência à arquitetura. O designer pode ser consultado pontualmente para confirmar referências ao `DESIGN.md`.

* **INPUTS:**
  - **DOCUMENTO DE REFINAMENTO** da funcionalidade ([FASE 2](FASE%202%20-%20DISCOVERY.md))
  - `DESIGN.md` da jornada correspondente ([FASE 2](FASE%202%20-%20DISCOVERY.md))
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** ([FASE 3](FASE%203%20-%20ARQUITETURA.md))
  - `CONTEXT.md` e `AGENT_RULES.md`
  - **REGISTRO DE RISCOS** (para verificar se há riscos associados à funcionalidade)

* **OUTPUTS:**
  - `SPEC_{FUNCIONALIDADE}.md` — especificação técnica completa da funcionalidade

---

## ETAPA 4: Desenvolvimento da Funcionalidade com Agente de IA (Etapa Recorrente)

Esta é a etapa central do ciclo de desenvolvimento. Ela segue a lógica fundamental do **AI-DLC**: **o agente propõe, o engenheiro aprova, o agente executa**. O fluxo abaixo é seguido para cada funcionalidade a ser desenvolvida.

### 4.1 — Leitura de Contexto e Perguntas do Agente

O engenheiro inicia a sessão fornecendo ao agente os seguintes documentos como contexto:

- `CONTEXT.md`
- `AGENT_RULES.md`
- `SPEC_{FUNCIONALIDADE}.md`
- `DESIGN.md` da jornada correspondente — referência primária para decisões de UI/UX
- **DOCUMENTO DE ARQUITETURA DO PROJETO** (SAD/ADRs)
- Acesso via MCP à ferramenta de design (Google Stitch, Figma Make ou Claude Design) para consulta direta aos protótipos quando necessário

O agente deve ser instruído a **ler todos os documentos, identificar eventuais lacunas ou ambiguidades e fazer perguntas ao engenheiro antes de propor qualquer plano**. Nenhuma decisão crítica deve ser tomada de forma autônoma — qualquer ponto não claro deve ser explicitamente levantado. Esta etapa é fundamental para garantir entendimento completo antes de avançar.

### 4.2 — Geração e Validação do Plano (PLAN MODE)

Com todas as dúvidas esclarecidas, o agente gera um **plano detalhado de implementação** antes de escrever qualquer linha de código. O plano deve:

1. Listar todos os passos da implementação em formato de checklist (arquivo markdown com checkboxes)
2. Indicar quais arquivos serão criados ou modificados
3. Descrever a abordagem técnica para cada componente da funcionalidade
4. Listar os testes unitários que serão criados, mapeados aos critérios de aceite

O engenheiro revisa o plano, sugere ajustes se necessário e, quando estiver de acordo, aprova explicitamente. **O agente não deve iniciar a implementação sem a aprovação do engenheiro.** Este é o principal ponto de controle humano do ciclo de desenvolvimento.

### 4.3 — Implementação

Com o plano aprovado, o agente executa a implementação passo a passo, marcando cada item do checklist à medida que conclui. Durante a implementação, o agente deve:

1. **Desenvolver o código** seguindo rigorosamente o plano aprovado, a arquitetura definida, os NFRs e as regras de segurança do `AGENT_RULES.md`
2. **Criar os testes unitários** baseados nos critérios de aceite e cenários de teste da `SPEC_{FUNCIONALIDADE}.md`, garantindo a cobertura mínima definida no `AGENT_RULES.md`
3. **Executar validações de qualidade** — lint, warnings, análise estática — corrigindo qualquer problema antes de prosseguir
4. **Garantir o build limpo** de todos os artefatos do projeto após a implementação
5. **Acionar o code review por segundo agente** — submeter o código a um segundo modelo de IA (ex: desenvolvido com Claude Sonnet → revisado pelo Codex) e registrar apontamentos e resoluções num relatório de review
6. **Atualizar o `CONTEXT.md`** — registrar a funcionalidade como concluída e atualizar qualquer informação relevante

### 4.4 — Revisão e Testes pelo Engenheiro

Com a implementação concluída pelo agente, o engenheiro realiza a revisão humana:

1. **Code review** — revisão do código gerado, com foco em qualidade, aderência à arquitetura, NFRs e regras de segurança
2. **Execução dos testes** — verificação dos testes criados pelo agente e execução de testes manuais complementares
3. **Commit e push** — após aprovação, o engenheiro realiza o commit seguindo a convenção definida na arquitetura

A pipeline de CI/CD configurada na [FASE 3](FASE%203%20-%20ARQUITETURA.md) assume automaticamente: executa testes automatizados, envia resultados ao SonarQube e, se aprovado nos critérios de quality gate, realiza o **deploy automático para o ambiente de DEV**.

### 4.5 — Validação pelo Designer

Com a funcionalidade publicada no ambiente de DEV, o designer realiza a validação visual e funcional tendo o **`DESIGN.md`** como referência oficial — verificando aderência às decisões de design, tokens do design system, comportamentos de interface e protótipos. Caso haja discrepâncias, o designer registra os ajustes necessários e o engenheiro os resolve com apoio do agente antes de considerar a funcionalidade concluída.

Uma funcionalidade é considerada **PRONTA** quando todos os critérios abaixo estão atendidos:

- ✅ Publicada no ambiente de DEV
- ✅ Cobertura mínima de testes atingida
- ✅ SonarQube aprovado nos critérios definidos na arquitetura
- ✅ Build limpo sem warnings
- ✅ Validação do designer concluída com base no `DESIGN.md`

* **INPUTS:**
  - `CONTEXT.md`
  - `AGENT_RULES.md`
  - `SPEC_{FUNCIONALIDADE}.md`
  - `DESIGN.md` da jornada correspondente
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** (SAD/ADRs)
  - Acesso MCP ao Google Stitch / Figma Make / Claude Design

* **OUTPUTS:**
  - Código da funcionalidade implementado, testado e publicado no ambiente de DEV
  - Testes unitários automatizados
  - Relatório de code review pelo segundo agente
  - `CONTEXT.md` atualizado
  - Funcionalidade marcada como **PRONTA** no backlog

---

## ETAPA 5: Review Semanal com o Cliente (Etapa Recorrente)

Ao final de cada bolt (semana), realiza-se a única reunião recorrente formal com o cliente. Deve ser objetiva e não ultrapassar **1h15min**, seguindo a agenda abaixo:

| Bloco | Duração | Conteúdo |
|---|---|---|
| **Review** | 30 min | Demonstração ao vivo das funcionalidades concluídas no bolt, no ambiente de DEV |
| **Refinamento** | 30 min | Alinhamento e esclarecimento de dúvidas sobre as funcionalidades do próximo bolt |
| **Dúvidas e Bloqueios** | 15 min | Questões abertas, feedbacks gerais, riscos e próximos passos |

Durante o bloco de **Review**, verificam-se as **MÉTRICAS DE SUCESSO** definidas na [FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md), apresentando evidências objetivas do progresso em relação a elas. Novos riscos identificados durante o bolt devem ser registrados no **REGISTRO DE RISCOS** e, quando relevantes, comunicados ao arquiteto.

Caso durante o **Refinamento** surja uma lacuna de design ou especificação não coberta pelos documentos existentes, o processo retorna à [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md) para os ajustes necessários (refinamento adicional, atualização de protótipo, novo `DESIGN.md`) antes de o item entrar no backlog.

* **INPUTS:**
  - Funcionalidades concluídas no bolt atual, publicadas no ambiente de DEV
  - Backlog atualizado
  - **MÉTRICAS DE SUCESSO** do projeto
  - **REGISTRO DE RISCOS** (versão mais recente)

* **OUTPUTS:**
  - Feedback do cliente sobre as entregas do bolt
  - Refinamento das funcionalidades do próximo bolt
  - Backlog atualizado com prioridades e ajustes
  - **REGISTRO DE RISCOS** atualizado (quando novos riscos forem identificados)
  - Eventuais retornos à [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md) para lacunas identificadas

---

> O ciclo das **ETAPAS 2 a 5** repete-se semanalmente até que todas as funcionalidades do escopo estejam concluídas e validadas, momento em que o projeto avança para a [FASE 5 - TESTES FUNCIONAIS](FASE%205%20-%20TESTES%20FUNCIONAIS.md).
