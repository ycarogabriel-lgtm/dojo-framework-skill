# Tratando screenshots, vídeos e fluxos do Figma como evidência

## Screenshots — obrigatório, a fonte primária

Cada tela avaliada precisa de pelo menos 1 screenshot real. É a partir dele que você identifica
problemas de Conteúdo, Design e boa parte de Arquitetura da Informação diretamente — não espere
um vídeo narrando o óbvio que já está visível na imagem. Sempre referencie o caminho real do
arquivo de screenshot no `data.py` (campo `screenshot` de cada tela) — nunca use um placeholder
ou invente que uma imagem existe quando não foi fornecida.

## Vídeos — opcionais, até 3, com papéis diferentes

Até 3 vídeos podem ser fornecidos, cada um com um papel distinto — trate-os de forma diferente:

1. **Alguém narrando fluxo + problemas juntos**: a fonte mais rica — tanto contexto de uso quanto
   achados de usabilidade na voz de quem usa o sistema no dia a dia. Cite trechos transcritos
   como evidência narrada direta de um achado específico.
2. **Alguém explicando o que cada tela/funcionalidade faz**: isto é **contexto, não achado**. Use
   para entender o objetivo da tela antes de avaliar se ela cumpre esse objetivo bem — não cite
   isso como prova de um problema.
3. **Alguém narrando problemas tela por tela especificamente**: achados diretos, geralmente mais
   focados que o vídeo 1. Cite como evidência narrada, associando cada trecho relevante à
   avaliação (área + tema) que ele sustenta.

Se um vídeo estiver disponível, transcreva (ou peça a transcrição) os trechos relevantes por
tela antes de escrever os achados — não parafraseie de memória depois de assistir uma vez.

## Fluxo do Figma — opcional, contexto de navegação

Um fluxo do Figma (de onde vem, para onde vai cada tela) ajuda a entender problemas de
Arquitetura da Informação que só aparecem na transição entre telas (ex. uma ação que deveria
levar a um lugar previsível mas leva a outro). Não é fonte de achados de Design ou Conteúdo
isolados — é contexto de navegação.

## Não confunda o artefato com a tela

Antes de escrever qualquer achado, confirme que o screenshot mostra de fato a interface sendo
avaliada — não um documento ou arquivo que essa interface produz. Um assessment já cometeu esse
erro: a tela de "Proposta" foi avaliada a partir de uma captura que mostrava, na verdade, um PDF
aberto no visualizador do navegador (a proposta já exportada), não a tela de edição real da
ferramenta. Isso levou a achados inteiros sobre "contraste dentro do PDF" e "ausência de busca no
documento" — problemas de um leitor de PDF genérico, não da interface que estava sendo avaliada.
O erro só foi pego porque o cliente reconheceu a tela errada; a análise inteira daquela tela teve
que ser refeita.

Antes de aceitar um screenshot como evidência de uma tela, pergunte: isto é a interface do
produto, ou é uma saída/exportação que o produto gera (PDF, impressão, e-mail, relatório
estático)? Se for a segunda opção, volte ao catálogo de capturas (ou peça um novo print) até
achar a tela real — nunca avalie a interface "por tabela", assumindo que ela deve ser parecida
com o artefato que ela produz.

## Regra de atribuição

No documento de revisão da Etapa 3, cada achado que se apoia em evidência narrada (vídeo) deve
citar de qual vídeo/trecho veio; achados baseados só no screenshot não precisam dessa citação,
mas ainda assim devem referenciar a tela/screenshot exato de onde vieram. Nunca misture
"comentário de alguém em reunião" com "achado heurístico verificado" sem deixar claro qual é
qual — comentários de usuário são contexto de apoio, a heurística em si precisa ser sua análise
independente contra as bases teóricas (ver `bases_teoricas.md`), não uma repetição do que a
pessoa gravada achou.
