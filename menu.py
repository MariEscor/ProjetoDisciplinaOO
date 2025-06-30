#!/usr/bin/python3.4
import pygame, sys
from os.path import join as path_join
from save_manager import load_progress
from scene_manager import load_scene
from bag_manager import reset_bag

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((1280, 720))
mainClock = pygame.time.Clock()

# Fontes
font = pygame.font.Font(path_join("background", "PokemonGb-RAeo.ttf"), 20)
fontxl = pygame.font.Font(path_join("background", "PokemonGb-RAeo.ttf"), 30)

# Sons
# Sons
pygame.mixer.init()
menu_music = None
hover_sfx = None
click_sfx = None

try:
    menu_music = pygame.mixer.Sound(path_join("background", "menu_music.ogg"))
except Exception as e:
    print(f"[ERRO] Falha ao carregar música de menu: {e}")

try:
    hover_sfx = pygame.mixer.Sound(path_join("background", "hover.mp3"))
    hover_sfx.set_volume(0.3)
except Exception as e:
    print(f"[ERRO] Falha ao carregar efeito sonoro de hover: {e}")

try:
    click_sfx = pygame.mixer.Sound(path_join("background", "click.mp3"))
    click_sfx.set_volume(0.5)
except Exception as e:
    print(f"[ERRO] Falha ao carregar efeito sonoro de clique: {e}")


# Volume default
volume_music = 0.5
volume_sfx = 0.5
if menu_music:
    menu_music.set_volume(volume_music)

# Estado de hover anterior para evitar repetição de som
prev_hover = None

def draw_text(text, font, color, surface, x, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(topleft=(x, y))
    surface.blit(surf, rect)

def draw_button(surface, text, font, rect, bg_color, text_color, hover=False, border_radius=60):
    pygame.draw.rect(surface, bg_color, rect, border_radius=border_radius)
    if hover:
        pygame.draw.rect(surface, (250, 183, 0), rect, width=6, border_radius=border_radius)
    surf = font.render(text, False, text_color)
    rect_txt = surf.get_rect(center=rect.center)
    surface.blit(surf, rect_txt)

def handle_audio(state):
    if state in ("menu", "options", "leaderboard"):
        if menu_music and not pygame.mixer.get_busy():
            menu_music.play(loops=-1)
    else:
        if menu_music:
            menu_music.stop()

def main_menu():
    handle_audio("menu")
    global volume_music, volume_sfx, prev_hover

    bg = pygame.image.load(path_join("background", "background_menu.png")).convert_alpha()
    buttons = [
        ("Jogar", pygame.Rect(90, 90, 300, 100), "game_menu"),
        ("opçoes", pygame.Rect(90, 237, 300, 100), "options"),
        ("Leaderboard", pygame.Rect(90, 383, 300, 100), "leaderboard"),
        ("Sair", pygame.Rect(90, 530, 300, 100), "exit"),
    ]

    while True:
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if click_sfx:
                    click_sfx.play()

        for name, rect, target in buttons:
            hov = rect.collidepoint((mx, my))
            if hov and prev_hover != name:
                if hover_sfx:
                    hover_sfx.play()
                prev_hover = name
            draw_button(screen, name, font, rect, (250, 10, 9), (255, 255, 255), hover=hov)
            if click and hov:
                return target

        prev_hover = None if not any(r.collidepoint((mx,my)) for _,r,_ in buttons) else prev_hover
        pygame.display.update()
        mainClock.tick(60)

def options():
    handle_audio("options")
    global volume_music, volume_sfx, prev_hover

    background = pygame.image.load(path_join("background", "background_menu.png")).convert_alpha()

    # Decorativos
    menu_options = pygame.Rect(-40, 100, 360, 100)
    volume_music_rect = pygame.Rect(-40, 210, 590, 70)
    volume_sfx_rect = pygame.Rect(-40, 420, 590, 70)
    button_back = pygame.Rect(-40, 630, 360, 70)

    # Sliders reais
    button_music = pygame.Rect(10, 315, 400, 20)
    button_sfx = pygame.Rect(10, 535, 400, 20)
    knob_radius = 16

    dragging_music = False
    dragging_sfx = False

    while True:
        screen.blit(background, (0, 0))
        mx, my = pygame.mouse.get_pos()
        click = False
        release = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if pygame.Rect(knob_x(button_music, volume_music, knob_radius), button_music.y - knob_radius, knob_radius*2, knob_radius*2).collidepoint(mx, my):
                    dragging_music = True
                elif pygame.Rect(knob_x(button_sfx, volume_sfx, knob_radius), button_sfx.y - knob_radius, knob_radius*2, knob_radius*2).collidepoint(mx, my):
                    dragging_sfx = True
                elif button_back.collidepoint((mx, my)):
                    click_sfx.play()
                    return "menu"
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_music = dragging_sfx = False
                release = True

        if dragging_music:
            volume_music = max(0, min(1, (mx - button_music.x) / button_music.w))
            if menu_music:
                menu_music.set_volume(volume_music)
        if dragging_sfx:
            volume_sfx = max(0, min(1, (mx - button_sfx.x) / button_sfx.w))
            if hover_sfx:
                hover_sfx.set_volume(volume_sfx)
            if click_sfx:
                click_sfx.set_volume(volume_sfx)

        # Hover SFX
        if button_back.collidepoint((mx, my)) and prev_hover != "back":
            hover_sfx.play()
            prev_hover = "back"
        elif not button_back.collidepoint((mx, my)):
            prev_hover = None

        # Interface gráfica
        draw_button(screen, "", font, menu_options, (20, 64, 120), (255, 255, 255))
        draw_text("Opções", fontxl, (255, 255, 255), screen, 20, 130)
        draw_button(screen, "", font, volume_music_rect, (56, 128, 67), (255, 255, 255))
        draw_text("Volume da música", font, (255, 255, 255), screen, 20, 235)
        draw_button(screen, "", font, volume_sfx_rect, (56, 128, 67), (255, 255, 255))
        draw_text("Volume dos efeitos sonoros", font, (255, 255, 255), screen, 20, 435)
        draw_button(screen, "", font, button_back, (250, 10, 9), (255, 255, 255), hover=button_back.collidepoint((mx, my)))
        draw_text("Voltar ao menu", font, (255, 255, 255), screen, 20, 655)

        # Sliders visuais com aparência aprimorada
        for rect, value, is_dragging in [(button_music, volume_music, dragging_music), (button_sfx, volume_sfx, dragging_sfx)]:
            pygame.draw.rect(screen, (120, 120, 120), rect, border_radius=8)  # linha cinza

            filled_rect = pygame.Rect(rect.x, rect.y, int(rect.w * value), rect.h)
            pygame.draw.rect(screen, (255, 255, 255), filled_rect, border_radius=8)  # faixa branca de volume

            kx = knob_x(rect, value, knob_radius)
            hover = pygame.Rect(kx, rect.y - knob_radius, knob_radius*2, knob_radius*2).collidepoint(mx, my)
            knob_color = (255, 255, 255) if not hover else (255, 220, 0)
            pygame.draw.circle(screen, knob_color, (int(kx + knob_radius), rect.y + rect.h // 2), knob_radius)


        pygame.display.update()
        mainClock.tick(60)

def knob_x(slider_rect, value, radius):
    return slider_rect.x + int(value * slider_rect.w) - radius


def leaderboard():
    handle_audio("leaderboard")
    while True:
        screen.fill((0, 0, 0))
        draw_text("Leaderboard", font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
        pygame.display.update()
        mainClock.tick(60)

def game_menu():
    handle_audio("menu")
    global volume_music, volume_sfx, prev_hover

    bg = pygame.image.load(path_join("background", "background_menu.png")).convert_alpha()

    button_novo = pygame.Rect(90, 90, 300, 100)
    button_continuar = pygame.Rect(90, 237, 300, 100)
    button_back = pygame.Rect(-40, 630, 360, 70)

    while True:
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if click_sfx:
                    click_sfx.play()

        buttons = [
            ("Novo jogo", button_novo, "selecionar"),
            ("Continuar", button_continuar, "continuar"),
            ("", button_back, "menu"),
        ]

        for name, rect, target in buttons:
            hov = rect.collidepoint((mx, my))
            if hov and prev_hover != name:
                if hover_sfx:
                    hover_sfx.play()
                prev_hover = name

            draw_button(screen, name, font, rect, (250, 10, 9), (255, 255, 255), hover=hov)
            draw_text("Voltar ao menu", font, (255, 255, 255), screen, 20, 655)
            if click and hov:
                if target == "selecionar":
                    reset_bag()  # ⚠️ Resetar a bag ao iniciar novo jogo
                return target

        # Resetar hover se nenhum botão estiver sob o cursor
        prev_hover = None if not any(r.collidepoint((mx, my)) for _, r, _ in buttons) else prev_hover

        pygame.display.update()
        mainClock.tick(60)

def continuar():
    handle_audio("game")
    data = load_progress()
    if data:
        # Passa os dados carregados como argumento extra
        load_scene("jogo", save_data=data)
    else:
        print("Nenhum save encontrado.")
    return "menu"  # após sair do jogo, volta pro menu

def run_game():
    state = "menu"
    while True:
        if state == "menu":
            state = main_menu()
        elif state == "options":
            state = options()
        elif state == "leaderboard":
            state = leaderboard()
        elif state == "selecionar":
            load_scene("selection")
            state = "menu"
        elif state == "game_menu":
            state = game_menu()
        elif state == "continuar":
            state = continuar()
        elif state == "exit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    run_game()
