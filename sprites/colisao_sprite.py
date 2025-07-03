# colisao_sprite.py

import pygame
from sprites.sprite import Sprite

class ColisaoSprite(Sprite):
    """
    Representa uma sprite com uma hitbox ajustada para colisões.

    Esta classe é utilizada para criar elementos no cenário que possuem uma hitbox
    menor que a sua imagem visual, simulando colisões mais precisas com a base
    dos objetos (e.g., um personagem colidindo com a base de uma árvore e não com o topo).

    Atributos:
        N/A (Herda e ajusta 'hitbox' da classe Sprite base).
    """
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: pygame.sprite.Group) -> None:
        super().__init__(pos, surf, groups)
        # Ajusta a hitbox para ser 60% menor em altura, centralizada verticalmente.
        self.hitbox = self.rect.inflate(0, -int(self.rect.height * 0.6))
