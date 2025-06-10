""" import pygame
from pygame.math import Vector2 as vector
from sys import exit

janela_largura, janela_altura = 1280, 720
tile_size = 64
velocidade_animacao = 6
battle_outline_width = 4

colors = {

}

world_layers = {

}

battle_positions = {

}

battle_layers = {

}

battle_choices = {
    
} """

class Config:
    def __init__(self, janela_largura=1280, janela_altura=720):
        self.__janela_largura = janela_largura
        self.__janela_altura = janela_altura

    @property
    def janela_largura(self):
        return self.__janela_largura

    @janela_largura.setter
    def janela_largura(self, value):
        self.__janela_largura = value

    @property
    def janela_altura(self):
        return self.__janela_altura

    @janela_altura.setter
    def janela_altura(self, value):
        self.__janela_altura = value

