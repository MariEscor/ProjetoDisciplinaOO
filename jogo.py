""" import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join

from config import Config
from sprite import Sprite
from allsprites import AllSprites
from entidade import Player

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
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(") """


# jogo.py
import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from os.path import join
from typing import Any

from config import Config
from allsprites import AllSprites
from player import Player

# --- NOVA CLASSE: TileSprite (temporária, para elementos de mapa fixos) ---
class TileSprite(pygame.sprite.Sprite):
    def __init__(self, posicao: tuple, superficie: pygame.Surface, grupos: pygame.sprite.Group) -> None:
        super().__init__(grupos)
        self.__image = superficie
        self.__rect = self.__image.get_rect(topleft=posicao)

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("Image deve ser uma instância de pygame.Surface.")
        self.__image = value

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @rect.setter
    def rect(self, value: pygame.Rect) -> None:
        if not isinstance(value, pygame.Rect):
            raise TypeError("Rect deve ser uma instância de pygame.Rect.")
        self.__rect = value

    def update(self, dt: float) -> None:
        pass

        
# --- FIM da NOVA CLASSE: TileSprite ---


class Jogo:
    def __init__(self) -> None:
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")
        print("Se não funcionar, é culpa do professor, não minha.")
        pygame.init()

        # Encapsulamento de atributos
        self.__config: Config = Config()
        self.__superficie_exibicao: pygame.Surface = pygame.display.set_mode((self.__config.largura_janela, self.__config.altura_janela))
        
        # CORREÇÃO AQUI: Inicializar __player com uma instância Jogador temporária
        # Isso garante que self.__player sempre exista e tenha um .rect
        # Mesmo se o mapa TMX não contiver o objeto 'Player' com 'pos' == 'world'.
        quadro_temp = pygame.Surface((self.__config.tam_sprite_padrao, self.__config.tam_sprite_padrao))
        quadro_temp.fill('gray') # Quadrado cinza temporário
        quadros_temp = {
            'direita_parado': [quadro_temp], 'esquerda_parado': [quadro_temp],
            'cima_parado': [quadro_temp], 'baixo_parado': [quadro_temp],
            'direita_andando': [quadro_temp], 'esquerda_andando': [quadro_temp],
            'cima_andando': [quadro_temp], 'baixo_andando': [quadro_temp],
        }
        self.__player: Player = Player(
            (0, 0), # Posição inicial temporária
            quadros_temp,
            'parado', 'baixo',
            1.0, # Velocidade de animação mínima
            0.0 # Velocidade de movimento zero para não mover se for o temporário
        )
        
        self.__todos_sprites: AllSprites = AllSprites(self.__config) 
        self.__rodando: bool = True
        self.__mapa_tmx = {}

        # Relógio para controlar o FPS
        self.__clock: pygame.time.Clock = pygame.time.Clock()
        
        pygame.display.set_caption('Profmoon: Crônicas Acadêmicas')

        print(f"Janela criada: {self.__config.largura_janela}x{self.__config.altura_janela} pixels.")

        # --- Carregamento de assets e configuração do mapa ---
        self.__importar_assets()
        # Após importar, o setup pode sobrescrever self.__player se encontrar um no mapa
        self.__setup(self.__mapa_tmx['hospital'], 'world') 
        
        print("Jogo: Instância Jogo criada.")
        
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
    def player(self) -> Player:
        return self.__player
    
    @player.setter
    def player(self, value: Player) -> None:
        if isinstance(value, Player):
            self.__player = value
        else:
            raise TypeError("Jogador deve ser uma instância da classe Jogador.")
        
    @property
    def todos_sprites(self) -> AllSprites:
        return self.__todos_sprites
    
    @todos_sprites.setter
    def todos_sprites(self, value: AllSprites) -> None:
        if isinstance(value, AllSprites):
            self.__todos_sprites = value
        else:
            raise TypeError("Todos sprites deve ser uma instância de AllSprites.")
        
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
        
    def __importar_assets(self) -> None:
        """
        Importa todos os assets do jogo, como mapas TMX, frames de animação, etc.
        Carrega os mapas do Tiled (.tmx) de 'assets/maps'.
        """
        try:
            # CORREÇÃO CRÍTICA DO CAMINHO DO TMX
            # Agora referencia assets/mundo/mundo.tmx e assets/mundo/hospital.tmx
            self.__mapa_tmx['mundo'] = load_pygame(join('assets', 'mundo', 'mundo.tmx'))
            self.__mapa_tmx['hospital'] = load_pygame(join('assets', 'mundo', 'hospital.tmx')) # Assumindo que hospital.tmx também estará lá
            print("Mapas TMX carregados com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar mapa TMX: {e}")
            print("Verifique se seus arquivos .tmx estão no diretório 'assets/mundo' e se a estrutura interna de pastas dos assets (graphics, tilesets) está correta.")
            pygame.quit()
            exit()
        
    def __setup(self, tmx_map: Any, jogador_posicao_inicio: str) -> None:
        """
        Configura o cenário do jogo com base em um mapa TMX e posiciona o jogador.
        Similar ao 'setup' do Monster Hunter.
        :param tmx_map: O objeto de mapa TMX carregado.
        :param jogador_posicao_inicio: A string da propriedade 'pos' do jogador no TMX.
        """
        self.__todos_sprites.empty() # Limpa o grupo de sprites para o novo mapa

        # --- Camada de Terreno (ex: Terrain) ---
        for x, y, superficie in tmx_map.get_layer_by_name('Terreno').tiles():
            TileSprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), superficie, self.__todos_sprites)
        
        # --- Camada de Objetos (ex: Objects) ---
        for objeto in tmx_map.get_layer_by_name('Objetos'):
            TileSprite((objeto.x, objeto.y), objeto.image, self.__todos_sprites)

        # --- Camada de Entidades (para posicionar o Jogador) ---
        # ATENÇÃO: Os TMX do Monster Hunter têm objetos 'Player' com propriedades específicas.
        # Por exemplo, em 'mundo.tmx' (world.tmx), há um 'Player' com pos='house'.
        # Se 'jogador_posicao_inicio' for 'world', ele procurará por isso.
        
        jogador_encontrado_no_mapa = False
        for objeto in tmx_map.get_layer_by_name('Entidades'):
            # Verifica se o objeto é o 'Player' e se sua propriedade 'pos'
            # corresponde à posição de início desejada.
            if objeto.name == 'Player' and objeto.properties['pos'] == jogador_posicao_inicio:
                jogador_encontrado_no_mapa = True
                
                quadro_jogador = pygame.Surface((self.__config.tam_sprite_padrao, self.__config.tam_sprite_padrao))
                quadro_jogador.fill('red') # Cor para o jogador no mapa
                quadros_jogador_mapa = {
                    'direita_parado': [quadro_jogador],
                    'esquerda_parado': [pygame.transform.flip(quadro_jogador, True, False)],
                    'cima_parado': [quadro_jogador],
                    'baixo_parado': [quadro_jogador],
                    'direita_andando': [quadro_jogador], 
                    'esquerda_andando': [pygame.transform.flip(quadro_jogador, True, False)],
                    'cima_andando': [quadro_jogador],
                    'baixo_andando': [quadro_jogador],
                }

                self.__player = Player(
                    (objeto.x, objeto.y), # Posição inicial do mapa TMX
                    quadros_jogador_mapa, 
                    objeto.properties.get('estado_inicial', 'parado'), # Pega do TMX ou usa padrão
                    objeto.properties.get('direcao_inicial', 'baixo'), # Pega do TMX ou usa padrão
                    6.0, # Velocidade da animação
                    250.0 # Velocidade de movimento
                )
                break # Encontrou o jogador, pode parar o loop

        if not jogador_encontrado_no_mapa:
            print(f"Aviso: Objeto 'Player' com pos='{jogador_posicao_inicio}' não encontrado no mapa TMX. Usando jogador temporário.")
            # O self.__player já foi inicializado no __init__ como temporário
            # Apenas adicione-o ao grupo de sprites se não foi adicionado pelo mapa
            self.__todos_sprites.add(self.__player)
        else:
            # Se o jogador foi encontrado e instanciado, adicione-o ao grupo de sprites
            self.__todos_sprites.add(self.__player)


    def executar(self) -> None:
        """
        Inicia e mantém o loop principal do jogo.
        """
        while self.__rodando:
            dt: float = self.__clock.tick() / 1000.0

            self.__processar_eventos()
            self.__atualizar_estado(dt) 
            self.__renderizar()

        print("Fechando o jogo...")
        pygame.quit()
        exit()

    def __processar_eventos(self) -> None:
        """
        Processa todos os eventos da fila do Pygame.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.__rodando = False

    def __atualizar_estado(self, dt: float) -> None:
        """
        Atualiza o estado de todos os elementos do jogo (movimento, colisões, etc.).
        Passa dt para os sprites.
        :param dt: Delta time (tempo decorrido desde o último frame).
        """
        self.__todos_sprites.update(dt)

    def __renderizar(self) -> None:
        """
        Desenha todos os elementos na tela.
        """
        self.__superficie_exibicao.fill((0, 0, 0)) # Preenche a tela de preto como base
        
        self.__todos_sprites.draw(self.__player.rect.center) 
        
        pygame.display.update()

    def __del__(self) -> None:
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(")