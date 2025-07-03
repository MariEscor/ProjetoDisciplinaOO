# menu.py
import pygame
import sys
from os.path import join as path_join
from save_manager import SaveManager
from scene_manager import SceneManager
from bag_manager import BagManager
from bases.leaderboard_scene import LeaderboardScene
from bases.player_state import player_state
from bases import timer

def resetar_player_state():
    player_state["pos"] = None
    player_state["direction"] = "down"
    player_state["map"] = "mundo"

class MenuManager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('game base')
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self._save_manager = SaveManager()
        self._scene_manager = SceneManager()
        self._bag_manager = BagManager()
        self._leaderboard_scene = LeaderboardScene()
        # Volume
        self.volume_music = 0.5
        self.volume_sfx = 0.5

        # Sons
        pygame.mixer.init()
        self.menu_music = self.load_sound("menu_music.ogg", music=True)
        self.hover_sfx = self.load_sound("hover.mp3", volume=0.3)
        self.click_sfx = self.load_sound("click.mp3", volume=0.5)

        # Fontes
        self.font = pygame.font.Font(path_join("background", "PokemonGb-RAeo.ttf"), 20)
        self.fontxl = pygame.font.Font(path_join("background", "PokemonGb-RAeo.ttf"), 30)

        # Estado do hover
        self.prev_hover = None

    def load_sound(self, filename, volume=0.5, music=False):
        try:
            path = path_join("background", filename)
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            if music:
                self.menu_music = sound
                sound.set_volume(self.volume_music)
            return sound
        except Exception as e:
            print(f"[ERRO] Falha ao carregar {'música' if music else 'som'} '{filename}': {e}")
            return None

    def draw_text(self, text, font, color, surface, x, y):
        surf = font.render(text, True, color)
        rect = surf.get_rect(topleft=(x, y))
        surface.blit(surf, rect)

    def draw_button(self, surface, text, font, rect, bg_color, text_color, hover=False, border_radius=60):
        pygame.draw.rect(surface, bg_color, rect, border_radius=border_radius)
        if hover:
            pygame.draw.rect(surface, (250, 183, 0), rect, width=6, border_radius=border_radius)
        surf = font.render(text, False, text_color)
        rect_txt = surf.get_rect(center=rect.center)
        surface.blit(surf, rect_txt)

    def handle_audio(self, state):
        if state in ("menu", "options", "leaderboard"):
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("background/menu_music.ogg")
                pygame.mixer.music.set_volume(self.volume_music)
                pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()


    def knob_x(self, slider_rect, value, radius):
        return slider_rect.x + int(value * slider_rect.w) - radius

    def main_menu(self):
        self.handle_audio("menu")
        bg = pygame.image.load(path_join("background", "background_menu.png")).convert_alpha()

        buttons = [
            ("Jogar", pygame.Rect(90, 90, 300, 100), "game_menu"),
            ("Opçoes", pygame.Rect(90, 237, 300, 100), "options"),
            ("Leaderboard", pygame.Rect(90, 383, 300, 100), "leaderboard"),
            ("Sair", pygame.Rect(90, 530, 300, 100), "exit"),
        ]

        while True:
            self.screen.blit(bg, (0, 0))
            mx, my = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                    if self.click_sfx:
                        self.click_sfx.play()

            for name, rect, target in buttons:
                hov = rect.collidepoint((mx, my))
                if hov and self.prev_hover != name:
                    if self.hover_sfx:
                        self.hover_sfx.play()
                    self.prev_hover = name
                self.draw_button(self.screen, name, self.font, rect, (250, 10, 9), (255, 255, 255), hover=hov)
                if click and hov:
                    return target

            self.prev_hover = None if not any(r.collidepoint((mx, my)) for _, r, _ in buttons) else self.prev_hover
            pygame.display.update()
            self.clock.tick(60)

    def options_menu(self):
        self.handle_audio("options")
        background = pygame.image.load(path_join("background", "background_menu.png")).convert_alpha()

        menu_options = pygame.Rect(-40, 100, 360, 100)
        volume_music_rect = pygame.Rect(-40, 210, 590, 70)
        volume_sfx_rect = pygame.Rect(-40, 420, 590, 70)
        button_back = pygame.Rect(-40, 630, 360, 70)

        button_music = pygame.Rect(10, 315, 400, 20)
        button_sfx = pygame.Rect(10, 535, 400, 20)
        knob_radius = 16

        dragging_music = False
        dragging_sfx = False

        while True:
            self.screen.blit(background, (0, 0))
            mx, my = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                    if pygame.Rect(self.knob_x(button_music, self.volume_music, knob_radius),
                                   button_music.y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                        dragging_music = True
                    elif pygame.Rect(self.knob_x(button_sfx, self.volume_sfx, knob_radius),
                                     button_sfx.y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                        dragging_sfx = True
                    elif button_back.collidepoint((mx, my)):
                        if self.click_sfx:
                            self.click_sfx.play()
                        return "menu"
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_music = dragging_sfx = False

            if dragging_music:
                self.volume_music = max(0, min(1, (mx - button_music.x) / button_music.w))
                pygame.mixer.music.set_volume(self.volume_music)

            if dragging_sfx:
                self.volume_sfx = max(0, min(1, (mx - button_sfx.x) / button_sfx.w))
                if self.hover_sfx:
                    self.hover_sfx.set_volume(self.volume_sfx)
                if self.click_sfx:
                    self.click_sfx.set_volume(self.volume_sfx)

            if button_back.collidepoint((mx, my)) and self.prev_hover != "back":
                if self.hover_sfx:
                    self.hover_sfx.play()
                self.prev_hover = "back"
            elif not button_back.collidepoint((mx, my)):
                self.prev_hover = None

            self.draw_button(self.screen, "", self.font, menu_options, (20, 64, 120), (255, 255, 255))
            self.draw_text("Opçoes", self.fontxl, (255, 255, 255), self.screen, 20, 130)
            self.draw_button(self.screen, "", self.font, volume_music_rect, (56, 128, 67), (255, 255, 255))
            self.draw_text("Volume da música", self.font, (255, 255, 255), self.screen, 20, 235)
            self.draw_button(self.screen, "", self.font, volume_sfx_rect, (56, 128, 67), (255, 255, 255))
            self.draw_text("Volume dos efeitos sonoros", self.font, (255, 255, 255), self.screen, 20, 435)
            self.draw_button(self.screen, "", self.font, button_back, (250, 10, 9), (255, 255, 255), hover=button_back.collidepoint((mx, my)))
            self.draw_text("Voltar ao menu", self.font, (255, 255, 255), self.screen, 20, 655)

            for rect, value, dragging in [(button_music, self.volume_music, dragging_music), (button_sfx, self.volume_sfx, dragging_sfx)]:
                pygame.draw.rect(self.screen, (120, 120, 120), rect, border_radius=8)
                filled_rect = pygame.Rect(rect.x, rect.y, int(rect.w * value), rect.h)
                pygame.draw.rect(self.screen, (255, 255, 255), filled_rect, border_radius=8)
                kx = self.knob_x(rect, value, knob_radius)
                hover = pygame.Rect(kx, rect.y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my)
                color = (255, 255, 255) if not hover else (255, 220, 0)
                pygame.draw.circle(self.screen, color, (int(kx + knob_radius), rect.y + rect.h // 2), knob_radius)

            pygame.display.update()
            self.clock.tick(60)

    def leaderboard_menu(self):
        self.handle_audio("leaderboard")
        self._leaderboard_scene.run()
        return "menu"

    def game_menu(self):
        self.handle_audio("menu")
        bg = pygame.image.load(path_join("background", "background_menu.png")).convert_alpha()
        button_novo = pygame.Rect(90, 90, 300, 100)
        button_continuar = pygame.Rect(90, 237, 300, 100)
        button_back = pygame.Rect(-40, 630, 360, 70)

        while True:
            self.screen.blit(bg, (0, 0))
            mx, my = pygame.mouse.get_pos()
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                    if self.click_sfx:
                        self.click_sfx.play()

            buttons = [("Novo jogo", button_novo, "selecionar"),
                    ("Continuar", button_continuar, "continuar"),
                    ("", button_back, "menu")]

            for name, rect, target in buttons:
                hov = rect.collidepoint((mx, my))
                if hov and self.prev_hover != name:
                    if self.hover_sfx:
                        self.hover_sfx.play()
                    self.prev_hover = name
                self.draw_button(self.screen, name, self.font, rect, (250, 10, 9), (255, 255, 255), hover=hov)
                self.draw_text("Voltar ao menu", self.font, (255, 255, 255), self.screen, 20, 655)
                if click and hov:
                    if target == "selecionar":
                        self._bag_manager.reset_bag()
                        resetar_player_state()
                        return target
                    elif target == "continuar":
                        return target
                    else:
                        return target

            self.prev_hover = None if not any(r.collidepoint((mx, my)) for _, r, _ in buttons) else self.prev_hover
            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):
        state = "menu"
        while True:
            if state == "menu":
                state = self.main_menu()
            elif state == "options":
                state = self.options_menu()
            elif state == "leaderboard":
                state = self.leaderboard_menu()
            elif state == "game_menu":
                state = self.game_menu()
            elif state == "selecionar":
                next_state = self._scene_manager.load_scene("selection")
                state = next_state or "menu"
            elif state == "continuar":
                data = self._save_manager.load_progress()
                if data:
                    import time
                    timer.game_start_time = time.time() - (data.get("elapsed_time", 0) / 1000)
                    next_state = self._scene_manager.load_scene("mundo_aberto")
                    resetar_player_state()
                    state = next_state or "menu"
                else:
                    print("Nenhum save encontrado.")
                    state = "menu"
            elif state == "exit":
                pygame.quit()
                sys.exit()