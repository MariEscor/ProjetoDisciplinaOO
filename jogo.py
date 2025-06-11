import pygame
from config import Config
from jogador import Jogador
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

class Jogo:
    def __init__(self):
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")
        print("Se não funcionar, é culpa do professor, não minha.")
        pygame.init()

        self.config = Config()

        self.superficieExib = pygame.display.set_mode((self.config.largura_janela, self.config.altura_janela))

        pygame.display.set_caption('Profmoon: Crônicas Acadêmicas')

        print(f"Janela criada: {self.config.largura_janela}x{self.config.altura_janela} pixels.")

        posicaoInicialX = self.config.largura_janela // 2 - self.config.tam_sprite_padrao // 2
        posicaoInicialY = self.config.altura_janela // 2 - self.config.tam_sprite_padrao // 2
        print(f"Posição inicial do jogador: ({posicaoInicialX}, {posicaoInicialY})")

        self.jogador = Jogador((posicaoInicialX, posicaoInicialY), self.config.tam_sprite_padrao)

        self.todosSprites = pygame.sprite.Group(self.jogador)
        self.rodando = True
        print("Jogo: Instância Jogo criada.")
        
        """ self.importar_assets()
    
    
    def importar_assets(self):
        self.tmx_mapa = {'mundo': load_pygame(join('mundo.tmx'))}
        print(self.tmx_mapa) """
        
        
    def executar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            self.superficieExib.fill((0, 0, 0))
            self.todosSprites.draw(self.superficieExib)
            pygame.display.update()

        print("Fechando o jogo...")
        pygame.quit()
        exit()

    def __del__(self):
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(")