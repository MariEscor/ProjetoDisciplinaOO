# sprite.py

import pygame
from bases.config import Config
from typing import Union

class Sprite(pygame.sprite.Sprite):
    """
    Classe base para todas as sprites visuais do jogo.

    Esta classe herda de pygame.sprite.Sprite e gerencia as propriedades
    básicas de uma sprite, como imagem, posição, camada de profundidade (z-index),
    ordenação vertical (y-sort) e uma hitbox para colisões.

    Atributos:
        __image (pygame.Surface): A superfície da imagem da sprite.
        __rect (pygame.FRect): O retângulo da sprite, que define sua posição e tamanho.
                                Usamos FRect para maior precisão com floats.
        __z (float): A camada de profundidade da sprite para ordenação de desenho.
                    Sprites com 'z' menor são desenhadas primeiro (mais ao fundo).
        __y_sort (float): O valor de ordenação vertical da sprite, usado para decidir
                        qual sprite é desenhada "acima" da outra em um ambiente isométrico.
                        Geralmente é o centro Y do retângulo da sprite.
        __hitbox (pygame.FRect): Um retângulo para detecção de colisões. Inicialmente
                                uma cópia de '__rect', mas pode ser ajustada em subclasses.
    """
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: pygame.sprite.Group, z: float = Config.CAMADAS_MUNDO['main']) -> None:
        super().__init__(groups)
        self.__image: pygame.Surface = surf
        self.__rect: pygame.FRect = self.__image.get_frect(topleft = pos)

        self.__z: float = z
        self.__y_sort: float = float(self.__rect.centery)
        self.__hitbox: pygame.FRect = self.__rect.copy() 

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'image' deve ser uma instância de pygame.Surface.")
        self.__image = value

    @property
    def rect(self) -> pygame.FRect:
        return self.__rect

    @rect.setter
    def rect(self, value: pygame.FRect) -> None:
        if not isinstance(value, (pygame.FRect, pygame.Rect)):
            raise TypeError("A 'rect' deve ser uma instância de pygame.FRect ou pygame.Rect.")            
        self.__rect = value

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("A camada 'z' deve ser um número (float ou int).")
        self.__z = float(value)        

    @property
    def y_sort(self) -> float:
        return self.__y_sort

    @y_sort.setter
    def y_sort(self, value: float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("O 'y_sort' deve ser um número (float ou int).")
        self.__y_sort = value

    @property
    def hitbox(self) -> pygame.FRect:
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, value: pygame.FRect) -> None:
        if not isinstance(value, (pygame.FRect, pygame.Rect)):
            raise TypeError("A 'hitbox' deve ser uma instância de pygame.FRect ou pygame.Rect.")
        self.__hitbox = value