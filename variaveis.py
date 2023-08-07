import pygame as pg
pg.init()

# Janela
largura, altura = 800, 600
margem_lateral = largura * (5/100)
nome_tela = "Instituto Ambikira"

# Texto exibido na tela inicial
intro = "Bem-vindo(a) ao nosso jogo de perguntas e respostas!"
desenvolvimento = "Mostre seu talento enquanto responde aos desafios: aumente sua pontuação e conquiste o topo da competição! Identifique-se para garantir que fiquemos em contato e você não perca a recompensa que preparamos"
texto_nome = "Seu nome completo"
texto_email = "Seu e-mail"

# Cores
branco = "#F2F2F2"
preto = "#0D0D0D"
amarelo = "#F29F05"
laranja = "#F2541B"
azul = "#5068F2"

# Fontes
fonte_texto_inicial = pg.font.SysFont('Quicksand.ttf', 32)
fonte_texto = pg.font.SysFont('Quicksand.ttf', 27)
fonte_legenda = pg.font.SysFont('Quicksand.ttf', 24)
fonte_gigante = pg.font.SysFont('Quicksand.ttf', 72)

# Tamanhos
largura_botao = 200
altura_botao = 40

# Perguntas e respostas
limite_tempo = 30 # Tempo máximo para responder cada pergunta em segundos

# opcoes_respostas: dicionario onde a chave é a pergunta e o valor é uma lista com as opções de resposta
opcoes_respostas = {
    "faceis" : {
        "Pergunta fácil 1": ["Opção 1 de resposta a primeira pergunta facil",
                             "Opção 2 de resposta a primeira pergunta facil",
                             "Opção 3 de resposta a primeira pergunta facil"
                             ],
        "Pergunta fácil 2": ["Opção 1 de resposta a segunda pergunta facil",
                             "Opção 2 de resposta a segunda pergunta facil",
                             "Opção 3 de resposta a segunda pergunta facil"
                            ], 
        "Pergunta fácil 3": ["Opção 1 de resposta a terceira pergunta facil",
                             "Opção 2 de resposta a terceira pergunta facil",
                             "Opção 3 de resposta a terceira pergunta facil"
                            ], 
        "Pergunta fácil 4": ["Opção 1 de resposta a quarta pergunta facil",
                             "Opção 2 de resposta a quarta pergunta facil",
                             "Opção 3 de resposta a quarta pergunta facil"
                            ]

    },
    "medias": {
        "Pergunta média 1": ["Opção 1 de resposta a primeira pergunta media",
                             "Opção 2 de resposta a primeira pergunta media",
                             "Opção 3 de resposta a primeira pergunta media"
                            ],
        "Pergunta média 2": ["Opção 1 de resposta a segunda pergunta media",
                             "Opção 2 de resposta a segunda pergunta media",
                             "Opção 3 de resposta a segunda pergunta media"
                            ],
        "Pergunta média 3": ["Opção 1 de resposta a terceira pergunta media",
                             "Opção 2 de resposta a terceira pergunta media",
                             "Opção 3 de resposta a terceira pergunta media"
                            ],
        "Pergunta média 4": ["Opção 1 de resposta a quarta pergunta media",
                             "Opção 2 de resposta a quarta pergunta media",
                             "Opção 3 de resposta a quarta pergunta media"
                            ]

    }, 
    "dificeis": {
        "Pergunta dificil 1": ["Opção 1 de resposta a primeira pergunta dificil",
                             "Opção 2 de resposta a primeira pergunta dificil",
                             "Opção 3 de resposta a primeira pergunta dificil"
                            ],
        "Pergunta dificil 2": ["Opção 1 de resposta a segunda pergunta dificil",
                             "Opção 2 de resposta a segunda pergunta dificil",
                             "Opção 3 de resposta a segunda pergunta dificil"
                            ],
        "Pergunta dificil 3": ["Opção 1 de resposta a terceira pergunta dificil",
                             "Opção 2 de resposta a terceira pergunta dificil",
                             "Opção 3 de resposta a terceira pergunta dificil"
                            ],
        "Pergunta dificil 4": ["Opção 1 de resposta a quarta pergunta dificil",
                             "Opção 2 de resposta a quarta pergunta dificil",
                             "Opção 3 de resposta a quarta pergunta dificil"
                            ]

    }

}

# acertos: dicionario onde a chave é a pergunta e o valor é a resposta correta
acertos = {
    "Pergunta fácil 1": "Opção 2 de resposta a primeira pergunta",
    "Pergunta fácil 2": "Opção 3 de resposta a segunda pergunta facil",
    "Pergunta fácil 3": "Opção 1 de resposta a terceira pergunta facil",
    "Pergunta fácil 4": "Opção 1 de resposta a quarta pergunta facil",
    "Pergunta média 1": "Opção 2 de resposta a primeira pergunta media",
    "Pergunta média 2": "Opção 3 de resposta a segunda pergunta media",
    "Pergunta média 3": "Opção 1 de resposta a terceira pergunta media",
    "Pergunta média 4": "Opção 3 de resposta a quarta pergunta media",
    "Pergunta dificil 1": "Opção 1 de resposta a primeira pergunta dificil",
    "Pergunta dificil 2": "Opção 3 de resposta a segunda pergunta dificil",
    "Pergunta dificil 3": "Opção 2 de resposta a terceira pergunta dificil",
    "Pergunta dificil 4": "Opção 1 de resposta a quarta pergunta dificil"
}

# Estandes presentes
estandes = ["Credit Suisse", "Dahlia Capital", "Genoa Capital", "Ibiuna Investimentos", "JGP", "Jive Investments",
            "Legacy Capital", "Neo Investimentos", "RBR Asset Management", "RPS Capital", "SPX Capital", "Verde Asset",
            "Vinland Capital"]

# Classe do jogador
class Jogador:
    def __init__(self):
        self.nome = None
        self.email = None
        self.acertos = None
        self.tempo = None
        self.acerto_por_tempo = None
        self.estande_selecionado = None
        self.participantes = None
        self.posicao = None

# Funções
def botao_clicado(coordenadas_botao):
    # Verifica se o botão foi clicado
    mouse_x, mouse_y = pg.mouse.get_pos()
    return coordenadas_botao.collidepoint(mouse_x, mouse_y)

def desenhar_retangulo_com_texto(janela, x, y, largura, altura, cor_retangulo, cor_texto, texto, fonte):
    # Desenhar retângulo (botão) com o texto dentro
    pg.draw.rect(janela, cor_retangulo, ((x, y), (largura, altura)))
    texto_renderizado = fonte.render(texto, True, cor_texto)

    # Centraliazação do texto no retângulo
    texto_x = x + (largura - texto_renderizado.get_width()) // 2
    texto_y = y + (altura - texto_renderizado.get_height()) // 2
    janela.blit(texto_renderizado, (texto_x, texto_y))

def formata_texto(texto, max_largura, fonte_texto):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ''
    for palavra in palavras:
        teste_linha = linha_atual + palavra + ' '
        superficie_teste = fonte_texto.render(teste_linha, True, laranja)
        if superficie_teste.get_width() <= max_largura:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + ' '
    linhas.append(linha_atual)
    return linhas

def posiciona_logo(janela):
    # Redimensionamento da imagem com as logos
    logos = pg.image.load('logos.png')
    porcentagem_redimensionamento = 10
    largura_original, altura_original = logos.get_size()
    proporcao = largura_original / altura_original
    largura_redimensionada = int(largura * porcentagem_redimensionamento / 100)
    altura_redimensionada = int(largura_redimensionada / proporcao)
    logos = pg.transform.scale(logos, (largura_redimensionada, altura_redimensionada))
    posicao_imagem = (largura - largura_redimensionada - 10, altura - altura_redimensionada)
    janela.blit(logos, posicao_imagem)