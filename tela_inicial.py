import pygame as pg
import sys
import variaveis

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.font_size = h - 10
        self.font = pg.font.SysFont('Arial', self.font_size)
        self.scroll_offset = 0
        self.txt_surface = self.font.render('', True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        self.txt_surface = self.font.render(self.text, True, self.color)

        # Cria um recorte do texto para mantê-lo dentro da caixa de texto
        text_width, _ = self.font.size(self.text)
        scroll = max(0, text_width - self.rect.w)
        if scroll > 0:
            # Calcula quantos caracteres cabem horizontalmente na caixa de texto
            characters_fit = len(self.text) * ((self.rect.w-10) / text_width)
            characters_fit = max(int(characters_fit), 0)

            # Recorta o texto para mostrar apenas a quantidade de caracteres que cabem
            self.txt_surface = self.font.render(self.text[-characters_fit:], True, self.color)
        else:
            self.txt_surface = self.font.render(self.text, True, self.color)
        return self.text

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)

        # Centraliza o texto verticalmente na caixa de texto
        text_y = self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2
        screen.blit(self.txt_surface, (self.rect.x + 5, text_y))

def tela_inicial(janela):
    altura_texto = 32
    altura_inputbox = 32
    input_box_nome = InputBox(variaveis.margem_lateral, altura_texto*7+30, variaveis.largura - variaveis.margem_lateral*2, altura_inputbox)
    input_box_email = InputBox(variaveis.margem_lateral, altura_texto*11, variaveis.largura - variaveis.margem_lateral*2, altura_inputbox)
    nome_preenchido = False
    email_preenchido = False
    aviso = ""  # Variável para armazenar o texto do aviso

    while True:
        janela.fill(variaveis.branco)
        x, y, largura, altura = variaveis.largura//2 - variaveis.largura_botao//2, altura_texto*14, variaveis.largura_botao, variaveis.altura_botao
        pg.draw.rect(janela, variaveis.laranja, ((x,y), (largura,altura)))

        variaveis.desenhar_retangulo_com_texto(janela, x, y, largura, altura, variaveis.laranja, variaveis.branco, "Iniciar", variaveis.fonte_texto)

        for evento in pg.event.get():
            nome = input_box_nome.handle_event(evento)
            email = input_box_email.handle_event(evento)
            if evento.type == pg.MOUSEBUTTONDOWN:
                if variaveis.botao_clicado(pg.Rect((x,y), (largura,altura))):
                    if input_box_nome.text.strip() != '':
                        nome_preenchido = True
                    if input_box_email.text.strip() != '' and '@' in input_box_email.text and '.' in input_box_email.text:
                        email_preenchido = True
                            
                    if nome_preenchido and email_preenchido:
                        variaveis.Jogador.nome = nome
                        variaveis.Jogador.email = email
                        return "jogo"
                    else:
                        if not(nome_preenchido):
                            aviso = "Campo de nome vazio"
                        elif not(email_preenchido):
                            aviso = "Preencha o email coretamente"
                    
            elif evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        
        input_box_nome.draw(janela)  
        input_box_email.draw(janela) 

        # Renderiza os textos na tela
        intro_lines = variaveis.formata_texto(variaveis.intro, variaveis.largura - variaveis.margem_lateral, variaveis.fonte_texto)
        intro_text = variaveis.fonte_texto_inicial.render(intro_lines[0], True, variaveis.laranja)
        desenvolvimento_lines = variaveis.formata_texto(variaveis.desenvolvimento, variaveis.largura - 2*variaveis.margem_lateral, variaveis.fonte_texto)

        # Posição dos textos na tela
        intro_x, intro_y = (variaveis.largura - intro_text.get_width()) // 2, altura_texto + 10 # Texto centralizado
        desenvolvimento_x, desenvolvimento_y = variaveis.margem_lateral, altura_texto*3
        nome_x, nome_y = variaveis.margem_lateral, altura_texto*7
        email_x, email_y = variaveis.margem_lateral, altura_texto*10

        # Desenha os textos na tela, pulando para a próxima linha quando necessário
        for i, line in enumerate(intro_lines):
            intro_text = variaveis.fonte_texto_inicial.render(line, True, variaveis.laranja)
            janela.blit(intro_text, (intro_x, intro_y + i * 30)) 

        for i, line in enumerate(desenvolvimento_lines):
            desenvolvimento_text = variaveis.fonte_texto.render(line, True, variaveis.preto)
            janela.blit(desenvolvimento_text, (desenvolvimento_x, desenvolvimento_y + i * 30))

        nome_text = variaveis.fonte_legenda.render(variaveis.texto_nome, True, variaveis.preto)
        janela.blit(nome_text, (nome_x,nome_y))

        email_text = variaveis.fonte_legenda.render(variaveis.texto_email, True, variaveis.preto)
        janela.blit(email_text, (email_x,email_y))

        # Renderização do aviso centralizado acima do botão "Iniciar"
        if aviso:
            aviso_fonte = variaveis.fonte_legenda.render(aviso, True, variaveis.amarelo)
            aviso_x = variaveis.largura // 2 - aviso_fonte.get_width() // 2
            aviso_y = altura_texto * 13.5 - aviso_fonte.get_height()
            janela.blit(aviso_fonte, (aviso_x, aviso_y))
        

        variaveis.posiciona_logo(janela)

        pg.display.flip() 
        pg.display.update()

