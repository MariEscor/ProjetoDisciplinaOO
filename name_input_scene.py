import pygame, sys
from os.path import join as path_join
import os # Import the os module

pygame.init()

# Configurações da tela
largura_tela = 1280
altura_tela = 720
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Tela de Nome")

# Cores
cor_texto = (0, 0, 0)        # Preto (para o texto digitado e para "Escolha seu nome...")
COR_FUNDO_CAIXA = (239, 242, 169)    # Um amarelo claro para o fundo da caixa
COR_BORDA_CAIXA = (0, 0, 0)  # Preto para a borda da caixa
COR_BOTAO_NORMAL = (196, 8, 8) # Um azul claro para o botão
COR_TEXTO_BOTAO = (0, 0, 0) # Preto para o texto do botão

# Função para desenhar texto, ajustada para centralizar se necessário
def draw_text(text, font, color, surface, x, y, center_x=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect(topleft=(x, y))
    if center_x:
        rect.centerx = surface.get_rect().centerx # Centraliza horizontalmente na surface
    surface.blit(surf, rect)
    
def draw_button(surface, text, font, rect, bg_color, text_color, hover=False, border_radius=60):
    # Desenha o fundo do botão
    pygame.draw.rect(surface, bg_color, rect, border_radius=border_radius)
    # Se estiver em hover, desenha a borda amarela
    if hover:
        pygame.draw.rect(surface, (0, 0, 0), rect, width=4, border_radius=border_radius)
    # Renderiza e centraliza o texto do botão
    surf = font.render(text, False, text_color)
    rect_txt = surf.get_rect(center=rect.center)
    surface.blit(surf, rect_txt)
    return rect # Retorna o retângulo do botão para checagem de clique/hover

# Caminho para os recursos
script_dir = os.path.dirname(__file__)
background_path = path_join(script_dir, 'background', 'pikachu_nome.jpg')
font_path = path_join(script_dir, 'PokemonGb-RAeo.ttf')

# Verifica se os recursos existem
if not os.path.exists(background_path):
    print(f"Erro: Imagem de fundo não encontrada em: {background_path}")
    sys.exit()
background = pygame.image.load(background_path).convert_alpha()

if not os.path.exists(font_path):
    print(f"Erro: Fonte não encontrada em: {font_path}")
    sys.exit()
fonte = pygame.font.Font(font_path, 20)

# Entrada do usuário
nome = ""
ativo = False
digitando = False
relogio = pygame.time.Clock()

# Loop principal do jogo
executando = True
while executando:
    # --- Atualização de Posições (tudo que precisa ser recalculado a cada frame) ---
    # Mouse position para hover
    mouse_pos = pygame.mouse.get_pos()

    # Cálculo da posição do texto principal
    texto_principal_surf = fonte.render("Escolha seu nome para o Leaderboard.", True, cor_texto)
    texto_principal_rect = texto_principal_surf.get_rect()
    texto_principal_rect.centerx = largura_tela // 2
    texto_principal_rect.y = altura_tela // 2 - 100 

    # Cálculo da posição da caixa de entrada
    texto_superficie_temp = fonte.render(nome, True, cor_texto)
    input_width = max(300, texto_superficie_temp.get_width() + 10)
    input_height = 50
    input_x = (largura_tela - input_width) // 2
    input_y = texto_principal_rect.bottom + 20 
    input_rect = pygame.Rect(input_x, input_y, input_width, input_height)

    # --- Cálculo da posição do botão "Próximo" ---
    # Vamos usar uma largura e altura fixas para o botão por enquanto, para centralizar
    button_width = 200
    button_height = 60
    button_x = (largura_tela - button_width) // 2 # Centraliza horizontalmente
    button_y = input_rect.bottom + 40 # 40 pixels abaixo da caixa de entrada
    
    # Criamos o objeto Rect para o botão
    proximo_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    # ---------------------------------------------------------------------------------

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        
        # Lógica de clique para a caixa de entrada
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(evento.pos):
                digitando = not digitando
            else:
                digitando = False # Desativa a digitação se clicar fora da caixa
            
            # Lógica de clique para o botão
            if proximo_button_rect.collidepoint(evento.pos):
                print("Botão 'Próximo' clicado!")
                # Aqui você pode adicionar a lógica para avançar para a próxima tela, etc.
                # Por exemplo: executando = False # Para sair do loop
                # Ou chamar uma função que muda o estado do jogo

        # Lógica de teclado para a caixa de entrada
        if evento.type == pygame.KEYDOWN:
            if digitando:
                if evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif evento.key == pygame.K_RETURN:
                    print(nome)
                    digitando = False # Desativa a digitação após ENTER
                else:
                    nome += evento.unicode

    # --- Desenho na tela ---
    tela.blit(background, (0, 0)) # Fundo

    tela.blit(texto_principal_surf, texto_principal_rect) # Texto principal

    # Desenha a caixa de entrada
    pygame.draw.rect(tela, COR_FUNDO_CAIXA, input_rect)
    pygame.draw.rect(tela, COR_BORDA_CAIXA, input_rect, 3)

    # Desenha o texto digitado na caixa
    texto_digitado_x = input_rect.x + 5
    texto_digitado_y = input_rect.y + (input_rect.height - texto_superficie_temp.get_height()) // 2
    tela.blit(texto_superficie_temp, (texto_digitado_x, texto_digitado_y))

    # --- Desenha o botão "Próximo" ---
    # Verifica se o mouse está sobre o botão para o efeito hover
    hover_proximo = proximo_button_rect.collidepoint(mouse_pos)
    draw_button(tela, "Próximo", fonte, proximo_button_rect, COR_BOTAO_NORMAL, COR_TEXTO_BOTAO, hover=hover_proximo, border_radius=60)
    # ----------------------------------

    pygame.display.flip()
    relogio.tick(30)

pygame.quit()