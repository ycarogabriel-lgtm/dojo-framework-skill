# Medindo contraste real com APCA

## Por que APCA e não a razão de contraste do WCAG 2.1

A razão de contraste clássica do WCAG 2.1 (ex.: "4.5:1") é uma fórmula antiga que não modela bem
a percepção humana em vários casos (texto claro sobre fundo escuro vs. o inverso, tamanhos de
fonte grandes, cores de baixa luminância). APCA (Accessible Perceptual Contrast Algorithm) é o
sucessor proposto para o WCAG 3 (Silver), e é o que esta skill usa para qualquer achado que cite
contraste — nunca estime contraste "de olho", meça de verdade.

## O fluxo de medição

1. **Recorte** uma região pequena ao redor do elemento de texto que você quer medir, a partir do
   screenshot real da tela (`scripts/apca/sample_and_measure.py --debug-crop` ajuda a conferir
   visualmente se o recorte pegou a área certa antes de confiar no número).
2. **Amostre os pixels**: trate a cor mais escura da região recortada como a cor do texto, e a
   cor mais frequente (moda) como a cor de fundo. Isso funciona bem para texto sólido sobre fundo
   sólido; para gradientes ou texto sobre imagem, recorte uma região menor e mais homogênea.
3. **Calcule Lc** alimentando os dois hex resultantes em `scripts/apca/lc.js` (wrapper Node sobre
   o pacote oficial `apca-w3` — não existe um equivalente confiável em pip, por isso o
   Node é necessário aqui). O sinal de Lc indica a polaridade (texto claro sobre fundo escuro dá
   Lc negativo, o inverso dá Lc positivo); a magnitude indica a severidade.

## Valores de referência para calibrar

- Preto sobre branco: Lc ≈ 106
- Branco sobre preto: Lc ≈ -108

Se o seu par calibrado (preto/branco puros) não bater perto disso, o wrapper está com problema —
não confie nos números de produção até resolver isso.

## Limiares de leitura

| \|Lc\|   | Leitura                                          |
|---------|---------------------------------------------------|
| ≥ 90    | Ideal                                              |
| ≥ 75    | Bom                                                 |
| ≥ 60    | Mínimo aceitável para texto de corpo                |
| ≥ 45    | Mínimo aceitável só para texto grande ou negrito    |
| < 45    | Reprovado — cite como achado de Design/Cores        |

## Como citar no achado

Sempre cite o valor de Lc medido, nunca uma descrição qualitativa sozinha: "Lc medido de 32
(abaixo do mínimo de 45 para texto grande) entre o texto do badge de status e o fundo cinza-claro
do card" é uma citação válida; "o contraste parece baixo" não é.

## Limitação conhecida do ambiente (não bloqueante)

Screenshots sintéticos ou muito comprimidos (JPEG com heavy compression, fontes pequenas com
anti-aliasing agressivo) podem produzir recortes onde a amostragem de "cor mais escura" e "cor
mais frequente" não isola bem texto de fundo, resultando em Lc artificialmente próximo de 0. Se
isso acontecer, aumente a região de recorte ou recorte um trecho de texto maior antes de
descartar a medição como não confiável — mas nunca substitua a medição por uma estimativa visual.
