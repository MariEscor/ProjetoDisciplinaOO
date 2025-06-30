# sprite_dialogo.py

import pygame
from pygame.math import Vector2 as vector
from Projeto.config import Config
from typing import Union, TYPE_CHECKING 

if TYPE_CHECKING:
    from entidades.entidades import Entidades

class SpriteDialogo(pygame.sprite.Sprite):
    """
    Representa a caixa de diálogo que exibe mensagens no jogo.

    Esta sprite é responsável por renderizar o texto do diálogo em uma caixa
    com fundo e posicioná-la de forma adequada acima do personagem que fala.

    Atributos:
        __messagem (str): A mensagem de texto a ser exibida.
        __character (Entidades): A instância do personagem (Player ou Npc) associada a este diálogo.
        __font (pygame.font.Font): A fonte utilizada para renderizar o texto.
        __z (float): A camada de profundidade da sprite para ordenação de desenho,
                    garantindo que o diálogo apareça acima de outros elementos.
        __image (pygame.Surface): A superfície visual da caixa de diálogo com o texto.
        __rect (pygame.FRect): O retângulo que define a posição e o tamanho da caixa de diálogo.
    """
    def __init__(self, messagem: str, character: 'Entidades', groups: pygame.sprite.Group, font: pygame.font.Font) -> None:
        super().__init__(groups)
        self.__messagem: str = messagem
        self.__character: 'Entidades' = character
        self.__font: pygame.font.Font = font
        self.__z: float = Config.CAMADAS_MUNDO['top']

        #texto
        text_surf: pygame.Surface = self.font.render(self.messagem, False, Config.CORES['black'])
        preenchimento: int = 5
        largura: int = max(30, text_surf.get_width() + preenchimento * 2)
        altura: int = text_surf.get_height() + preenchimento * 2

        #fundo e deixar com bordas arredondadas
        surf: pygame.Surface = pygame.Surface((largura, altura), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, Config.CORES['pure white'], surf.get_frect(topleft = (0, 0)), 0, 4)
        surf.blit(text_surf, text_surf.get_frect(center = (largura / 2, altura / 2)))

        #posicionar sprite
        self.__image: pygame.Surface = surf
        self.__rect: pygame.FRect = self.image.get_frect(midbottom = self.character.rect.midtop + vector(0, -10))

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("A camada 'z' deve ser um número (float ou int).")
        self.__z = value

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'image' deve ser uma superfície Pygame.")
        self.__image = value

    @property
    def rect(self) -> pygame.FRect:
        return self.__rect

    @rect.setter
    def rect(self, value: pygame.FRect) -> None:
        if not isinstance(value, pygame.FRect):
            raise TypeError("O 'rect' deve ser um pygame.FRect.")
        self.__rect = value

    @property
    def messagem(self) -> str:
        return self.__messagem

    @messagem.setter
    def messagem(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("A 'messagem' deve ser uma string.")
        self.__messagem = value
        
    @property
    def character(self) -> 'Entidades':
        return self.__character
    
    @character.setter
    def character(self, value: 'Entidades') -> None:
        if not hasattr(value, 'rect'):
            raise ValueError("O 'character' deve ser uma instância de Entidades ou similar.")
        self.__character = value

    @property
    def font(self) -> pygame.font.Font:
        return self.__font
    
    @font.setter
    def font(self, value: pygame.font.Font) -> None:
        if not isinstance(value, pygame.font.Font):
            raise TypeError("A 'font' deve ser uma instância de pygame.font.Font.")
        self.__font = value
