import variaveis
import sys
import pygame
import math

def tela_score(janela):
    while True:
        janela.fill(variaveis.branco)
        altura_texto = 32

        # Botão
        x, y, largura, altura = variaveis.largura//2 - variaveis.largura_botao//2, altura_texto*14, variaveis.largura_botao, variaveis.altura_botao
        variaveis.desenhar_retangulo_com_texto(janela, x, y, largura, altura, variaveis.laranja, variaveis.branco, "Reiniciar", variaveis.fonte_texto)

        # Renderiza textos na tela
        desempenho = f"Você chegou ao fim! Teve {variaveis.Jogador.acertos} acerto(s) em aproximadamente {int(variaveis.Jogador.tempo)} segundos. Muito bem! Veja a sua posição entre os {variaveis.Jogador.participantes} participantes até o momento:"
        posicao_usuario = str(variaveis.Jogador.posicao)
        agradecimento = "Agradecemos sua participação!"

        desempenho_lines = variaveis.formata_texto(desempenho, variaveis.largura - variaveis.margem_lateral, variaveis.fonte_texto)
        posicao_text = variaveis.fonte_gigante.render(posicao_usuario, True, variaveis.amarelo)
        agradecimento_lines = variaveis.formata_texto(agradecimento, variaveis.largura - variaveis.margem_lateral, variaveis.fonte_texto)
        agradecimento_text = variaveis.fonte_texto_inicial.render(agradecimento, True, variaveis.laranja)
        
        # Posiciona os textos na tela
        desempenho_x, desempenho_y = variaveis.margem_lateral, altura_texto*4
        posicao_x, posicao_y = (variaveis.largura - posicao_text.get_width())//2, (variaveis.altura - posicao_text.get_height())//2
        agradecimento_x, agradecimento_y =  (variaveis.largura - agradecimento_text.get_width()) // 2, y-50

        for i, line in enumerate(desempenho_lines):
            desempenho_text = variaveis.fonte_texto.render(line, True, variaveis.preto)
            janela.blit(desempenho_text, (desempenho_x, desempenho_y + i * 30))

        for i, line in enumerate(agradecimento_lines):
            agradecimento_text = variaveis.fonte_texto.render(line, True, variaveis.preto)
            janela.blit(agradecimento_text, (agradecimento_x, agradecimento_y + i * 30))
        
        janela.blit(posicao_text, (posicao_x, posicao_y))

        # Círculo em volta da posição
        raio = 50
        pygame.draw.arc(janela, variaveis.preto, (variaveis.largura//2 - raio, variaveis.altura//2 - raio, raio * 2, raio * 2), math.radians(0), math.radians(360), 3)

        variaveis.posiciona_logo(janela)

        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if variaveis.botao_clicado(pygame.Rect((x,y), (largura,altura))):
                    return "inicio"
            elif evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()