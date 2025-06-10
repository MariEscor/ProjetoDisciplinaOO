""" import pygame
from pygame.math import Vector2 as vector
from sys import exit

larguraJanela, alturaJanela = 1280, 720
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
    def __init__(self, larguraJanela=1280, alturaJanela=720, tamSpritePad=64):
        self.__larguraJanela = larguraJanela
        self.__alturaJanela = alturaJanela
        self.__tamSpritePad = tamSpritePad

    @property
    def larguraJanela(self):
        return self.__larguraJanela

    @larguraJanela.setter
    def larguraJanela(self, value):
        self.__larguraJanela = value

    @property
    def alturaJanela(self):
        return self.__alturaJanela

    @alturaJanela.setter
    def alturaJanela(self, value):
        self.__alturaJanela = value

    @property
    def tamSpritePad(self):
        return self.__tamSpritePad
    
    @tamSpritePad.setter
    def tamSpritePad(self, value):
        self.__tamSpritePad = value

    def __del__(self):
        print("poh deu moh trabalho fazer essa classe Config e você a matou >:(")

    

