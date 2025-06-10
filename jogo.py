import pygame
from config import Config
from jogador import Jogador
from sys import exit

class Jogo:
    def __init__(self):
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")
        print("Se não funcionar, é culpa do professor, não minha.")
        pygame.init()

        self.config = Config()

        self.superficieExib = pygame.display.set_mode((self.config.larguraJanela, self.config.alturaJanela))

        pygame.display.set_caption('Profmoon: Crônicas Acadêmicas')

        print(f"Janela criada: {self.config.larguraJanela}x{self.config.alturaJanela} pixels.")

        posicaoInicialX = self.config.larguraJanela // 2 - self.config.tamSpritePad // 2
        posicaoInicialY = self.config.alturaJanela // 2 - self.config.tamSpritePad // 2
        print(f"Posição inicial do jogador: ({posicaoInicialX}, {posicaoInicialY})")

        self.jogador = Jogador((posicaoInicialX, posicaoInicialY), self.config.tamSpritePad)

        self.todosSprites = pygame.sprite.Group(self.jogador)
        self.rodando = True
        print("Jogo: Instância Jogo criada.")

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