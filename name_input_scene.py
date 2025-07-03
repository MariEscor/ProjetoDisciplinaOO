import pygame
import sys
import os
import time
from os.path import join as path_join
from bases import timer
from bases.leaderboard_manager import LeaderboardManager
from scene_manager import SceneManager

class NameInputScene:
    def __init__(self):
        pygame.init()
        self._largura_tela = 1280
        self._altura_tela = 720
        self._screen = pygame.display.set_mode((self._largura_tela, self._altura_tela))
        pygame.display.set_caption("Tela de Nome")
        self._scene_manager = SceneManager()
        self._leaderboard_manager = LeaderboardManager()

        script_dir = os.path.dirname(__file__)
        self._background = pygame.image.load(path_join(script_dir, 'background', 'pikachu_nome.jpg')).convert_alpha()
        self._font = pygame.font.Font(path_join(script_dir, 'PokemonGb-RAeo.ttf'), 20)

        self._nome = ""
        self._digitando = False
        self._clock = pygame.time.Clock()
        self._elapsed_time = time.time() - timer.game_start_time if timer.game_start_time else 0.0

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            texto_principal = self._font.render("Escolha seu nome para o Leaderboard.", True, (0, 0, 0))
            texto_rect = texto_principal.get_rect(centerx=self._largura_tela // 2)
            texto_rect.y = self._altura_tela // 2 - 100

            texto_temp = self._font.render(self._nome, True, (0, 0, 0))
            input_width = max(300, texto_temp.get_width() + 10)
            input_rect = pygame.Rect((self._largura_tela - input_width) // 2, texto_rect.bottom + 20, input_width, 50)

            button_rect = pygame.Rect((self._largura_tela - 200) // 2, input_rect.bottom + 40, 200, 60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif self._digitando:
                        if event.key == pygame.K_BACKSPACE:
                            self._nome = self._nome[:-1]
                        elif event.key == pygame.K_RETURN and self._nome:
                            self._leaderboard_manager.save_score(self._nome, self._elapsed_time)
                            self._scene_manager.load_scene("leaderboard")
                            running = False
                        else:
                            self._nome += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        self._digitando = True
                    else:
                        self._digitando = False

                    if button_rect.collidepoint(event.pos) and self._nome:
                        self._leaderboard_manager.save_score(self._nome, self._elapsed_time)
                        self._scene_manager.load_scene("leaderboard")
                        running = False

            self._screen.blit(self._background, (0, 0))
            self._screen.blit(texto_principal, texto_rect)
            pygame.draw.rect(self._screen, (239, 242, 169), input_rect)
            pygame.draw.rect(self._screen, (0, 0, 0), input_rect, 3)
            self._screen.blit(texto_temp, (input_rect.x + 5, input_rect.y + (input_rect.height - texto_temp.get_height()) // 2))

            pygame.draw.rect(self._screen, (196, 8, 8), button_rect, border_radius=60)
            surf = self._font.render("Próximo", False, (0, 0, 0))
            self._screen.blit(surf, surf.get_rect(center=button_rect.center))

            pygame.display.flip()
            self._clock.tick(30)

        pygame.quit()
