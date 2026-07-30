"""
data_exemplo.py -- Exemplo de arquivo de dados para a skill ux-assessment-heuristico.

Define TELAS: uma lista de dicts, um por tela avaliada. Cada tela tem:
  - key:        slug curto, usado em IDs de HTML (ex. "dashboard")
  - label:      nome de exibição da tela (ex. "Dashboard")
  - screenshot: caminho para o arquivo de imagem real da tela (obrigatório na prática --
                sem ele, o HTML final mostra o estado "screenshot não fornecido")
  - rows:       lista de até 15 avaliações (3 por área x 5 áreas), cada uma criada com o
                helper R() abaixo.

O helper R(area, tema, importancia, quebra, problema, solucao, ...) aceita 3 kwargs
opcionais que enriquecem o documento de revisão da Etapa 3 (não aparecem no HTML final,
que é enxuto por design):
  - base:               referência teórica específica desta avaliação (ex. "Nielsen (1994)
                         — Heurística 4"). Se omitido, cai num default genérico por área
                         (ver basis_for() em gen_html.py e references/bases_teoricas.md).
  - justificativa:       a lógica por trás da Importância e da Quebra escolhidas -- por que
                         esse número, não outro. Vai para o documento de revisão (Etapa 3).
  - contraste_medido:    valor de Lc (APCA) medido via scripts/apca/, quando o achado for
                         sobre legibilidade/contraste de cor.
  - evidencia_narrada:   trecho transcrito de um vídeo de walkthrough, se o achado se apoiar
                         em algo que a pessoa gravada disse (ver references/captura_evidencias.md).

`area` deve ser uma das 5 chaves fixas: "conteudo", "ai", "design", "tecnologia", "negocios".
`quebra` deve ser uma das 5 categorias fixas: "Nenhum", "Ruído", "Obstáculo", "Obstrução", "Barreira".
"""

import os

_HERE = os.path.dirname(os.path.abspath(__file__))


def R(area, tema, importancia, quebra, problema, solucao, base=None,
      justificativa=None, contraste_medido=None, evidencia_narrada=None):
    return {
        "area": area,
        "tema": tema,
        "importancia": importancia,
        "quebra": quebra,
        "nota": importancia * {"Nenhum": 0.0, "Ruído": 0.25, "Obstáculo": 0.5,
                                "Obstrução": 0.75, "Barreira": 1.0}[quebra],
        "problema": problema,
        "solucao": solucao,
        "base": base,
        "justificativa": justificativa,
        "contraste_medido": contraste_medido,
        "evidencia_narrada": evidencia_narrada,
    }


TELAS = [
    {
        "key": "dashboard",
        "label": "Dashboard",
        "screenshot": os.path.join(_HERE, "example_assets", "shot_dashboard.png"),
        "rows": [
            R("conteudo", "Clareza dos rótulos", 2, "Ruído",
              "Os cartões de indicador usam abreviações internas (\"TKT méd.\") sem legenda.",
              "Expandir a abreviação ou adicionar tooltip explicando o indicador.",
              justificativa="Importância 2 porque afeta compreensão, mas não impede o uso; Ruído porque a pessoa consegue continuar, só precisa perguntar a um colega o que significa."),
            R("conteudo", "Densidade de informação", 2, "Nenhum",
              "", ""),
            R("conteudo", "Hierarquia de leitura", 3, "Obstáculo",
              "Não fica claro qual dos 6 cartões do topo é o mais urgente de olhar primeiro.",
              "Destacar visualmente (tamanho/cor) o indicador mais crítico do momento."),
            R("ai", "Nomenclatura de menu", 2, "Ruído",
              "O item de menu \"Zeta\" não deixa claro que é o dashboard principal.",
              "Renomear para \"Painel\" ou \"Dashboard\"."),
            R("ai", "Localização de filtros", 3, "Obstrução",
              "Os filtros de período ficam escondidos atrás de um ícone sem rótulo, em canto pouco visível.",
              "Expor o filtro de período como controle visível no topo da tela.",
              base="ISO 9241-110:2020"),
            R("ai", "Breadcrumb/Where am I", 1, "Nenhum", "", ""),
            R("design", "Contraste do texto secundário", 3, "Barreira",
              "Texto de legenda dos gráficos em cinza-claro sobre fundo branco.",
              "Escurecer a cor do texto de legenda para atingir Lc >= 60 (APCA).",
              base="WCAG 2.1",
              contraste_medido="Lc medido de 28 entre o texto de legenda (#BBBBBB) e o fundo branco (#FFFFFF) -- abaixo do mínimo de 45 mesmo para texto grande."),
            R("design", "Consistência de cor por status", 2, "Obstaculo" if False else "Obstáculo",
              "Vermelho, laranja e amarelo são usados de forma inconsistente entre cartões e gráficos.",
              "Definir uma paleta única de status e aplicá-la em todos os componentes."),
            R("design", "Espaçamento entre cartões", 1, "Ruído",
              "Cartões colados uns nos outros em telas menores.",
              "Aumentar o gap entre cartões no grid responsivo."),
            R("tecnologia", "Estado de carregamento", 3, "Obstrução",
              "Ao trocar o filtro de período, a tela fica em branco por 2-3s sem indicação de carregamento.",
              "Adicionar skeleton/spinner visível durante o recarregamento dos dados."),
            R("tecnologia", "Mensagem de erro", 2, "Barreira",
              "Se a API de indicadores falha, a tela mostra os cartões zerados sem aviso de erro.",
              "Exibir mensagem de erro clara com opção de tentar novamente."),
            R("tecnologia", "Responsividade", 1, "Nenhum", "", ""),
            R("negocios", "Comunicação da marca", 1, "Ruído",
              "Logo do produto aparece em baixa resolução no cabeçalho.",
              "Substituir por um arquivo de logo em resolução adequada."),
            R("negocios", "Percepção de confiabilidade", 2, "Obstáculo",
              "Números sem unidade/contexto (\"482\") reduzem a confiança de quem lê rapidamente.",
              "Adicionar unidade e comparação com período anterior em cada indicador."),
            R("negocios", "Diferenciação competitiva", 1, "Nenhum", "", ""),
        ],
    },
    {
        "key": "pedidos",
        "label": "Pedidos",
        "screenshot": os.path.join(_HERE, "example_assets", "shot_pedidos.png"),
        "rows": [
            R("conteudo", "Clareza do status do pedido", 3, "Obstáculo",
              "Status exibido só como cor (bolinha), sem texto, na lista de pedidos.",
              "Adicionar rótulo textual ao lado da cor de status.",
              base="WCAG 2.1",
              evidencia_narrada="\"Eu não sei o que cada bolinha colorida quer dizer sem passar o mouse em cima\" — narração de walkthrough, tela de Pedidos."),
            R("conteudo", "Terminologia consistente", 2, "Ruído",
              "\"Pedido\" e \"Ordem\" são usados de forma intercambiável em textos da mesma tela.",
              "Padronizar em um único termo em toda a interface."),
            R("conteudo", "Mensagens vazias", 1, "Nenhum", "", ""),
            R("ai", "Busca por número de pedido", 1, "Nenhum", "", ""),
            R("ai", "Ordenação da lista", 2, "Obstáculo",
              "Não é possível ordenar a lista de pedidos por data ou valor.",
              "Adicionar cabeçalhos de coluna clicáveis para ordenação."),
            R("ai", "Agrupamento por cliente", 2, "Ruído",
              "Pedidos do mesmo cliente aparecem espalhados na lista sem agrupamento.",
              "Permitir agrupar/filtrar por cliente."),
            R("design", "Tamanho da fonte da tabela", 2, "Obstáculo",
              "Fonte de 11px na tabela principal, pequena para leitura prolongada.",
              "Aumentar para no mínimo 13px no corpo da tabela."),
            R("design", "Contraste dos botões de ação", 3, "Obstrução",
              "Botão \"Cancelar pedido\" em cinza-claro sobre branco, quase invisível.",
              "Aplicar cor de alerta com contraste adequado ao botão de cancelamento.",
              base="WCAG 2.1",
              contraste_medido="Lc medido de 22 entre o texto do botão (#CCCCCC) e o fundo branco -- bem abaixo do mínimo de 45."),
            R("design", "Alinhamento de colunas numéricas", 1, "Ruído",
              "Valores monetários alinhados à esquerda, dificultando comparação visual.",
              "Alinhar colunas numéricas à direita."),
            R("tecnologia", "Confirmação antes de ação destrutiva", 3, "Barreira",
              "Clicar em \"Cancelar pedido\" cancela imediatamente, sem diálogo de confirmação.",
              "Adicionar modal de confirmação antes de cancelar um pedido."),
            R("tecnologia", "Paginação", 2, "Obstáculo",
              "Lista carrega todos os pedidos de uma vez, travando com bases grandes.",
              "Implementar paginação ou scroll virtualizado."),
            R("tecnologia", "Auto-save de filtros", 1, "Nenhum", "", ""),
            R("negocios", "Upsell/Cross-sell", 1, "Nenhum", "", ""),
            R("negocios", "Percepção de controle", 2, "Obstáculo",
              "Ausência de confirmação (ver Tecnologia) também prejudica a percepção de controle sobre ações críticas.",
              "Ver solução de confirmação já recomendada."),
            R("negocios", "Comunicação de valor", 1, "Ruído",
              "Nenhum indicador de economia/eficiência é reforçado nesta tela.",
              "Considerar destacar métricas de eficiência obtidas pelo cliente."),
        ],
    },
]
