""" import pygame
from pygame.math import Vector2 as vector
from sys import exit

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
    def __init__(self, largura_janela = 1280, altura_janela=720, tam_sprite_padrao=64):
        self.__largura_janela = largura_janela
        self.__altura_janela = altura_janela
        self.__tam_sprite_padrao = tam_sprite_padrao

    @property
    def largura_janela(self):
        return self.__largura_janela

    @largura_janela.setter
    def largura_janela(self, value):
        self.__largura_janela = value

    @property
    def altura_janela(self):
        return self.__altura_janela

    @altura_janela.setter
    def altura_janela(self, value):
        self.__altura_janela = value

    @property
    def tam_sprite_padrao(self):
        return self.__tam_sprite_padrao
    
    @tam_sprite_padrao.setter
    def tam_sprite_padrao(self, value):
        self.__tam_sprite_padrao = value

    def __del__(self):
        print("poh deu moh trabalho fazer essa classe Config e você a matou >:(") 
