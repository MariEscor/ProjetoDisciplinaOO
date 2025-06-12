#2025-06-12 01h03 ok
import pygame
from pygame.math import Vector2 as vector
from animacao import Animacao

class Entidade(Animacao):
    def __init__(self, posicao: tuple, quadros: dict, estado_inicial: str, direcao_inicial: str, velocidade_animacao: float, velocidade_movimento: float) -> None:
        super().__init__(posicao, quadros, estado_inicial, direcao_inicial, velocidade_animacao)
        self.__velocidade_movimento = velocidade_movimento
        self.__direcao_movimento = vector()

        print("Entidade criada")

    @property
    def velocidade_movimento(self) -> float:
        return self.__velocidade_movimento

    @velocidade_movimento.setter
    def velocidade_movimento(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Velocidade de movimento deve ser um número positivo.")
        self.__velocidade_movimento = value

    @property
    def direcao_movimento(self) -> vector:
        return self.__direcao_movimento

    @direcao_movimento.setter
    def direcao_movimento(self, value: vector) -> None:
        self.__direcao_movimento = value

    def mover(self, dt: float) -> None:
        if self.__direcao_movimento.length() > 0:
            direcao_normalizada = self.__direcao_movimento.normalize() 
            deslocamento = direcao_normalizada * self.__velocidade_movimento * dt
            self.rect.center += deslocamento

    def update(self, dt: float) -> None:
        super().update(dt)
        self.mover(dt)

    def __del__(self) -> None:
        print("Será que foi a entidade foi destruída?")