from config import Config
import pygame
from pygame.math import Vector2 as vector

class Player(pygame.sprite.Sprite):
    def __init__(self, posicao, groups, tamanho=100):
        super().__init__(groups)
        self.image = pygame.Surface((tamanho, tamanho))  # usar o tamanho passado
        self.image.fill('red')
        self.rect = self.image.get_rect(center=posicao)  # corrigido: get_rect e center em inglês

        self.direcao = vector()

    def input(self):
        chaves = pygame.key.get_pressed()
        input_vector = vector()
        if chaves[pygame.K_UP]:
            input_vector.y -= 1
        if chaves[pygame.K_DOWN]:
            input_vector.y += 1
        if chaves[pygame.K_LEFT]:
            input_vector.x -= 1
        if chaves[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direcao = input_vector

    def mover(self, diferenca_tempo):
        deslocamento = self.direcao * 250 * diferenca_tempo
        self.rect.center = vector(self.rect.center) + deslocamento

    def update(self, diferenca_tempo):
        self.input()
        self.mover(diferenca_tempo)
