# jogo.py
import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from typing import Any
from config import Config
from allsprites import AllSprites
from player import Player
from tilesprite import TileSprite
from utils import Utils
from sprite import Sprite, AnimatedSprite

class Jogo:
    def __init__(self) -> None:
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")

        pygame.init()

        self.__config: Config = Config()
        self.__superficie_exibicao: pygame.Surface = pygame.display.set_mode((self.__config.largura_janela, self.__config.altura_janela))
        
        quadro_player_inicial = pygame.Surface((self.__config.tam_sprite_padrao, self.__config.tam_sprite_padrao))
        quadro_player_inicial.fill(Config.CORES['red']) 
        
        quadros_player_mapa = {
            'direita_parado': [quadro_player_inicial], 
            'esquerda_parado': [pygame.transform.flip(quadro_player_inicial, True, False)],
            'cima_parado': [quadro_player_inicial], 
            'baixo_parado': [quadro_player_inicial],
            'direita_andando': [quadro_player_inicial], 
            'esquerda_andando': [pygame.transform.flip(quadro_player_inicial, True, False)],
            'cima_andando': [quadro_player_inicial], 
            'baixo_andando': [quadro_player_inicial],
        }

        self.__player: Player = Player(
            (self.__config.largura_janela // 2 - self.__config.tam_sprite_padrao // 2, 
             self.__config.altura_janela // 2 - self.__config.tam_sprite_padrao // 2), 
            quadros_player_mapa, 
            'parado', 'baixo',
            6.0, 
            250.0 
        )
        
        self.__all_sprites: AllSprites = AllSprites(self.__config, self.__player) 
        self.__all_sprites.add(self.__player)

        self.__rodando: bool = True
        self.__mapa_tmx = {}

        self.__clock: pygame.time.Clock = pygame.time.Clock()
        pygame.display.set_caption("Profmoon: Crônicas Acadêmicas")

        print(f"Janela criada: {self.__config.largura_janela}x{self.__config.altura_janela} pixels.")
        self.__importar_assets()
        self.__setup(self.__mapa_tmx['mundo'], 'fogo')

        print("O JOGO") 

    def __importar_assets(self) -> None:
        self.__mapa_tmx = {
            'mundo': load_pygame('mundo/mundo.tmx'),
            'hospital': load_pygame('maps/hospital.tmx')
            }
        self.overwolrd_frames = {
            'water': Utils.importar_pasta('..', 'graphics', 'tilesets', 'water'),
            'coast': Utils.coast_importar(24, 12, '..', 'graphics', 'tilesets', 'coast')
        }

    def __setup(self, tmx_map, jogador_posicao_inicio) -> None:
        # Terreno
        for x, y, superficie in tmx_map.get_layer_by_name('Terrain').tiles():
            TileSprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), superficie, self.__all_sprites)
        
        # Objetos
        for objeto in tmx_map.get_layer_by_name('Objetos'):
            TileSprite((objeto.x, objeto.y), objeto.image, self.__all_sprites)

        # Entidades
        for objeto in tmx_map.get_layer_by_name('Entidades'):
            if objeto.name == 'Player' and objeto.properties['pos'] == jogador_posicao_inicio:
                self.__player.rect.topleft = (objeto.x, objeto.y)

        # Água
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), self.__config.tam_sprite_padrao):
                for y in range(int(obj.y), int(obj.y + obj.height), self.__config.tam_sprite_padrao):
                    AnimatedSprite((x,y), self.overwolrd_frames['water'], self.__all_sprites)

        # Costa
        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overwolrd_frames['coast'][terrain][side], self.__all_sprites)

    def executar(self) -> None:
        while self.__rodando:
            dt = self.__clock.tick() / 1000.0
            self.__processar_eventos()
            self.__atualizar_estado(dt)
            self.__renderizar()
        
        print("O jogo acabou :|") 
        pygame.quit()
        exit()

    def __processar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.__rodando = False

    def __atualizar_estado(self, dt: float) -> None:
        self.__all_sprites.update(dt)

    def __renderizar(self) -> None:
        self.__superficie_exibicao.fill(Config.CORES['black']) 
        self.__all_sprites.draw() 
        pygame.display.update()

    def __del__(self) -> None:
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(")
