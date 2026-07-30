# Camada de humanização (revisor-narrativa-executiva)

Depois que o documento de revisão da Etapa 3 é aprovado, mas antes de gerar o XLSX e o HTML
finais, todo texto narrativo em português que vai aparecer nos entregáveis (descrições de
problema/solução nos cards, texto de contexto/método, síntese de fechamento) passa por uma
revisão de humanização, usando a skill `revisor-narrativa-executiva` quando disponível no
ambiente. Se a skill não estiver disponível, aplique manualmente os mesmos princípios abaixo.

## O que essa camada verifica

- **Travessão (em-dash) em excesso**: corrige reestruturando a frase, não só trocando a
  pontuação por vírgula ou ponto. Um texto cheio de "—" em toda frase tem cadência de IA, não de
  redação humana.
- **Cacofonia e vícios de linguagem**: junções de palavras que soam estranhas quando lidas em voz
  alta, repetição de conectivos, frases que começam todas da mesma forma.
- **Tiques de IA / assinatura estrutural**: padrões previsíveis de frase (ex. sempre
  "problema → solução" na mesma cadência, adjetivos genéricos como "robusto", "eficiente",
  "intuitivo" sem sustentação concreta) — humanize trocando por linguagem específica ao achado
  real.
- **Legibilidade (Flesch PT-BR)**: mira uma zona de leitura confortável para um público executivo
  (nem infantilizado, nem acadêmico demais) — frases longas demais ou com muitas subordinadas
  aninhadas são simplificadas.

## Exceções — o que nunca deve ser reestruturado

Nem todo travessão é um tique de IA. Dois tipos de texto usam "—" legitimamente e **nunca** devem
ser alterados por essa camada, mesmo quando a regra acima mandaria reestruturar:

- **Nomes próprios de tela/artefato**, quando o travessão é parte do nome, não pontuação de frase
  — ex. o rótulo de tela "Chat — Atendimento" (`TELA_LABEL`, `data-section`, títulos de slide). Um
  passe de humanização que já reescreveu isso incorretamente numa versão anterior do documento;
  o teste correto é perguntar "isto é um nome que aparece em outro lugar do sistema/produto
  avaliado, ou é prosa que eu mesmo escrevi para descrever algo?" — só o segundo caso é elegível
  para reestruturação.
- **Citações bibliográficas formais**, no formato `Autor (ano) — Título/descrição` usado em toda
  referência a ISO, W3C, APCA/Somers, Nielsen & Molich etc. (ex. "APCA — Accessible Perceptual
  Contrast Algorithm (Somers, 2019-2024)"). Esse travessão separa autor/ano de título de obra —
  é convenção bibliográfica padrão, não uma frase composta que precise de reestruturação.

Na dúvida, aplique o teste: se o texto ao redor do "—" é uma sentença corrida com sujeito e verbo
próprios (uma frase que alguém escreveu), reestruture. Se o "—" é parte de um rótulo, nome ou
citação que **identifica algo** (uma tela, uma fonte, um autor), deixe como está.

## Por que isso importa aqui especificamente

Um UX Assessment é, em si, um artefato de comunicação executiva — vai para stakeholders que
precisam agir sobre os achados, não só lê-los. Texto com cadência robótica ou genérica demais
reduz a credibilidade do diagnóstico, mesmo quando os números por trás estão corretos. A
humanização não muda nenhum dado, nota ou classificação — só a forma como o achado é descrito.

## Quando aplicar

Sempre na Etapa 4, depois da aprovação do documento de revisão. Nunca antes — o documento de
revisão da Etapa 3 prioriza precisão e rastreabilidade sobre elegância de prosa; é aceitável (e
até desejável) que ele seja mais cru/técnico, já que quem revisa quer conferir a lógica, não ler
uma versão polida.
