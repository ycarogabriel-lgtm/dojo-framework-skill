# FASE 2: DISCOVERY E REFINAMENTO

Nesta fase entra pela primeira vez a **[EQUIPE DO PROJETO](EQUIPE%20DO%20PROJETO.md)** definida para entregar o projeto. A equipe deve ler e internalizar integralmente a **MEMÓRIA DO PROJETO**, o **INTENT DO PROJETO**, o **REGISTRO DE RISCOS** e as **MÉTRICAS DE SUCESSO** gerados durante a **[FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md)** antes de qualquer contato com o cliente.

Esta fase segue o princípio do **AI-DLC** de inverter a direção da conversa: o agente de IA não apenas apoia a equipe — ele **lidera ativamente** a análise, propõe estruturas, gera documentos e faz perguntas. A equipe (designer e engenheiro) atua como validadora e aprovadora, refinando o que o agente propõe com base no seu conhecimento do cliente e do negócio.

> **Importante:** A FASE 2 é um processo em onda contínua. Ela não precisa estar completamente concluída para que a **[FASE 4 - DESENVOLVIMENTO](FASE%204%20-%20DESENVOLVIMENTO.md)** comece. Assim que as primeiras jornadas estiverem refinadas, prototipadas e validadas, o desenvolvimento pode e deve se iniciar — enquanto as demais jornadas continuam sendo refinadas em paralelo. Esse fluxo contínuo reduz o tempo de espera entre fases e maximiza a velocidade de entrega de valor ao cliente.

---

## ETAPA 1: Reunião de Kick-Off

O intuito desta reunião é o alinhamento claro entre a equipe do projeto e o cliente, e também a coleta dos insumos iniciais necessários para o processo de design. Antes da reunião, o agente de IA deve ler a **MEMÓRIA DO PROJETO** e preparar uma pauta estruturada com os pontos a serem validados e as informações a serem coletadas.

Na reunião, a equipe deve se apresentar e utilizar o momento para alinhar o entendimento do projeto, do escopo definido e aprovado de acordo com a **PROPOSTA COMERCIAL**, validando os **ENTREGÁVEIS** esperados e as **MÉTRICAS DE SUCESSO** acordadas.

Neste momento deve-se solicitar ao cliente os materiais necessários para a definição do **DESIGN SYSTEM**:

1. Guia de identidade visual da marca
2. Arquivos de logotipos e outras imagens necessárias
3. Capturas de tela de outros sistemas já existentes (quando aplicável)

Caso o **DESIGN SYSTEM** seja criado do zero, é importante pedir ao cliente referências de outros aplicativos ou websites que ele considera bons exemplos de layout, design e experiência — isso ajuda a calibrar o estilo esperado. Deve-se também definir claramente em quais dispositivos a solução será executada (desktop, mobile, tablet, touch/não-touch, etc.).

* **INPUTS:**
  - **MEMÓRIA DO PROJETO** gerada na [FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md)
  - **INTENT DO PROJETO**
  - **MÉTRICAS DE SUCESSO**

* **OUTPUTS:**
  - Escopo alinhado e confirmado com o cliente
  - Transcrição da reunião de Kick-Off
  - Materiais de identidade visual (guia de marca, logotipos, referências de design)
  - Definição dos dispositivos-alvo da solução


---

## ETAPA 2: Criação das PERSONAS, FUNCIONALIDADES, JORNADAS e do DESIGN SYSTEM

Com base na **MEMÓRIA DO PROJETO** e na transcrição do Kick-Off, o agente de IA **assume a liderança** desta etapa: ele lê todos os documentos disponíveis, analisa o **INTENT DO PROJETO** e os **ENTREGÁVEIS** definidos na proposta, e propõe ativamente a lista completa de **PERSONAS**, **FUNCIONALIDADES** e **JORNADAS** da solução — identificando as relações entre cada funcionalidade e o entregável correspondente. A equipe revisa, ajusta e aprova o que o agente propôs, complementando com o conhecimento do cliente e do contexto que não está documentado.

Na sequencia, o designer utiliza uma das ferramentas de design com IA para criar o **DESIGN SYSTEM** inicial da solução, a partir dos materiais de identidade visual coletados no Kick-Off. As ferramentas recomendadas são:

- **Google Stitch**
- **Figma Make**
- **Claude Design**

A escolha da ferramenta fica a critério do designer e pode variar conforme o projeto. É possível combinar mais de uma ao longo do processo.

Com as **PERSONAS**, **FUNCIONALIDADES** e **JORNADAS** definidas e o **DESIGN SYSTEM** criado, o agente gera automaticamente o **GUIA DE REFINAMENTO** — um documento estruturado com as perguntas e pontos de discussão específicos para cada **JORNADA** e suas **FUNCIONALIDADES**, identificando as lacunas de entendimento e os detalhes que precisam ser elucidados com o cliente. A equipe (designer e engenheiro) revisa e aprova o Guia antes de usá-lo nas sessões de refinamento.

* **INPUTS:**
  - **MEMÓRIA DO PROJETO** gerada na [FASE 1 - PREVENDA](FASE%201%20-%20PREVENDA.md)
  - Transcrição da reunião de Kick-Off
  - Materiais de identidade visual do cliente

* **OUTPUTS:**
  - Definição de **PERSONAS**
  - Definição de **FUNCIONALIDADES** e sua relação com os **ENTREGÁVEIS** da proposta
  - Diagrama de **JORNADAS** por **PERSONA**
  - **DESIGN SYSTEM** inicial
  - **GUIA DE REFINAMENTO** por **JORNADA** e suas **FUNCIONALIDADES**, gerado pelo agente e validado pela equipe


---

## ETAPA 3: Refinamento de JORNADAS e FUNCIONALIDADES (Etapa Recorrente)

Esta etapa é recorrente e acontece diversas vezes ao longo do projeto, garantindo o detalhamento completo de cada jornada e funcionalidade antes de serem prototipadas e desenvolvidas. É uma reunião com o cliente, conduzida pela equipe com base no **GUIA DE REFINAMENTO**, onde são discutidos e documentados os seguintes aspectos de cada **FUNCIONALIDADE**:

1. Respostas ao **GUIA DE REFINAMENTO** gerado na [Etapa 2](#etapa-2-criação-das-personas-funcionalidades-jornadas-e-do-design-system)
2. **Permissões** — quem pode acessar ou executar aquela jornada/funcionalidade e com qual nível de acesso (somente leitura / leitura parcial / escrita parcial / acesso total / etc.)
3. **Informações de Entrada e Saída** — quais dados entram e quais dados saem de cada funcionalidade
4. **Formatos de Entrada e Saída** — telas, arquivos importados, arquivos exportados, integrações
5. **Regras de validação** — validações de campos, formatos, obrigatoriedades
6. **Regras de cálculo** — fórmulas e lógicas de processamento de dados
7. **Integrações com sistemas externos** — APIs, arquivos, bancos de dados externos
8. **Critérios de aceite** — condições objetivas e verificáveis que definem quando aquela funcionalidade está pronta e aprovada pelo cliente
9. **Outras dúvidas** da equipe para garantir entendimento completo

É fundamental que nessa etapa estejam presentes **designer e engenheiro**, para garantir entendimento pleno de ambos os papéis. Qualquer risco técnico ou de negócio identificado durante o refinamento deve ser registrado imediatamente no **REGISTRO DE RISCOS** do projeto — que corre em paralelo com a [FASE 3 - ARQUITETURA](FASE%203%20-%20ARQUITETURA.md), tornando esse compartilhamento especialmente crítico para o arquiteto.

Após cada sessão de refinamento, o agente de IA processa a transcrição da reunião e produz o **DOCUMENTO DE REFINAMENTO** de cada funcionalidade discutida, seguindo a estrutura padronizada abaixo. A equipe revisa e valida o documento antes de avançar:

```
# REFINAMENTO: {Nome da Funcionalidade}

## Propósito
[O que essa funcionalidade faz e qual problema resolve]

## Jornada e Persona
[A qual jornada pertence e qual persona a utiliza]

## Permissões e Perfis de Acesso
[Quem pode acessar e com qual nível de permissão]

## Entradas
[Dados, arquivos ou eventos que iniciam ou alimentam a funcionalidade]

## Saídas
[Dados, telas, arquivos ou eventos produzidos pela funcionalidade]

## Regras de Negócio e Validações
[Lista de regras funcionais, validações e restrições]

## Regras de Cálculo
[Fórmulas e lógicas de processamento, quando aplicável]

## Integrações Externas
[APIs, sistemas ou fontes de dados externas envolvidas]

## Critérios de Aceite
[Condições objetivas e verificáveis que definem quando a funcionalidade está pronta]

## Dúvidas Resolvidas
[Registro das dúvidas que surgiram e foram respondidas durante o refinamento]
```

* **INPUTS:**
  - Definição de **PERSONAS**, **FUNCIONALIDADES** e **JORNADAS**
  - **DESIGN SYSTEM**
  - **GUIA DE REFINAMENTO** aprovado pela equipe

* **OUTPUTS:**
  - **DOCUMENTO DE REFINAMENTO** por **FUNCIONALIDADE** (estrutura padronizada acima)
  - Transcrição das reuniões de refinamento
  - **REGISTRO DE RISCOS** atualizado com os novos riscos identificados


---

## ETAPA 4: Prototipação das Jornadas

Com o **DESIGN SYSTEM** criado e os **DOCUMENTOS DE REFINAMENTO** das funcionalidades disponíveis, o designer cria os protótipos visuais das jornadas para apresentação e validação junto ao cliente. A prototipação deve utilizar a mesma ferramenta de design com IA escolhida na [Etapa 2](#etapa-2-criação-das-personas-funcionalidades-jornadas-e-do-design-system) — **Google Stitch**, **Figma Make** ou **Claude Design** —, alimentando-a com os documentos de refinamento para gerar os protótipos de forma iterativa e consistente com o design system.

O designer trabalha de forma interativa até atingir um nível profissional de qualidade, que atenda claramente a necessidade do cliente. Antes de avançar para a apresentação, os protótipos devem ser validados internamente pelo engenheiro do projeto, garantindo viabilidade técnica e aderência à arquitetura definida na [FASE 3](FASE%203%20-%20ARQUITETURA.md).

Para a apresentação ao cliente, os protótipos devem ser organizados em sequência lógica de jornada, facilitando o acompanhamento e a compreensão da experiência como um todo.

Ao concluir a prototipação de uma jornada, o designer produz o **`DESIGN.md`** correspondente — um documento markdown formatado para consumo pelos agentes de IA na [FASE 4 - DESENVOLVIMENTO](FASE%204%20-%20DESENVOLVIMENTO.md). Ele deve conter:

1. Decisões de design e UX relevantes para a implementação
2. Referências diretas aos arquivos de protótipo no Google Stitch / Figma Make / Claude Design
3. Lista de componentes do **DESIGN SYSTEM** utilizados, com seus tokens e variantes
4. Instruções específicas de comportamento de interface (animações, estados, responsividade, etc.)

* **INPUTS:**
  - **DESIGN SYSTEM**
  - **DOCUMENTOS DE REFINAMENTO** das funcionalidades a prototipar

* **OUTPUTS:**
  - Protótipos das jornadas para apresentação ao cliente
  - **`DESIGN.md`** por jornada prototipada, formatado para consumo pelo agente de desenvolvimento


---

## ETAPA 5: Apresentação dos Protótipos ao Cliente

Os protótipos criados na [Etapa 4](#etapa-4-prototipação-das-jornadas) são apresentados ao cliente para validação. A equipe apresenta cada jornada em sequência, explicando a experiência esperada do usuário, as regras contempladas e as decisões de design. Atenção especial deve ser dada aos comentários do cliente — que podem revelar lacunas de entendimento, necessidade de ajustes ou mudanças de escopo.

Caso ajustes sejam necessários, volta-se a uma nova rodada de prototipação (e eventualmente de refinamento, se as mudanças forem funcionais), num ciclo que se repete até que os protótipos estejam **validados pelo cliente**.

Com a validação de uma jornada, todos os seus documentos de refinamento, critérios de aceite e o `DESIGN.md` já estão prontos para alimentar a [FASE 4 - DESENVOLVIMENTO](FASE%204%20-%20DESENVOLVIMENTO.md). O desenvolvimento dessa jornada pode ser iniciado imediatamente, sem aguardar a validação das demais jornadas.

* **INPUTS:**
  - Protótipos das jornadas
  - **`DESIGN.md`** correspondente

* **OUTPUTS:**
  - Ajustes para nova rodada de prototipação, ou
  - Validação dos protótipos pelo cliente — liberando a jornada para desenvolvimento na [FASE 4](FASE%204%20-%20DESENVOLVIMENTO.md)
