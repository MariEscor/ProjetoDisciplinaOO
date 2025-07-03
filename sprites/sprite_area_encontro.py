# sprite_area_encontro.py

import pygame
from bases.config import Config
from sprites.sprite import Sprite

class SpriteAreaEncontro(Sprite):
    """
    Representa uma área no mapa que pode ativar as batalhas contra pokemons.

    Esta classe é usada para demarcar regiões onde batalhas com pokemons, 
    como por exemplo os arbustos, ou zonas de areia, podem ser iniciadas ao 
    colidir com o jogador. Também ajusta a camada de renderização para 
    corrigir a profundidade visual do player em relação a esses elementos de 
    terreno.

    Atributos:
        __biome (str): O tipo de bioma associado a esta área (e.g., 'forest', 
        'sand', 'ice').
                        
    """
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups: pygame.sprite.Sprite, biome: str) -> None:
        self.__biome: str = biome
        z_layer: float = Config.CAMADAS_MUNDO['main' if biome != 'sand' else 'bg']
        super().__init__(pos, surf, groups, z_layer)
        self.y_sort -= 40

    @property
    def biome(self) -> str:
        return self.__biome

    @biome.setter
    def biome(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("O 'biome' deve ser uma string.")
        self.__biome = value  
