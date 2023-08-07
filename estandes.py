import variaveis
import sys
import pygame

def estandes(janela):
    while True:
        janela.fill(variaveis.branco)
        
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao, estande in zip(botoes, variaveis.estandes):
                    if variaveis.botao_clicado(botao):
                        variaveis.Jogador.estande_selecionado = estande
                        return "inicio"
            elif evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pergunta_texto = variaveis.fonte_texto_inicial.render("Em qual estande está o jogo?", True, variaveis.laranja)
        janela.blit(pergunta_texto, (variaveis.largura / 2 - pergunta_texto.get_width() / 2, 20))

        botoes = []
        altura_botao = 40
        largura_botao = variaveis.largura//2 + 20
        for i, estande in enumerate(variaveis.estandes):
            retangulo_botao = pygame.Rect(variaveis.largura/2 - largura_botao/2, 50 + i * (altura_botao + 10), largura_botao, altura_botao)
            pygame.draw.rect(janela, variaveis.preto, retangulo_botao, 2)
            botoes.append(retangulo_botao)

            # Renderiza o texto dos estandes nos botões
            texto = variaveis.fonte_texto.render(estande, True, variaveis.preto)
            retangulo_texto = texto.get_rect(center=retangulo_botao.center)
            janela.blit(texto, retangulo_texto)

        variaveis.posiciona_logo(janela)
        pygame.display.flip()
        pygame.display.update()