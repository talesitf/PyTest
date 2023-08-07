import variaveis
from tela_inicial import tela_inicial
from tela_jogo import tela_jogo
from tela_score import tela_score
from estandes import estandes
import pygame
import sys
import asyncio
import math
import random
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

async def main():
    pygame.init()

    janela = pygame.display.set_mode((variaveis.largura, variaveis.altura))

    pygame.display.set_caption(variaveis.nome_tela)

    tela_atual = "estandes"

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Controle de qual tela é exibida
        if tela_atual == "estandes":
            tela_atual = estandes(janela)
        elif tela_atual == "inicio":
            tela_atual = tela_inicial(janela)
        elif tela_atual == "jogo":
            tela_atual = tela_jogo(janela)
        elif tela_atual == "score":
            tela_atual = tela_score(janela)

if __name__ == "__main__":
    asyncio.run(main())