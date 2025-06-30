# borda_sprite.py

import pygame
from sprites.sprite import Sprite


class BordaSprite(Sprite):
    """
    Representa uma sprite de borda ou "parede" no jogo.

    Esta classe herda de Sprite e é especificamente utilizada para criar
    elementos de cenário que atuam como barreiras de colisão, impedindo
    que outras entidades (como o jogador) passem por elas. A hitbox
    desta sprite é uma cópia exata do seu retângulo visual.

    Atributos:
        N/A (herda e utiliza '__image', '__rect', '__z', '__y_sort' e '__hitbox' de Sprite).
    """
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: pygame.sprite.Group) -> None:
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()