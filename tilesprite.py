#2025-06-12 18h22
import pygame

class TileSprite(pygame.sprite.Sprite):
    def __init__(self, posicao: tuple, superficie: pygame.Surface, grupos: pygame.sprite.Group) -> None:
        super().__init__(grupos)
        self.image = superficie
        self.rect = self.image.get_rect(topleft=posicao)

    @property
    def image(self) -> pygame.Surface:
        return self.__image
        
    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A imagem deve ser uma Surface do Pygame.")
        self.__image = value
        
    @property
    def rect(self) -> pygame.Rect:
        return self.__rect
    
    @rect.setter
    def rect(self, value: pygame.Rect) -> None:
        if not isinstance(value, pygame.Rect):
            raise TypeError("O Rect deve ser pygame.Rect.")
        self.__rect = value

    def update(self, dt: float) -> None:
        pass

"""     def __del__(self) -> None:
        print("JOGARAM ÁGUA NO TILESPRITE E ELE DESAPARECEU ;--;") """