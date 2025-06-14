#2025-06-13 02h09
import pygame
from pygame.math import Vector2 as vector
from config import Config
from player import Player

class AllSprites(pygame.sprite.Group):
    def __init__(self, config: Config, player: Player) -> None:
        super().__init__()
        self.__config = config
        self.__player = player
        self.__display_surface = pygame.display.get_surface()
        self.__offset = vector(100, 20)

    @property
    def config(self) -> Config:
        return self.__config
    
    @config.setter
    def config(self, value: Config) -> None:
        if not isinstance(value, Config):
            raise TypeError("Config tem que vir da classe Config")
        self.__config = value

    @property
    def player(self) -> Player:
        return self.__player
    
    @player.setter
    def player(self, value: Player) -> None:
        if not isinstance(value, Player):
            raise TypeError("Player tem que ser uma instância da classe Player.")
        self.__player = value


    @property
    def display_surface(self) -> pygame.Surface:
        return self.__display_surface
    
    @display_surface.setter
    def display_surface(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("display_surface tem que ser uma Surface do Pygame")
        self.__display_surface = value

    @property
    def offset(self) -> vector:
        return self.__offset
    
    @offset.setter
    def offset(self, value: vector) -> None:
        if not isinstance(value, vector):
            raise TypeError("offset tem que ser um objeto do tipo vector")
        self.__offset = value

    def draw(self) -> None:
        self.__offset.x = -(self.__player.rect.center[0] - self.__config.largura_janela / 2)
        self.__offset.y = -(self.__player.rect.center[1] - self.__config.altura_janela / 2)
        
        for sprite in self.sprites():
            self.__display_surface.blit(sprite.image, sprite.rect.topleft + self.__offset)

    def __del__(self) -> None:
        print("Criei isso aqui 2h49 da madrugada, to sem criatividade pro del de AllSprites. Imagina algo dramatico.")