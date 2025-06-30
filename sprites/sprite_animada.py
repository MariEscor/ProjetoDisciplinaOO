# sprite_animada.py

import pygame
from Projeto.config import Config
from sprites.sprite import Sprite
from typing import List, Union

class SpriteAnimada(Sprite):
    """
    Representa uma sprite que possui múltiplos frames e pode ser animada.

    Esta classe estende a classe base Sprite e adiciona a funcionalidade
    de animação, permitindo que a sprite mude sua aparência ao longo do tempo.

    Atributos:
        __frames_index (float): O índice atual do frame da animação (float para precisão).
        __frames (list[pygame.Surface]): Uma lista de superfícies Pygame, cada uma representando um frame da animação.
    """
    def __init__(self, pos: tuple[int, int], frames: List[pygame.Surface], groups: pygame.sprite.Group, z: float = Config.CAMADAS_MUNDO['main']) -> None:
        self.__frames_index: float = 0.0
        self.__frames: List[pygame.Surface]  = frames
        img_inicial: pygame.Surface = frames[int(self.frames_index)] if frames else pygame.Surface((1, 1), pygame.SRCALPHA) 
        super().__init__(pos, img_inicial, groups, z)

    @property
    def frames_index(self) -> float:
        return self.__frames_index

    @frames_index.setter
    def frames_index(self, value: Union[float, int]) -> None:
        if not isinstance(value, (float, int)) or value < 0:
            raise ValueError("O 'frames_index' deve ser um número (float ou int) não negativo.")
        self.__frames_index = value

    @property
    def frames(self) -> List[pygame.Surface]:
        return self.__frames

    @frames.setter
    def frames(self, value: List[pygame.Surface]) -> None:
        if not isinstance(value, list) or not all(isinstance(f, pygame.Surface) for f in value):
            raise ValueError("Os 'frames' devem ser uma lista de superfícies Pygame.")
        self.__frames = value

    def animado(self, dt: float) -> None:
        if not self.frames:
            return
        self.frames_index += Config().vel_animacao * dt 
        self.image = self.frames[int(self.frames_index) % len(self.frames)]

    def update(self, dt: float) -> None:
        self.animado(dt)
