# Projeto/leaderboard_scene.py
import pygame
import sys
import os
from os.path import join as path_join
from bases.leaderboard_manager import LeaderboardManager
from scene_manager import SceneManager

class LeaderboardScene:
    def __init__(self):
        """Inicializa tela de leaderbord"""
        pygame.init()
        
        self._largura_tela = 1280
        self._altura_tela = 720
        self._screen = pygame.display.set_mode((self._largura_tela, self._altura_tela))
        pygame.display.set_caption("Leaderboard")

        # Load resources
        script_dir = os.path.dirname(__file__)
        self._background = pygame.image.load(path_join(script_dir, '..', 'background', 'fundo_escolha.png')).convert()
        self._font = pygame.font.Font(path_join(script_dir, '..', 'background', 'PokemonGb-RAeo.ttf'), 24)
        self._font_title = pygame.font.Font(path_join(script_dir, '..', 'background', 'PokemonGb-RAeo.ttf'), 48)

        # Colors
        self._white = (255, 255, 255)
        self._black = (0, 0, 0)
        self._gold = (255, 215, 0)

        self._leaderboard_manager = LeaderboardManager()
        self._scene_manager = SceneManager()
        self._clock = pygame.time.Clock()

    def _draw_text(self, text, font, color, x, y):
        """Helper function to draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self._screen.blit(text_surface, text_rect)

    def _format_time(self, total_seconds):
        """Formats total seconds into MM:SS format."""
        if total_seconds is None:
            return "N/A"
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def run(self):
        """The main loop for the leaderboard scene."""
        running = True
        scores = self._leaderboard_manager.load_leaderboard()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        # Use the scene manager to transition back to the menu
                        self._scene_manager.load_scene("menu")
                        running = False # Exit the current scene loop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Also allow clicking to go back
                    self._scene_manager.load_scene("menu")
                    running = False

            # Drawing
            self._screen.blit(self._background, (0, 0))
            self._draw_text("Leaderboard", self._font_title, self._gold, self._largura_tela // 2, 80)

            # Display scores
            start_y = 180
            for i, score in enumerate(scores[:10]):  # Show top 10
                y = start_y + i * 50
                rank = f"{i + 1}."
                name = score.get("name", "Anonymous")
                time_str = self._format_time(score.get("elapsed_time"))

                self._draw_text(rank, self._font, self._white, 200, y)
                self._draw_text(name, self._font, self._white, self._largura_tela // 2, y)
                self._draw_text(time_str, self._font, self._white, self._largura_tela - 200, y)

            self._draw_text("Pressione ESC ou ENTER para voltar ao Menu", self._font, self._white, self._largura_tela // 2, 680)
            
            pygame.display.flip()
            self._clock.tick(60)

# This allows running the scene directly if needed for testing,
# but the main flow will be through the scene_manager
if __name__ == '__main__':
    LeaderboardScene().run()