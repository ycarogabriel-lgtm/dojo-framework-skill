# FASE 1: PRE-VENDA

Na **Performa_IT** os projetos começam quando os clientes nos trazem uma necessidade ou uma dor. E a primeira demanda desse cliente normalmente é uma estimativa de prazo e custo para o projeto. Nesse momento temos que conseguir ter um entendimento mínimo do que é o projeto e do que precisamos fazer nele para conseguirmos estimar o esforço necessário no projeto e conseguirmos gerar uma proposta comercial para o cliente. Vamos chamar essa fase de **PRE-VENDA**.

Quando começamos o processo de **PRE-VENDA** precisamos ter claramente definido quem será o responsável pelo projeto na **Performa_IT**. Nesse início de processo também precisamos identificar de forma clara quem é o cliente e gerar um registro para esse projeto com uma chave única que acompanhará esse projeto do início ao fim (**PIPROJETO-XXXX** com XXXX sendo um sequencial).

Nessa fase de **PRE-VENDA** ainda não temos como gastar muito tempo, pois ainda não temos certeza de que vamos vender o projeto, mas temos que investir o mínimo necessário para conseguirmos escrever uma proposta comercial com um escopo macro que descreva de forma clara os seguintes pontos:

- Qual é o desafio do projeto
- Quais são as **MÉTRICAS DE SUCESSO** do projeto?
- Qual a solução proposta
- Qual o escopo de atuação da Performa_IT
- Qual a especificação da solução ofertada, contendo a lista de **ENTREGÁVEIS** e, para cada um deles, uma especificação funcional minimamente detalhada e detalhes de tecnologias sugeridas
- Qual o cronograma estimado para o projeto (quais são as fases e quando serão entregues cada um dos **ENTREGÁVEIS**)
- Qual é a equipe do projeto
- Premissas desta proposta comercial
- Investimento e condições comerciais (com detalhamento de valores e formas de pagamento)
- Premissas gerais de projetos da Performa_IT

Vamos chamar esse documento de **PROPOSTA COMERCIAL**. Ele deve ser o resultado da fase de **PRE-VENDA** de um projeto.

Durante a **PRE-VENDA** claramente vamos ter ao menos três contatos (um possível quarto) com o cliente, na sequência que segue:

1. **Demanda Inicial** — primeiro contato do cliente com a explicação da demanda inicial. Pode ser uma call, uma reunião presencial ou algum documento enviado por e-mail.
2. **Refinamento da Demanda** — uma call ou reunião para discutirmos nosso entendimento da demanda e refinarmos um entendimento mais profundo da solução.
3. **Apresentação da Proposta Comercial** — apresentar a proposta comercial com nosso entendimento final para o cliente.
4. **Ajustes na Proposta Comercial** — efetuar e apresentar uma proposta comercial ajustada após feedback recebido do cliente na apresentação da **PROPOSTA COMERCIAL** (etapa anterior). Esta etapa pode se repetir mais de uma vez.

Toda essa fase é apoiada por um **agente de IA de PRE-VENDA** pré-configurado com o contexto da Performa_IT, seus diferenciais e os padrões esperados para os documentos de saída. Esse agente opera segundo os princípios do **AI-DLC (AI-Driven Development Lifecycle)**: propõe, questiona e estrutura ativamente — cabendo ao responsável pelo projeto o papel de validador e aprovador em cada ponto crítico de decisão.

---

## ETAPA 1

Após o primeiro contato com o cliente, o agente de IA recebe os insumos iniciais disponíveis e assume a condução da análise. Antes de produzir qualquer documento, o agente deve identificar lacunas de entendimento e fazer perguntas diretas ao responsável pelo projeto para esclarecê-las — nunca tomando decisões críticas de forma autônoma.

Com o entendimento suficientemente claro, o agente formaliza o **INTENT DO PROJETO**: uma declaração concisa e objetiva que captura o propósito de alto nível da iniciativa — o problema que o cliente quer resolver, o resultado de negócio esperado e o que está explicitamente fora do escopo. O **INTENT DO PROJETO** é o artefato âncora do projeto: será referenciado em todas as fases seguintes e garante que qualquer decisão tomada ao longo do projeto possa ser avaliada contra a intenção original do cliente.

Na sequência, o agente produz os demais documentos de preparação para a reunião de refinamento.

* **INPUTS:**
  - Transcript da reunião ou documento de demanda inicial enviado pelo cliente
  - Documentos adicionais enviados pelo cliente
  - Comentários e contexto do responsável pelo projeto

* **OUTPUTS:**
  - **INTENT DO PROJETO** — declaração formal do propósito, resultado esperado e limites de escopo
  - Diagrama de entendimento macro da demanda
  - Texto do entendimento macro da solução proposta
  - Sugestão de **MÉTRICAS DE SUCESSO** para o projeto
  - Documento de preparação para a reunião de refinamento, com perguntas e pontos de discussão

---

## ETAPA 2

O agente de IA recebe o resultado da reunião de refinamento e, em conjunto com o responsável pelo projeto, conduz a construção da **PROPOSTA COMERCIAL**.

Um ponto central desta etapa é a definição dos **ENTREGÁVEIS** do projeto. Cada entregável deve ser pensado como um bloco coeso de valor de negócio — minimamente acoplado aos demais, com propósito claro e autônomo o suficiente para ser desenvolvido e entregue de forma independente. Essa coesão e esse desacoplamento não apenas tornam o escopo mais preciso e a estimativa mais confiável, como também criam a base natural para a organização do trabalho nas fases de desenvolvimento. O agente deve sugerir a decomposição dos entregáveis e o responsável pelo projeto deve validar e ajustar essa estrutura.

Paralelamente à **PROPOSTA COMERCIAL**, o agente produz um **REGISTRO DE RISCOS** inicial do projeto. Esse documento identifica os riscos já visíveis neste momento — técnicos, de prazo, de integração com sistemas existentes, de dependência do cliente, de negócio e de premissas —, atribuindo a cada risco uma classificação de probabilidade e impacto e sugerindo estratégias iniciais de mitigação. O **REGISTRO DE RISCOS** nasce aqui e viaja com o projeto até o final, sendo enriquecido em cada fase.

A definição de precificação fica a cargo do responsável pelo projeto. O agente poderá, porém, trazer indícios de valor extraídos das conversas com o cliente (budget mencionado, estimativas de custos ou perdas do processo atual, ganhos esperados com a solução) e referências de mercado para apoiar a precificação.

* **INPUTS:**
  - Transcript da reunião de refinamento
  - Documentos adicionais enviados pelo cliente
  - Documento de perguntas de refinamento respondido
  - Comentários do responsável pelo projeto
  - **INTENT DO PROJETO** gerado na Etapa 1

* **OUTPUTS:**
  - **PROPOSTA COMERCIAL** com lista estruturada de **ENTREGÁVEIS** coesos e de valor de negócio claro
  - Lista consolidada de **MÉTRICAS DE SUCESSO** do projeto
  - **REGISTRO DE RISCOS** inicial do projeto

---

## ETAPA 3

Após a reunião de apresentação da **PROPOSTA COMERCIAL**, é comum recebermos feedbacks do cliente que exigem ajustes — no entendimento do problema, na solução proposta, no escopo ou nos aspectos comerciais. O agente recebe o retorno dessa reunião e conduz os ajustes necessários, produzindo uma versão atualizada da **PROPOSTA COMERCIAL**. Quando os ajustes impactarem o **REGISTRO DE RISCOS** ou o **INTENT DO PROJETO**, esses documentos devem ser revisados na mesma etapa.

Esta etapa pode repetir-se mais de uma vez até que se chegue a uma versão final aprovada pelo cliente.

* **INPUTS:**
  - Transcript da reunião de apresentação da proposta comercial
  - Comentários do responsável pelo projeto

* **OUTPUTS:**
  - **PROPOSTA COMERCIAL** atualizada
  - **REGISTRO DE RISCOS** atualizado (se aplicável)
  - **INTENT DO PROJETO** atualizado (se aplicável)

---

## ETAPA 4

Com a versão final da **PROPOSTA COMERCIAL** enviada ao cliente, o projeto entra em compasso de espera pela decisão. Durante esse período, o agente acompanha o processo de forma proativa:

- A cada **duas semanas**, o agente aciona o responsável pelo projeto para obter uma atualização sobre o status da decisão.
- O agente permanece disponível para receber inputs assíncronos do responsável (novas dúvidas do cliente, solicitações de ajuste, informações adicionais) e responder ou preparar subsídios de forma ágil.

### Se o projeto for **reprovado**:

O agente questiona o responsável sobre o motivo da perda e registra essa informação de forma estruturada. Em seguida, cruza o motivo com o histórico de perdas anteriores para identificar padrões recorrentes (ex: "terceira perda por questão de prazo em projetos do segmento financeiro") e entrega um breve relatório de análise ao responsável. Esse aprendizado sistêmico alimenta o processo de melhoria contínua da pré-venda da Performa_IT.

### Se o projeto for **aprovado**:

O agente gera a **MEMÓRIA DO PROJETO** — o documento central que consolidará todo o conhecimento gerado durante a pré-venda e que servirá de entrada para todos os agentes e equipes das fases seguintes. Para que seja consumida de forma previsível e eficiente, a **MEMÓRIA DO PROJETO** segue uma estrutura padronizada, contendo obrigatoriamente as seguintes seções:

1. **INTENT DO PROJETO** — declaração de propósito, resultado esperado e limites de escopo
2. **ENTREGÁVEIS** — lista estruturada com descrição e valor de negócio de cada entregável
3. **MÉTRICAS DE SUCESSO** — lista consolidada e acordada com o cliente
4. **REGISTRO DE RISCOS** — versão mais recente do registro de riscos identificados
5. **Escopo** — o que está dentro e o que está fora do escopo contratado
6. **Restrições e Premissas** — todas as premissas da proposta e restrições conhecidas
7. **Decisões Tomadas** — principais decisões de solução e tecnologia já definidas
8. **Contexto Comercial** — valor do contrato, forma de pagamento, marco de entregas e informações relevantes do relacionamento comercial

Com a **MEMÓRIA DO PROJETO** pronta, o agente sugere o acionamento do agente responsável pela confecção do contrato (quando necessário) e do agente de alocação da equipe para o projeto.

* **INPUTS:**
  - Resultado da pré-venda (projeto aprovado ou reprovado)
  - Todo o histórico de documentos gerados nas etapas anteriores

* **OUTPUTS:**
  - **MEMÓRIA DO PROJETO** estruturada (em caso de aprovação)
  - Relatório de análise de padrões de perda (em caso de reprovação)

---

> O agente deverá armazenar no registro do **PIPROJETO** a data e hora em que cada uma das etapas ocorreram (transições de estado) para fins de apuração do lead time do processo de vendas e de análise de eficiência do funil.
