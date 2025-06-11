#25-06-11 04h39 ok
import pygame
from config import Config
from jogador import Jogador
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

class Jogo:
    def __init__(self) -> None:
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")
        print("Se não funcionar, é culpa do professor, não minha.")
        pygame.init()

        #encapsulamento
        self.__config = Config()
        self.__superficie_exibicao = pygame.display.set_mode((self.__config.largura_janela, self.__config.altura_janela))
        self.__jogador = None
        self.__todos_sprites = None
        self.__rodando = True
        self.__mapa_tmx = {}

        pygame.display.set_caption('Profmoon: Crônicas Acadêmicas')

        print(f"Janela criada: {self.__config.largura_janela}x{self.__config.altura_janela} pixels.")

        posicao_inicial_x = self.__config.largura_janela // 2 - self.__config.tam_sprite_padrao // 2
        posicao_inicial_y = self.__config.altura_janela // 2 - self.__config.tam_sprite_padrao // 2
        print(f"Posição inicial do jogador: ({posicao_inicial_x}, {posicao_inicial_y})")

        self.__jogador = Jogador((posicao_inicial_x, posicao_inicial_y), self.__config.tam_sprite_padrao)
        self.__todos_sprites = pygame.sprite.Group(self.__jogador)

        print("Jogo: Instância Jogo criada.")
        
        self.__importar_assets()
        
    @property
    def config(self) -> Config:
        return self.__config
    
    @config.setter
    def config(self, value: Config) -> None:
        if isinstance(value, Config):
            self.__config = value
        else:
            raise TypeError("Config deve ser uma instância da classe Config.")

    @property
    def superficie_exibicao(self) -> pygame.Surface:
        return self.__superficie_exibicao
    
    @superficie_exibicao.setter
    def superficie_exibicao(self, value: pygame.Surface) -> None:
        if isinstance(value, pygame.Surface):
            self.__superficie_exibicao = value
        else:
            raise TypeError("Superfície de exibição deve ser uma instância de pygame.Surface.")
        
    @property
    def jogador(self) -> Jogador:
        return self.__jogador
    
    @jogador.setter
    def jogador(self, value: Jogador) -> None:
        if isinstance(value, Jogador):
            self.__jogador = value
        else:
            raise TypeError("Jogador deve ser uma instância da classe Jogador.")
        
    @property
    def todos_sprites(self) -> pygame.sprite.Group:
        return self.__todos_sprites
    
    @todos_sprites.setter
    def todos_sprites(self, value: pygame.sprite.Group) -> None:
        if isinstance(value, pygame.sprite.Group):
            self.__todos_sprites = value
        else:
            raise TypeError("Todos sprites deve ser uma instância de pygame.sprite.Group.")
        
    @property
    def rodando(self) -> bool:
        return self.__rodando
    
    @rodando.setter
    def rodando(self, value: bool) -> None:
        if isinstance(value, bool):
            self.__rodando = value
        else:
            raise TypeError("Rodando deve ser um valor booleano.")
        
    @property
    def mapa_tmx(self) -> dict:
        return self.__mapa_tmx
    
    @mapa_tmx.setter
    def mapa_tmx(self, value: dict) -> None:
        if isinstance(value, dict):
            self.__mapa_tmx = value
        else:
            raise TypeError("Mapa TMX deve ser um dicionário.")
        
    

    """ 
    def importar_assets(self):
        self.tmx_mapa = {'mundo': load_pygame(join('mundo.tmx'))}
        print(self.tmx_mapa) 
        
        def __importar_assets(self) -> None:
                
        try:            
            self.__mapa_tmx['mundo'] = load_pygame(join('assets', 'maps', 'mundo.tmx'))
            print("Mapa 'mundo.tmx' carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar mapa TMX: {e}")
            print("Verifique se 'mundo.tmx' está em 'assets/maps'.")
            pygame.quit()
            exit()

        """
        
    def executar(self) -> None:
        while self.__rodando:
            self.__processar_eventos()
            self.__atualizar_estado()
            self.__renderizar()

        print("Fechando o jogo...")
        pygame.quit()
        exit()

    def __processar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.__rodando = False
            
    def __atualizar_estado(self) -> None:
        self.__todos_sprites.update()

    def __renderizar(self) -> None:
        self.__superficie_exibicao.fill((0, 0, 0))
        self.__todos_sprites.draw(self.__superficie_exibicao)
        pygame.display.update()

    def __del__(self) :
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(")