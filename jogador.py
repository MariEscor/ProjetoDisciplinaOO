import pygame
from sys import exit

class Jogador(pygame.sprite.Sprite):
    def __init__(self, posicao: tuple, tamanho: int):
        super().__init__()

        self.tamSprite = tamanho

        try:
            self.playerCompleto = pygame.image.load('assets/player.png').convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem do jogador: {e}")
            print("Olhe se a imagem 'player.png' está no diretório 'assets'.")
            pygame.quit()
            exit()
        
        self.image = pygame.Surface((self.tamSprite, self.tamSprite), pygame.SRCALPHA)
        self.image.blit(self.playerCompleto, (0, 0), (0, 0, self.tamSprite, self.tamSprite))

        self.rect = self.image.get_rect(topleft=posicao)

        self.posiInicial = posicao

        print(f"Jogador criado na posição {self.posiInicial} com tamanho {self.tamSprite}.")

    def desenhar(self, superficie: pygame.Surface) -> None:

        superficie.blit(self.image, self.rect)

    def update(self) -> None:
        
        pass

    def __del__(self):
        print("CÊ MATOU O JOGADOR >:(")
