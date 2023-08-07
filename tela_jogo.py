import pygame
import math
import sys
import variaveis
import random
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def seleciona_perguntas():
    # Seleciona 10 perguntas aleatoriamente: 3 fáceis, 4 médias e 3 difíceis
    perguntas_faceis = random.sample(list(variaveis.opcoes_respostas["faceis"].keys()), 3)
    perguntas_medias = random.sample(list(variaveis.opcoes_respostas["medias"].keys()), 4)
    perguntas_dificeis = random.sample(list(variaveis.opcoes_respostas["dificeis"].keys()), 3)
    perguntas_selecionadas = perguntas_faceis + perguntas_medias + perguntas_dificeis
    random.shuffle(perguntas_selecionadas)
    return perguntas_selecionadas

def exibe_opcoes(janela, pergunta, opcao_selecionada):
    # Exibe as opções de resposta para a pergunta selecionada
    y_pos = 300 # Posição vertical inicial das opções de resposta
    for modalidade, conjunto_questao in variaveis.opcoes_respostas.items():
        for questao, opcoes in conjunto_questao.items():
            if pergunta == questao:
                alternativas = opcoes
                for i, opcao in enumerate(opcoes):
                    if i == opcao_selecionada:
                        cor_texto = variaveis.laranja
                    else:
                        cor_texto = variaveis.preto
                    texto_opcao = variaveis.fonte_texto.render(opcao, True, cor_texto)
                    janela.blit(texto_opcao, (100, y_pos))
                    y_pos += 50 
    return alternativas

def grava_na_planilha(acertos, tempo_decorrido, ranking):
    # Grava os dados no Google Sheets e atualiza dados da clasee Jogador
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    client = gspread.authorize(credentials)
    spreadsheet_id = '1XWSPN-6Oefi9xpcWCFqDrw5abLBbRNuZoYhySkap_K4' # ID da planilha        
    sheet = client.open_by_key(spreadsheet_id).worksheet(variaveis.Jogador.estande_selecionado)
    
    variaveis.Jogador.tempo = tempo_decorrido
    variaveis.Jogador.acertos = acertos
    variaveis.Jogador.acerto_por_tempo = float("{:.9f}".format(ranking))
    dados = [variaveis.Jogador.nome, variaveis.Jogador.email, variaveis.Jogador.acerto_por_tempo, variaveis.Jogador.acertos, variaveis.Jogador.tempo]
    sheet.append_row(dados)

    valores_acertos_tempo = sheet.col_values(3)[4:]
    valores_acertos_tempo = [float(valor) for valor in valores_acertos_tempo]
    valores_acertos_tempo.sort(reverse=True)
    jogador_posicao = valores_acertos_tempo.index(variaveis.Jogador.acerto_por_tempo) + 1
    variaveis.Jogador.posicao = jogador_posicao

    qtd_jogadores = len(sheet.col_values(1)[4:])
    variaveis.Jogador.participantes = qtd_jogadores

def desenha_circulo_contador(janela, angulo):
    # Desenha o círculo de contagem regressiva
    pos_x, pos_y = variaveis.largura - 50, 50
    raio = 40
    espessura = 3
    cor_circulo = variaveis.amarelo
    angulo_rad = math.radians(angulo)
           
    # Desenha o arco com o ângulo desejado, criando a animação
    pygame.draw.arc(janela, cor_circulo, pygame.Rect(pos_x - raio, pos_y - raio, raio * 2, raio * 2), -math.pi / 2, -math.pi / 2 + angulo_rad, espessura)

    # Exibe o tempo restante dentro do círculo
    texto_tempo = variaveis.fonte_texto.render(f"{int(angulo / 360 * 30)+1}s", True, variaveis.preto)
    largura_texto, altura_texto = texto_tempo.get_size()
    pos_x_texto = pos_x - largura_texto // 2
    pos_y_texto = pos_y - altura_texto // 2
    janela.blit(texto_tempo, (pos_x_texto, pos_y_texto))

def tela_jogo(janela):
    perguntas = seleciona_perguntas()
    opcao_selecionada = None
    indice_pergunta = 0
    acertos = 0
    tempo_resposta = 0
    tempo_primordial = time.time() # Marca o início do jogo
    tempo_inicio = time.time() # Marca o início do ciclo de cada pergunta

    while indice_pergunta<len(perguntas):
        janela.fill(variaveis.branco)

        # Exibir a pergunta
        pergunta = perguntas[indice_pergunta]
        texto_pergunta = variaveis.fonte_texto.render(pergunta, True, variaveis.preto)
        janela.blit(texto_pergunta, (100, 150))
        opcoes = exibe_opcoes(janela, pergunta, opcao_selecionada)

        # Exibir o círculo de contagem regressiva
        tempo_atual = time.time()
        tempo_resposta = tempo_atual - tempo_inicio
        tempo_restante = max(0, variaveis.limite_tempo - tempo_resposta)
        angulo = (tempo_restante / variaveis.limite_tempo) * 360
        desenha_circulo_contador(janela, angulo)

        x, y, largura, altura = variaveis.largura//2 - variaveis.largura_botao//2, variaveis.altura-100, variaveis.largura_botao, variaveis.altura_botao
        variaveis.desenhar_retangulo_com_texto(janela, x, y, largura, altura, variaveis.azul, variaveis.branco, "Confirmar", variaveis.fonte_texto)

        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if variaveis.botao_clicado(pygame.Rect((x,y), (largura,altura))):
                    if opcao_selecionada is not None:
                        # Verifica se a resposta selecionada pelo jogador está correta
                        acertou = (variaveis.acertos[pergunta] == opcoes[opcao_selecionada])
                        if acertou:
                            acertou = False
                            acertos += 1
                        indice_pergunta += 1
                        opcao_selecionada = None
                        tempo_resposta = 0
                        tempo_inicio = time.time()  # Reinicia o tempo de início para a próxima pergunta


                else:
                    # Verifica se alguma opção foi clicada
                    y_pos = 300
                    for i in range(len(opcoes)):
                        if 100 < evento.pos[0] < 700 and y_pos < evento.pos[1] < y_pos + 50:
                            opcao_selecionada = i
                            break
                        y_pos += 50

            elif evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        tempo_atual = time.time()
        tempo_resposta = tempo_atual - tempo_inicio

        # Verifica se o tempo de resposta da pergunta atual excedeu o limite
        if tempo_resposta >= variaveis.limite_tempo:
            indice_pergunta += 1
            opcao_selecionada = None
            tempo_resposta = 0 
            tempo_inicio = time.time()
            
        variaveis.posiciona_logo(janela)
        pygame.display.update()
    
    tempo_decorrido = tempo_atual - tempo_primordial
    ranking = acertos/tempo_decorrido
    grava_na_planilha(acertos,tempo_decorrido, ranking)

    return "score"