import pygame

class Animacao(pygame.sprite.Sprite):
    def __init__(self, posicao: tuple, quadros: dict, estado_inicial: str, direcao_inicial: str, velocidade_animacao: float):
        super().__init__()
        self.__quadros = quadros
        self.__indice_quadro = 0.0        
        self.__estado = estado_inicial
        self.__direcao = direcao_inicial
        self.__velocidade_animacao = velocidade_animacao

        self.image = self.__quadros[f'{self.__direcao}_{self.__estado}'][int(self.__indice_quadro)]
        self.rect = self.image.get_rect(topleft=posicao)

        print("Instância de Animacao ta ok(eu acho)")

    @property
    def quadros(self) -> dict:
        return self.__quadros