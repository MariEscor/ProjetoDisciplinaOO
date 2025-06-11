import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

from config import Config
from sprite import Sprite
from allsprites import AllSprites
from entidades import Player

class Jogo:
    def __init__(self):
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")
        print("Se não funcionar, é culpa do professor, não minha.")
        pygame.init()

        self.config = Config()

        self.superficieExib = pygame.display.set_mode((self.config.larguraJanela, self.config.alturaJanela))

        pygame.display.set_caption('Profmoon: Crônicas Acadêmicas')
        self.clock = pygame.time.Clock()

        #grupos
        self.todosSprites = AllSprites(self.config)

        self.rodando = True
        
        self.importar_assets()
        self.setup(self.tmx_mapa['hospital'], 'world')
    

    def importar_assets(self):
        self.tmx_mapa = {
            'mundo': load_pygame('mundo/mundo.tmx'),
            'hospital': load_pygame('maps/hospital.tmx')
            }
        

    def setup(self, tmx_map, jogador_posicao_inicio):
        #terreno
        for x, y, superficie in tmx_map.get_layer_by_name('Terreno').tiles():
            Sprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), superficie, self.todosSprites)
        
        #objetos
        for objeto in tmx_map.get_layer_by_name('Objetos'):
            Sprite((objeto.x, objeto.y), objeto.image, self.todosSprites)

        #entidades
        for objeto in tmx_map.get_layer_by_name('Entidades'):
            if objeto.name == 'Player' and objeto.properties['pos'] == jogador_posicao_inicio:
                self.player = Player((objeto.x, objeto.y), self.todosSprites, tamanho = self.config.tamSpritePad)


    def executar(self):
        while self.rodando:
            diferenca_tempo = self.clock.tick() / 1000

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            #logica jogo
            self.superficieExib.fill('black')
            self.todosSprites.update(diferenca_tempo)
            self.todosSprites.draw(self.player.rect.center)
            pygame.display.update()

        print("Fechando o jogo...")
        pygame.quit()
        exit()

    def __del__(self):
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(")