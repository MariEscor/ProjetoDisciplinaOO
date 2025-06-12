#2025-06-12 02h26
import pygame
from sys import exit
from entidade import Entidade
from pygame.math import Vector2 as vector

class Player(Entidade):
    def __init__(self, posicao: tuple, quadros: dict, estado_inicial: str, direcao_inicial: str, velocidade_animacao: float, velocidade_movimento: float) -> None:
        super().__init__(posicao, quadros, estado_inicial, direcao_inicial, velocidade_animacao, velocidade_movimento)
        print("Cê deu a luz ao Jogador")

    def input(self) -> None:
        chaves = pygame.key.get_pressed()
        input_vector = vector()

        if chaves[pygame.K_UP]:
            input_vector.y -= 1
            self.direcao = 'cima'
        if chaves[pygame.K_DOWN]:
            input_vector.y += 1
            self.direcao = 'baixo'
        if chaves[pygame.K_LEFT]:
            input_vector.x -= 1
            self.direcao = 'esquerda'
        if chaves[pygame.K_RIGHT]:
            input_vector.x += 1
            self.direcao = 'direita'

        if input_vector.length() > 0:
            self.direcao_movimento = input_vector.normalize()  
        else:
            self.direcao_movimento = vector()

    def update(self, dt: float) -> None:
        self.input()
        super().update(dt)

    def __del__(self):
        print("CÊ MATOU O JOGADOR >:(")