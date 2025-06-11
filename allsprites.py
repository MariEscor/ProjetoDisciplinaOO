import pygame
from pygame.math import Vector2 as vector

class AllSprites(pygame.sprite.Group):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.display_surface = pygame.display.get_surface()
        self.offset = vector(100, 20)

    def draw(self, jogador_centro):
        self.offset.x = -(jogador_centro[0] - self.config.larguraJanela / 2)
        self.offset.y = -(jogador_centro[1] - self.config.alturaJanela / 2)

        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
