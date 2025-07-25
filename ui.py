import pygame
import constants
from pokemon import Pokemon

class UI:
    def __init__(self):
        """Inicializa a UI, carregando a fonte padrão."""
        try:
            self.default_font_path = constants.FONT_PATH
        except AttributeError:
            self.default_font_path = None

    def get_font(self, size: int) -> pygame.font.Font:
        """Carrega e retorna uma fonte, com fallback para a fonte padrão."""
        try:
            return pygame.font.Font(self.default_font_path, size)
        except (pygame.error, TypeError):
            return pygame.font.Font(None, size + 10)

    def draw_text(self, screen: pygame.Surface, text: str, size: int, color: tuple, center_pos: tuple) -> None:
        """Desenha texto centralizado na tela."""
        font = self.get_font(size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)

    def draw_message_box(self, screen: pygame.Surface, message: str) -> None:
        """Desenha a caixa de mensagem na parte inferior da tela."""
        message_box_width = constants.LARGURA_JANELA - 120
        message_box_x = (constants.LARGURA_JANELA - message_box_width) // 2
        message_box_y = constants.UI_AREA_Y + 46
        message_box_height = 60
        box_rect = pygame.Rect(message_box_x, message_box_y, message_box_width, message_box_height)
        
        pygame.draw.rect(screen, constants.GREEN_GREY, box_rect)
        pygame.draw.rect(screen, constants.GREEN_GREY, box_rect, 0)  # A borda é desenhada sobre o preenchimento
        self.draw_text(screen, message, 24, constants.WHITE, box_rect.center)

    def draw_pokemon_hp(self, screen: pygame.Surface, pokemon: Pokemon, position_type: str) -> None:
        """Desenha a barra de vida e informações do Pokémon."""
        bar_width = 250
        bar_height = 20
        hp_ratio = pokemon.get_hp_ratio()

        if position_type == 'player':
            hp_bar_x = 830
            hp_bar_y = constants.ALTURA_JANELA - constants.UI_AREA_HEIGHT - 110
        else:  # rival
            hp_bar_x = constants.LARGURA_JANELA - bar_width - 900
            hp_bar_y = 85

        name_font = self.get_font(24)
        name_text = name_font.render(f'{pokemon.name} LV.{pokemon.level}', True, constants.BLACK)
        screen.blit(name_text, (hp_bar_x, hp_bar_y - 35))

        pygame.draw.rect(screen, constants.RED, (hp_bar_x, hp_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, constants.GREEN, (hp_bar_x, hp_bar_y, bar_width * hp_ratio, bar_height))

        hp_font = self.get_font(20)
        hp_text_str = f'HP: {pokemon.get_current_hp()} / {pokemon.get_max_hp()}'
        hp_text = hp_font.render(hp_text_str, True, constants.BLACK)
        screen.blit(hp_text, (hp_bar_x, hp_bar_y + bar_height + 5))

    def draw_button(self, screen: pygame.Surface, rect: pygame.Rect, label: str) -> None:
        """Desenha um botão com um rótulo em um retângulo específico."""
        mouse_pos = pygame.mouse.get_pos()
        color = constants.GOLD if rect.collidepoint(mouse_pos) else constants.WHITE

        pygame.draw.rect(screen, color, rect, border_radius=5)

        font = self.get_font(30)
        text = font.render(label, True, constants.BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
