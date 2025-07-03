# sprite_transicao.py

import pygame
from sprites.sprite import Sprite

class SpriteTransicao(Sprite):
    """
    Representa uma área invisível no mapa que, ao ser colidida pelo jogador,
    ativa uma transição para outro mapa ou estado do jogo.

    Esta sprite é essencial para criar pontos de passagem entre diferentes
    cenários (e.g., sair de uma casa para o mundo exterior).

    Atributos:
        __target (tuple[str, str]): Uma tupla contendo a posição inicial do jogador
                                    no mapa de destino e o nome do arquivo .tmx do mapa
                                    (e.g., ('fogo', 'mundo')). fogo == player e mundo == mundo.tmx 
    """
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], target: tuple[str, str], groups: pygame.sprite.Group) -> None:
        surf: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        super().__init__(pos, surf, groups)
        self.__target: tuple[str, str]  = target

    @property
    def target(self) -> tuple[str, str]:
        return self.__target

    @target.setter
    def target(self, value: tuple[str, str]) -> None:
        if not isinstance(value, tuple) or len(value) != 2 or not all(isinstance(s, str) for s in value):
            raise ValueError("O 'target' deve ser uma tupla de dois strings.")
        self.__target = value