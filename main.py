from configuracoes import *
from pytmx.util_pygame import load_pygame
from os.path import join

class Jogo:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((janela_largura, janela_altura))
        pygame.display.set_caption('Profmoon: Crônicas Acadêmicas')

        self.importar_assets()

    def importar_assets(self):
        self.tmx_mapa = {'mundo': load_pygame(join('mundo.tmx'))}
        print(self.tmx_mapa)

    def corre(self):
        while True:
            #evento loop para fechar o jogo, caso a interacao seja no x
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #logica jogo
            pygame.display.update()

if __name__ == '__main__':
    jogo = Jogo()
    jogo.corre()