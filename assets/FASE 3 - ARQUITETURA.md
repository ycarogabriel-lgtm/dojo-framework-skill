# FASE 3 - ARQUITETURA

Esta fase começa imediatamente após a aprovação da **PROPOSTA COMERCIAL** pelo cliente e ocorre **em paralelo** com as etapas da [FASE 2 - DISCOVERY](FASE%202%20-%20DISCOVERY.md). O arquiteto não integra a equipe do projeto de forma integral, mas é responsável pelas definições de arquitetura e pelo acompanhamento técnico da solução ao longo de todo o projeto, garantindo que a arquitetura e os padrões definidos sejam respeitados durante o desenvolvimento.

O principal artefato desta fase é o **DOCUMENTO DE ARQUITETURA DO PROJETO** — um documento markdown abrangente que consolida **todas** as decisões técnicas, padrões, restrições e definições de ambiente do projeto. Este documento é a **principal fonte de verdade técnica** para os agentes de IA na [FASE 4 - DESENVOLVIMENTO](FASE%204%20-%20DESENVOLVIMENTO.md): é a partir dele que o engenheiro popula o `CONTEXT.md` e o `AGENT_RULES.md`, garantindo que o agente de desenvolvimento opere dentro dos limites e padrões definidos pelo arquiteto.

---

## ETAPA 1: Entendimento do Projeto e Proposta Inicial de Arquitetura

O arquiteto inicia esta etapa lendo integralmente a **MEMÓRIA DO PROJETO**, o **INTENT DO PROJETO** e o **REGISTRO DE RISCOS** gerados na [FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md). O REGISTRO DE RISCOS é especialmente relevante neste momento, pois riscos técnicos de integração, performance, escalabilidade e segurança já identificados devem influenciar diretamente as decisões arquiteturais desde o início.

Com o contexto completo, o arquiteto aciona um agente de IA para liderar a geração do rascunho de arquitetura: o agente lê todos os documentos disponíveis, identifica restrições e requisitos técnicos implícitos, e propõe uma arquitetura inicial com a justificativa para cada decisão relevante. O arquiteto revisa a proposta do agente, ajusta o que for necessário com base no seu conhecimento técnico e de mercado, e produz o rascunho que será levado à reunião com o cliente.

* **INPUTS:**
  - **MEMÓRIA DO PROJETO** gerada na [FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md)
  - **INTENT DO PROJETO**
  - **REGISTRO DE RISCOS** (versão inicial da FASE 1, atualizada nas sessões de refinamento da FASE 2)

* **OUTPUTS:**
  - Rascunho da arquitetura sugerida com justificativas


---

## ETAPA 2: Coleta de Informações e Validação com o Cliente

O arquiteto realiza uma reunião com o cliente para coletar informações sobre padrões adotados, ambientes existentes, infraestrutura disponível ou desejada para o projeto, e para solicitar os acessos necessários à preparação do ambiente. Esta reunião pode ser realizada em sequência ou em conjunto com a reunião de Kick-Off da [FASE 2](FASE%202%20-%20DISCOVERY.md).

O arquiteto pode optar por já apresentar o rascunho preparado na [Etapa 1](#etapa-1-entendimento-do-projeto-e-proposta-inicial-de-arquitetura) para validação e alinhamento com o cliente. Ao final da reunião, o arquiteto deve ter condições de definir, de forma inequívoca, a arquitetura para o novo projeto.

* **INPUTS:**
  - **MEMÓRIA DO PROJETO**
  - **REGISTRO DE RISCOS**
  - Rascunho da arquitetura sugerida

* **OUTPUTS:**
  - Ajustes e refinamentos no rascunho de arquitetura
  - Informações adicionais coletadas com o cliente (padrões, acessos, restrições)
  - Transcrição da reunião de coleta com o cliente


---

## ETAPA 3: Definição e Documentação da Arquitetura

O arquiteto define e documenta toda a arquitetura do projeto no **DOCUMENTO DE ARQUITETURA DO PROJETO**. Este documento é estruturado em formato SAD (Solution Architecture Document) com ADRs (Architecture Decision Records) individuais para cada decisão relevante, acompanhado de diagramas C4 de níveis 1 e 2 em formato Mermaid — garantindo clareza visual e consumo eficiente pelos agentes de IA.

O documento deve cobrir **obrigatoriamente** os seguintes tópicos, cada decisão acompanhada de sua justificativa:

**1. Infraestrutura e Ambiente de Execução**
Definição do modelo de infraestrutura do projeto: Cloud (qual provedor) / On-Premises / Serverless / Containers / etc. Inclui a estratégia de ambientes (DEV, Staging, Produção) e os recursos de cada um.

**2. Bancos de Dados**
Escolha e justificativa dos bancos de dados: Relacional / NoSQL / Cache / Busca / etc., com identificação dos serviços específicos e suas responsabilidades no projeto.

**3. Tecnologias de Back-End e Front-End**
Linguagens, frameworks e bibliotecas principais para cada camada da solução, com as versões mínimas e as justificativas de escolha.

**4. Padrões de Arquitetura**
Estilo arquitetural adotado: Microsserviços / Monolito / Serverless / SSR / BFF / etc. Inclui os padrões de comunicação entre componentes (REST / gRPC / eventos / filas) e padrões de design obrigatórios (ex: CQRS, Circuit Breaker, Repository Pattern).

**5. Requisitos Não-Funcionais (NFRs)**
Definição quantitativa e qualitativa dos requisitos de: performance (tempos de resposta esperados, throughput), escalabilidade (estratégia de escalonamento horizontal/vertical), disponibilidade e SLA, tolerância a falhas, retenção e backup de dados, e limites de carga suportados. Esses requisitos se tornam restrições diretas para o agente de desenvolvimento na [FASE 4](FASE%204%20-%20DESENVOLVIMENTO.md).

**6. Arquitetura de Segurança**
Decisões de segurança que devem ser respeitadas em todo o desenvolvimento: estratégia de autenticação e autorização (OAuth2, JWT, RBAC, etc.), criptografia de dados em trânsito e em repouso, gerenciamento de secrets e variáveis de ambiente, segurança de APIs (rate limiting, validação de entrada, headers de segurança), e conformidade com regulamentações aplicáveis (LGPD, PCI, etc.).

**7. Ambiente de Desenvolvimento**
Definição dos repositórios de código-fonte, estratégia de branches (ex: GitFlow, trunk-based), ferramentas de análise de qualidade (SonarQube), critérios mínimos de aceite nas pipelines de CI (cobertura de testes, ausência de vulnerabilidades críticas, quality gate do SonarQube), e estratégia de CD para cada ambiente.

**8. Dependências Permitidas e Proibidas**
Lista de bibliotecas, serviços e integrações aprovadas para uso no projeto, bem como as explicitamente proibidas — com justificativa para cada restrição. Esta lista alimenta diretamente o `AGENT_RULES.md` da FASE 4.

**9. Diagramas de Arquitetura**
Diagramas C4 de Nível 1 (Contexto do Sistema) e Nível 2 (Containers) em formato Mermaid, para visualização clara da solução e entendimento pelos agentes de IA. Diagramas de Nível 3 (Componentes) devem ser criados para os módulos de maior complexidade.

* **INPUTS:**
  - **MEMÓRIA DO PROJETO**
  - **INTENT DO PROJETO**
  - **REGISTRO DE RISCOS** atualizado
  - Rascunho da arquitetura ajustado
  - Transcrição da reunião de coleta com o cliente

* **OUTPUTS:**
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** completo (SAD + ADRs + Diagramas C4 em Mermaid)


---

## ETAPA 4: Validação da Arquitetura com o Cliente (quando necessário)

Com a arquitetura definida, o arquiteto apresenta ao cliente os diagramas e as principais decisões técnicas, justificando cada escolha. O objetivo é obter validação formal e antecipar eventuais restrições ou preferências não capturadas anteriormente.

Caso ajustes sejam necessários, eles devem ser refletidos nos ADRs e nos diagramas correspondentes. A validação pode exigir mais de uma rodada até que o cliente aprove a arquitetura proposta. Todas as alterações devem ser registradas com data e justificativa nos ADRs.

* **INPUTS:**
  - **DOCUMENTO DE ARQUITETURA DO PROJETO**

* **OUTPUTS:**
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** atualizado com eventuais ajustes
  - Transcrição da reunião de validação com o cliente


---

## ETAPA 5: Preparação do Ambiente de Desenvolvimento

Esta etapa é realizada preferencialmente em conjunto com o engenheiro do projeto. O ambiente deve ser provisionado utilizando **Infraestrutura como Código (IaC)** — Terraform, AWS CDK, Pulumi ou equivalente, conforme definido na arquitetura — garantindo reprodutibilidade e rastreabilidade de todos os recursos criados.

Devem ser criados e validados, no mínimo, os seguintes recursos:

1. Ambiente de execução de **DEV** (provisionado via IaC)
2. Repositórios de código-fonte com acesso de escrita ao engenheiro do projeto
3. Estrutura de branches conforme a estratégia definida na arquitetura (ex: `dev`, `staging`, `main`)
4. Projetos no **SonarQube** para cada artefato técnico da solução
5. Pipelines de **CI** em cada repositório: build, testes automatizados, envio ao SonarQube e critérios de quality gate definidos na arquitetura
6. Pipelines de **CD** para deploy automático ao ambiente de DEV após aprovação no quality gate
7. Acesso do engenheiro a todas as ferramentas e ambientes necessários
8. Validação completa: execução end-to-end das pipelines e confirmação de que o ambiente de DEV está operacional

O código IaC de provisionamento deve ser versionado nos repositórios do projeto e servirá de base para a criação dos ambientes de Staging e Produção nas fases seguintes.

* **INPUTS:**
  - **DOCUMENTO DE ARQUITETURA DO PROJETO**

* **OUTPUTS:**
  - Ambiente de DEV provisionado e operacional (Repositórios, SonarQube, Pipelines CI/CD, Infraestrutura)
  - Código IaC versionado no repositório


---

## ETAPA 6: Apresentação da Arquitetura ao Engenheiro e Inicialização dos Documentos da FASE 4

O arquiteto apresenta ao engenheiro toda a arquitetura definida — explicando cada componente, justificando as decisões e garantindo entendimento completo. Esta apresentação deve cobrir também o ambiente de desenvolvimento preparado na etapa anterior, assegurando que o engenheiro tenha todos os acessos necessários.

Ao final desta etapa, arquiteto e engenheiro trabalham juntos para inicializar os dois documentos que guiarão o agente de IA durante toda a [FASE 4 - DESENVOLVIMENTO](FASE%204%20-%20DESENVOLVIMENTO.md):

- **`CONTEXT.md`** — o arquiteto contribui com a visão macro de arquitetura e tecnologias que deve compor o documento, garantindo que o agente tenha a visão técnica correta do projeto desde o início
- **`AGENT_RULES.md`** — extraído diretamente do **DOCUMENTO DE ARQUITETURA DO PROJETO**, deve incluir as regras de arquitetura obrigatórias, os NFRs como restrições de implementação, as regras de segurança, os padrões de design exigidos, os critérios de qualidade das pipelines e a lista de dependências permitidas e proibidas

Esses dois documentos nascem das definições arquiteturais, não de interpretação posterior — garantindo fidelidade total entre o que foi arquitetado e o que o agente irá implementar.

* **INPUTS:**
  - **DOCUMENTO DE ARQUITETURA DO PROJETO**
  - Ambiente de DEV provisionado

* **OUTPUTS:**
  - Engenheiro com pleno entendimento da arquitetura e acesso ao ambiente
  - `CONTEXT.md` e `AGENT_RULES.md` inicializados com as definições arquiteturais


---

## ETAPA 7: Acompanhamento Arquitetural durante o Desenvolvimento (Etapa Recorrente)

O papel do arquiteto não se encerra com a Etapa 6. Ao longo de toda a [FASE 4 - DESENVOLVIMENTO](FASE%204%20-%20DESENVOLVIMENTO.md), o arquiteto realiza **revisões periódicas** para garantir que a arquitetura e os padrões definidos estão sendo respeitados na implementação.

Recomenda-se que essas revisões ocorram ao início de cada novo **ENTREGÁVEL** sendo desenvolvido — momento em que o arquiteto analisa o código produzido até então, verifica a aderência arquitetural e atualiza o **DOCUMENTO DE ARQUITETURA DO PROJETO** sempre que decisões precisarem evoluir para acomodar necessidades identificadas no desenvolvimento.

Quando surgirem necessidades de mudança arquitetural relevantes, o arquiteto registra um novo ADR com a decisão, a motivação e o impacto, e comunica ao engenheiro para que o `AGENT_RULES.md` seja atualizado de forma correspondente.

* **INPUTS:**
  - Código produzido na [FASE 4](FASE%204%20-%20DESENVOLVIMENTO.md)
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** (versão vigente)
  - **REGISTRO DE RISCOS** (versão atualizada)

* **OUTPUTS:**
  - **DOCUMENTO DE ARQUITETURA DO PROJETO** atualizado (quando necessário)
  - `AGENT_RULES.md` atualizado (quando necessário)
  - Novos ADRs registrados para decisões de evolução arquitetural
