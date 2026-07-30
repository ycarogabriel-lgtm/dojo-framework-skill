# Bases teóricas — quando citar cada uma

Todo card de heurística no HTML final e toda linha da matriz no XLSX cita uma base teórica
específica (campo `card-basis` / coluna "Base"). Nunca deixe um achado sem base citada, e nunca
cite uma base genérica ("boas práticas de UX") quando uma das fontes abaixo se aplica com mais
precisão.

## Nielsen (1994) — 10 Usability Heuristics for User Interface Design

A base mais usada — cobre a maioria dos achados de Conteúdo, Arquitetura da Informação,
Tecnologia e parte de Design. As 10 heurísticas clássicas, para referência ao escolher qual citar:

1. Visibilidade do status do sistema
2. Correspondência entre o sistema e o mundo real
3. Controle e liberdade do usuário
4. Consistência e padrões
5. Prevenção de erros
6. Reconhecimento em vez de memorização (relaciona-se a Miller/Hick, ver abaixo)
7. Flexibilidade e eficiência de uso
8. Estética e design minimalista
9. Ajudar os usuários a reconhecer, diagnosticar e corrigir erros
10. Ajuda e documentação

Cite como: `Nielsen (1994) — Heurística N`. Também cite **Nielsen & Molich (1990)** — o paper que
mostra que um avaliador isolado costuma identificar entre 20% e 51% dos problemas de usabilidade
existentes — na seção de limitação metodológica do documento de revisão e do slide de contexto,
nunca como base de um achado individual.

## ISO 9241-110:2020 — Ergonomics of human-system interaction — Dialogue principles

Use para achados sobre os 7 princípios de diálogo (adequação à tarefa, autodescritividade,
capacidade de controle, conformidade com expectativas, tolerância a erros, capacidade de
individualização, adequação à aprendizagem) — tipicamente achados de Tecnologia e Arquitetura da
Informação que não se encaixam perfeitamente numa heurística de Nielsen específica.

## WCAG 2.1 (W3C, 2018)

Use para qualquer achado de acessibilidade: contraste de cor (SC 1.4.1 Use of Color, SC 1.4.3/1.4.6
Contrast Minimum/Enhanced, SC 1.4.4 Resize Text), navegação por teclado, texto alternativo. É a
base padrão para achados de Design ligados a legibilidade — sempre acompanhada de uma medição
real de contraste (ver `apca_contraste.md`), nunca citada sozinha como "parece pouco acessível".

## Morville — User Experience Honeycomb (2004)

Use para achados que não são um bug pontual, mas uma qualidade ausente da experiência como um
todo: útil, usável, desejável, encontrável, acessível, crível, valioso. Frequente em achados de
Design (desejabilidade/credibilidade visual) e Negócios (valor percebido).

## Miller (1956) / Hick (1952)

Miller — "The Magical Number Seven, Plus or Minus Two": use quando o achado é sobre carga de
memória (muitas opções/informações para reter ao mesmo tempo). Hick — "On the rate of gain of
information": use quando o achado é sobre tempo de decisão crescendo com o número de opções
apresentadas (ex. um menu com 20 itens sem agrupamento). Ambos aparecem tipicamente em achados de
Conteúdo e Design ligados a excesso de opções/informação simultânea.

## APCA — Accessible Perceptual Contrast Algorithm (Somers, 2019-2024, W3 WCAG 3/Silver)

Use para qualquer achado de contraste que você mediu de verdade via `scripts/apca/` — é a base
mais precisa disponível hoje para contraste perceptual (sucessor do WCAG 2.1 no draft do WCAG 3).
Ver `apca_contraste.md` para o processo completo de medição.

## "Framework próprio Performa.it — lente de negócio"

Use exclusivamente para achados da área **Negócios** (habilidade de comunicar a marca, habilidade
de vender a percepção do produto, alinhamento com objetivos comerciais) — não existe uma fonte
acadêmica externa consolidada para essa lente; é o framework proprietário da Performa.it. Nunca
force uma citação de Nielsen/ISO/WCAG num achado que é fundamentalmente sobre percepção de marca
ou negócio.

## Regra de ouro

Se um achado parece se encaixar em duas bases, escolha a mais específica (ex.: um problema de
contraste de cor é WCAG/APCA, não Nielsen — mesmo que "Estética e design minimalista" também
pareça aplicável). A base citada deve ajudar quem lê a entender *por que* aquilo é considerado um
problema reconhecido, não apenas decorar o achado com uma referência acadêmica.

## Precisão terminológica — "heurística" não é sinônimo de "critério"

Erro já cometido e corrigido: usar "heurística" como palavra genérica para qualquer achado do
documento, em textos como "26 heurísticas avaliadas" ou "heurísticas reconhecidas (Nielsen, ISO
9241-110, WCAG, Morville, Miller)". Isso é impreciso — cada uma das bases acima é um tipo
diferente de instrumento, não uma "heurística" no sentido técnico do termo:

| Base                        | Tipo correto                          |
|------------------------------|----------------------------------------|
| Nielsen (1994)               | Heurística de usabilidade (o único caso que é, de fato, uma heurística) |
| ISO 9241-110:2020             | Norma internacional de diálogo         |
| Morville — Honeycomb (2004)   | Modelo de arquitetura da informação    |
| WCAG 2.1 / APCA               | Diretriz de acessibilidade             |
| Miller (1956) / Hick (1952)   | Achado de psicologia cognitiva         |
| Framework próprio Performa.it | Lente de negócio proprietária          |

Regra prática ao escrever qualquer texto fixo do documento (capa, contexto, método, carrossel,
`aria-label`, contadores):

- **"Heurística" só quando o achado específico vem de Nielsen.** Nunca use a palavra para descrever
  o conjunto todo, nem para um achado que vem de ISO/WCAG/Morville/Miller/Performa.
- **"Critério"** é o termo neutro para o conjunto — use-o em qualquer frase que precise se referir
  genericamente a "cada um dos itens avaliados por tela", independente da base de origem (ex.: "3
  critérios por área", "critério com problema identificado", navegação "achado anterior/próximo").
- Isso vale também para rótulos de interface que não parecem prosa — o mesmo erro apareceu em
  `aria-label="Heurística anterior"` e num contador "heurística 1 de N" no carrossel de achados;
  ambos foram corrigidos para "achado anterior"/"achado 1 de N".
- O slide dedicado de metodologia (`_render_base_row` / token `BASE_ROW` em `gen_html.py`) existe
  para tornar essa distinção visível ao leitor com números reais do cliente, não só como nota de
  rodapé — sempre que a skill gerar um novo documento, essa lâmina deve refletir a proporção real
  de achados por base (via `compute_basis_rows`), nunca um texto fixo copiado de outro cliente.
