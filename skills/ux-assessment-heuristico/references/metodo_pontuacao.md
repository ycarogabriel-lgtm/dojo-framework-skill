# Método de pontuação — Importância × Quebra = Nota

## As 5 áreas fixas

Toda tela avaliada é dividida nas mesmas 5 áreas, sempre nesta ordem:

1. **Conteúdo** — o que é dito, em que ordem, com que clareza (texto, dados, mensagens exibidas).
2. **Arquitetura da Informação** — como a informação é estruturada, nomeada, encontrada e
   reconhecida entre telas.
3. **Design** — como o conteúdo é apresentado visualmente (hierarquia, cor, tipografia, espaço).
4. **Tecnologia** — como o sistema responde, valida, orienta e sustenta o processo tecnicamente.
5. **Negócios** — como a tela comunica a marca e serve aos objetivos comerciais do negócio.

Cada área recebe **3 heurísticas/temas avaliados por tela** (15 avaliações por tela no total).
Os 3 temas de cada área não precisam ser sempre os mesmos 3 em todas as telas — mantenha um
catálogo mais amplo de temas possíveis por área (um produto avaliado anteriormente, por exemplo,
acionou 26 temas distintos ao longo de 10 telas) e escolha, para cada tela, os 3 mais relevantes
por área com base no que a evidência realmente mostra. O que é fixo é a contagem (3 por área, 15
por tela) e a ordem das áreas — não a lista exata de temas.

## A fórmula

Cada uma das 15 avaliações por tela recebe:

- **Importância** (0 a 3): o quanto aquilo importa para o usuário atingir seu objetivo na tela.
  0 = irrelevante · 1 = menor · 2 = relevante · 3 = crítico para completar a tarefa.
- **Quebra** (categórica, 5 níveis) — o quanto a interface falha nesse ponto:

  | Quebra      | Fator | Definição                                                              |
  |-------------|-------|-------------------------------------------------------------------------|
  | Nenhum      | 0,00  | Não há impedimento — o usuário atende ao objetivo sem esforço extra.    |
  | Ruído       | 0,25  | Estorvo que incomoda, mas não impede a conclusão da tarefa.             |
  | Obstáculo   | 0,50  | Inconveniente que causa dificuldade real, consome tempo.                |
  | Obstrução   | 0,75  | Impedimento parcial — a conclusão da tarefa fica incerta.               |
  | Barreira    | 1,00  | Impedimento total da continuidade da tarefa.                            |

- **Nota** = Importância × fator de Quebra.

**Heurísticas com Quebra = Nenhum não entram no HTML final nem no numerador/denominador do
Erro%** — elas ficam registradas na planilha XLSX (para rastreabilidade de que a área foi de fato
avaliada, e não só ignorada), mas o HTML e o cálculo de Erro% só mostram as avaliações com
problema real identificado. Isso é intencional: o assessment é sobre o que está quebrado, não um
inventário de tudo que foi checado.

## Erro%

Por tela: `Erro% = (soma das Notas das avaliações com Quebra ≠ Nenhum) / (soma das Importâncias
dessas mesmas avaliações)`. O mesmo cálculo se aplica por área dentro de uma tela (usando só as
avaliações daquela área com Quebra ≠ Nenhum), e no agregado geral do assessment (somando Notas e
Importâncias de todas as tela×área combinações).

## Matriz de risco 2×2

Cada combinação tela×área com pelo menos 1 avaliação de Quebra ≠ Nenhum entra na matriz de risco,
classificada por Erro% da combinação e Importância média da combinação:

- `Erro% ≥ 50% e Importância média ≥ 2,0` → **Crítico**
- `Erro% ≥ 50% e Importância média < 2,0` → **Monitorar**
- `Erro% < 50% e Importância média ≥ 2,0` → **Sob controle**
- `Erro% < 50% e Importância média < 2,0` → **Aceitável**

Combinações tela×área onde todas as 3 avaliações daquela área foram "Nenhum" não entram na
matriz (não há o que classificar).

## Semáforo de 2 cores — nunca use verde

O semáforo visual (tags de Quebra, barras, cores de card) usa só 2 cores, nunca uma terceira
"tudo certo" em verde — porque este assessment só lista o que tem problema; não faz sentido um
card "verde" entre achados que são, por definição, problemas identificados:

- **Laranja** (`#FF6E01`): Ruído e Obstáculo (a tarefa é concluída, mas com atrito).
- **Vermelho** (`#C62828`): Obstrução e Barreira (a tarefa fica comprometida ou impedida).

A única exceção de verde no documento inteiro é a seção "Nossas oportunidades" do fechamento
(que lista o que já funciona bem, como contraponto aos achados) — nunca dentro do carrossel de
heurísticas em si.

## Síntese de diagnóstico é sobre jornada, não só notas por tela

O slide de síntese (`diagnostico_ferramenta_atual` / `diagnostico_necessidade_negocio`) não é um
resumo estatístico do Erro% — é o único lugar do assessment que olha o produto **como um todo**,
não tela por tela. Um erro já cometido: descrever cada tela como "resolve bem seu problema local"
sem nunca dizer se as telas, juntas, formam uma jornada coerente. Um produto pode ter 10 telas
individualmente competentes e ainda assim não ter nenhuma trilha que leve uma pessoa do início ao
fim de uma tarefa — isso É um achado de UX, geralmente mais importante que qualquer achado
isolado de uma tela, e precisa aparecer explicitamente em `diagnostico_ferramenta_atual`.

Ao escrever esse campo, responda diretamente: as telas avaliadas compartilham um vocabulário
visual único de status/erro? Existe uma sequência esperada entre elas, ou cada uma é um destino
isolado que a pessoa precisa saber escolher de cor? Se a resposta for "não" ou "não fica claro",
isso deve ser dito explicitamente — não afundado dentro de uma descrição genérica de qualidade
tela a tela.

## Por que registrar a lógica de cada nota

O documento de revisão (Etapa 3) exige, para cada avaliação, uma frase explicando por que aquela
Importância e aquele fator de Quebra foram escolhidos — não só o número. Isso é o que permite à
pessoa que aprova discordar de um número específico com base no raciocínio, não só no resultado.
Uma nota sem lógica registrada não é auditável nem contestável, e o gate da Etapa 3 perde sentido.
