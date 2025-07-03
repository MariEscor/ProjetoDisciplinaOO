# jogo.py

import pygame
import random
from pytmx.util_pygame import load_pygame
from os.path import join
from typing import Dict, List, Any, Callable, Union

from bases.config import Config
from bases.utils import Utils
from sprites.sprite import Sprite
from entidades.npc import Npc
from sprites.all_sprites import AllSprites
from entidades.player import Player
from sprites.borda_sprite import BordaSprite
from sprites.colisao_sprite import ColisaoSprite
from sprites.sprite_area_encontro import SpriteAreaEncontro
from sprites.sprite_animada import SpriteAnimada
from dialogo.arvore_de_dialogo import ArvoreDeDialogo
from sprites.sprite_transicao import SpriteTransicao
from bag_manager import BagManager
from battle_scene import BattleScene, run_battle
from bag_window import BagWindow
from pokemon import Pokemon
from scene_manager import SceneManager
from pause_menu import PauseMenu
from api_client import APIClient
from pokemon import Pokemon
from functools import partial
from pokemon_encounter import gerar_pokemon_encontro
from battle_context import set_player_team
from bases.player_state import player_state
from battle_context import player_team


from bases.game_data import *

class Jogo:
    """
    Classe principal do jogo Profmoon: Crônicas Acadêmicas.

    Gerencia o loop principal do jogo, inicialização do Pygame,
    carregamento de assets, configuração de mapas e entidades,
    interações de diálogo e transições de tela.

    Atributos:
        __config (Config): Instância da classe de configurações do jogo.
        __tela_exibicao (pygame.Surface): A superfície principal da tela do jogo.
        __clock (pygame.time.Clock): Objeto para controlar o framerate do jogo.
        __all_sprites (AllSprites): Grupo de sprites que gerencia a renderização de todos os elementos visuais.
        __player (Player): Instância do personagem jogável.
        __colisao_sprites (pygame.sprite.Group): Grupo de sprites para detecção de colisões.
        __npc_sprites (pygame.sprite.Group): Grupo de sprites para personagens não jogáveis.
        __transicao_sprites (pygame.sprite.Group): Grupo de sprites para áreas de transição de mapa.
        __transition_target (Union[tuple[str, str], None]): O alvo da transição (próximo mapa, batalha, etc.).
        __tint_surf (pygame.Surface): Superfície usada para efeitos de transição de tela (tint).
        __tint_mode (str): Modo do efeito de tint ('tint' para escurecer, 'untint' para clarear).
        __tint_progress (int): Progresso atual do efeito de tint (0-255).
        __tint_direction (int): Direção do progresso do tint (-1 para clarear, 1 para escurecer).
        __tint_speed (int): Velocidade do efeito de tint.
        __tmx_mapa (Dict[str, Any]): Dicionário de mapas TMX carregados.
        __mapa_frames (Dict[str, Any]): Dicionário de frames de animação de elementos do mapa.
        __fonts (Dict[str, pygame.font.Font]): Dicionário de fontes carregadas.
        __arvore_dialogo (Union[ArvoreDeDialogo, None]): Instância da árvore de diálogo ativa.
    """
    
    def __init__(self, start_scene: str = "mundo_aberto") -> None:
        print("Inicializando a obra de arte que merece tomar nota total do projeto...")
        pygame.init()
        pygame.display.set_caption("Profmoon: Crônicas Acadêmicas")
        self.__config: Config = Config() 
        self.__bag_manager: BagManager = BagManager()
        self.__scene_manager: SceneManager = SceneManager()
        self.__api_client: APIClient = APIClient()

        self.__tela_exibicao: pygame.Surface = pygame.display.set_mode((self.config.largura_tela, self.config.altura_tela))
        self.__clock: pygame.time.Clock = pygame.time.Clock()
        
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/overworld.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1) # Toca em loop infinito
        
        self.som_encontro = pygame.mixer.Sound("assets/sounds/notice.wav")
        self.som_encontro.set_volume(0.5)  # Ajuste o volume se quiser


        self.__all_sprites: AllSprites = AllSprites(self.config)
        self.__player: Union[Player, None] = None
        self.__colisao_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.__npc_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.__transicao_sprites: pygame.sprite.Group = pygame.sprite.Group()
        
        self.__areas_encontro: list[SpriteAreaEncontro] = []
        self.__pode_iniciar_batalha: bool = True
        self.pause_menu = PauseMenu(self)
        # Transição / tint (animaçãozinha de tela preta e PAH lugar novo)
        self.__transition_target: Union[tuple[str, str], None] = None
        self.__tint_surf: pygame.Surface = pygame.Surface((self.config.largura_tela, self.config.altura_tela))
        self.__tint_mode: str = 'untint'
        self.__tint_progress: Union[int, float] = 0.0
        self.__tint_direction: int = -1 
        self.__tint_speed: int = 600
        

        self.__tmx_mapa: Dict[str, Any] = {}
        self.__mapa_frames: Dict[str, Any] = {}
        self.__fonts: Dict[str, pygame.font.Font] = {}

        self.importar_assets()
        if start_scene == "hospital":
            self.setup(self.tmx_mapa['hospital'], 'mundo')
        elif start_scene == "mundo_aberto":
            self.setup(self.tmx_mapa['mundo'], 'fogo')

        self.__arvore_dialogo: Union[ArvoreDeDialogo, None] = None
        
        self.bag_window = BagWindow()
        self.mostrar_bag = False
        

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, value: Config) -> None:
        if not isinstance(value, Config):
            raise TypeError("O 'config' deve ser uma instância da classe Config.")
        self.__config = value

    @property
    def tela_exibicao(self) -> pygame.Surface:
        return self.__tela_exibicao

    @tela_exibicao.setter
    def tela_exibicao(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'tela_exibicao' deve ser uma instância de pygame.Surface.")
        self.__tela_exibicao = value

    @property
    def clock(self) -> pygame.time.Clock:
        return self.__clock

    @clock.setter
    def clock(self, value: pygame.time.Clock) -> None:
        if not isinstance(value, pygame.time.Clock):
            raise TypeError("O 'clock' deve ser uma instância de pygame.time.Clock.")
        self.__clock = value

    @property
    def all_sprites(self) -> AllSprites:
        return self.__all_sprites

    @all_sprites.setter
    def all_sprites(self, value: AllSprites) -> None:
        if not isinstance(value, AllSprites):
            raise TypeError("O 'all_sprites' deve ser uma instância da classe AllSprites.")
        self.__all_sprites = value

    @property
    def player(self) -> Union[Player, None]:
        return self.__player

    @player.setter
    def player(self, value: Union[Player, None]) -> None: # Anotação atualizada
        if value is not None and not isinstance(value, Player):
            raise TypeError("O 'player' deve ser uma instância da classe Player ou None.")
        self.__player = value

    @property
    def colisao_sprites(self) -> pygame.sprite.Group:
        return self.__colisao_sprites

    @colisao_sprites.setter
    def colisao_sprites(self, value: pygame.sprite.Group) -> None:
        if not isinstance(value, pygame.sprite.Group):
            raise TypeError("O 'colisao_sprites' deve ser um grupo de sprites Pygame.")
        self.__colisao_sprites = value

    @property
    def npc_sprites(self) -> pygame.sprite.Group:
        return self.__npc_sprites

    @npc_sprites.setter
    def npc_sprites(self, value: pygame.sprite.Group) -> None:
        if not isinstance(value, pygame.sprite.Group):
            raise TypeError("O 'npc_sprites' deve ser um grupo de sprites Pygame.")
        self.__npc_sprites = value

    @property
    def transicao_sprites(self) -> pygame.sprite.Group:
        return self.__transicao_sprites

    @transicao_sprites.setter
    def transicao_sprites(self, value: pygame.sprite.Group) -> None:
        if not isinstance(value, pygame.sprite.Group):
            raise TypeError("O 'transicao_sprites' deve ser um grupo de sprites Pygame.")
        self.__transicao_sprites = value

    @property
    def transition_target(self) -> Union[tuple[str, str], None]:
        return self.__transition_target

    @transition_target.setter
    def transition_target(self, value: Union[tuple[str, str], None]) -> None: 
        if value is not None and (not isinstance(value, tuple) or len(value) != 2 or not all(isinstance(s, str) for s in value)):
            raise TypeError("O 'transition_target' deve ser uma tupla de (str, str) ou None.")
        self.__transition_target = value

    @property
    def tint_surf(self) -> pygame.Surface:
        return self.__tint_surf

    @tint_surf.setter
    def tint_surf(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'tint_surf' deve ser uma instância de pygame.Surface.")
        self.__tint_surf = value

    @property
    def tint_mode(self) -> str:
        return self.__tint_mode

    @tint_mode.setter
    def tint_mode(self, value: str) -> None:
        if not isinstance(value, str): 
            raise ValueError("O 'tint_mode' deve ser 'tint', 'untint' ou 'idle'.")
        self.__tint_mode = value

    @property
    def tint_progress(self) -> Union[int, float]:
        return self.__tint_progress

    @tint_progress.setter
    def tint_progress(self, value: Union[int, float]) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("O 'tint_progress' deve ser um número (int ou float).")
        self.__tint_progress = float(value)

    @property
    def tint_direction(self) -> int:
        return self.__tint_direction

    @tint_direction.setter
    def tint_direction(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("O 'tint_direction' deve ser -1 ou 1.")
        self.__tint_direction = value

    @property
    def tint_speed(self) -> int:
        return self.__tint_speed

    @tint_speed.setter
    def tint_speed(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("A 'tint_speed' deve ser um inteiro positivo.")
        self.__tint_speed = value

    @property
    def tmx_mapa(self) -> Dict[str, Any]:
        return self.__tmx_mapa

    @tmx_mapa.setter
    def tmx_mapa(self, value: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("O 'tmx_mapa' deve ser um dicionário.")
        self.__tmx_mapa = value

    @property
    def mapa_frames(self) -> Dict[str, Any]:
        return self.__mapa_frames

    @mapa_frames.setter
    def mapa_frames(self, value: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("O 'mapa_frames' deve ser um dicionário.")
        self.__mapa_frames = value

    @property
    def fonts(self) -> Dict[str, pygame.font.Font]:
        return self.__fonts

    @fonts.setter
    def fonts(self, value: Dict[str, pygame.font.Font]) -> None:
        if not isinstance(value, dict) or not all(isinstance(f, pygame.font.Font) for f in value.values()):
            raise TypeError("As 'fonts' devem ser um dicionário onde os valores são instâncias de pygame.font.Font.")
        self.__fonts = value

    @property
    def arvore_dialogo(self) -> Union[ArvoreDeDialogo, None]:
        return self.__arvore_dialogo

    @arvore_dialogo.setter
    def arvore_dialogo(self, value: Union[ArvoreDeDialogo, None]) -> None:
        if value is not None and not isinstance(value, ArvoreDeDialogo):
            raise TypeError("A 'arvore_dialogo' deve ser uma instância da classe ArvoreDeDialogo ou None.")
        self.__arvore_dialogo = value

    def importar_assets(self):
        self.tmx_mapa = Utils.importar_tmx('assets', 'maps')

        self.mapa_frames = {

            'water': Utils.importar_pasta('assets', 'graphics', 'tilesets', 'water'),
            'coast': Utils.importar_coast(24, 12, 'assets', 'graphics', 'tilesets', 'coast'),
            'characters': Utils.importar_todos_personagens('assets', 'graphics', 'characters')

        }

        self.fonts = {

            #usa essa fonte quando tiver um dialog
            'dialog': pygame.font.Font(join('assets', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30)

        }

    def iniciar_batalha_com_npc(self, npc):
        self.cria_dialogo(npc)
        
    def setup(self, tmx_mapa: any, player_ini_pos: str) -> None:
        #RESETA O MAPA ATUAL PARA CARREGAR OUTRO
        for group in [self.all_sprites, self.colisao_sprites, self.npc_sprites, self.transicao_sprites]:
            group.empty()

        #desenha o mapa
        #terreno
        for layer in ['Terrain', 'Terrain Top']:
            for x,y, surf in tmx_mapa.get_layer_by_name(layer).tiles():
                #gambi -> tmx_mapa.tilewidth, y * tmx_mapa.tileheight em vez de self.config.tam_sprite_padrao, y * self.config.tam_sprite_padrao
                Sprite(
                    (x * tmx_mapa.tilewidth, y * tmx_mapa.tileheight), 
                    surf, self.__all_sprites, 
                    self.__config.CAMADAS_MUNDO['bg']
                    )

                """ 
                correto
                Sprite(
                    (x * self.__config.tam_sprite_padrao, y * self.__config.tam_sprite_padrao), 
                    surf, self.__all_sprites, 
                    self.__config.CAMADAS_MUNDO['bg']
                    ) 
                    #Resolver problema com uso de self.__config.tam_sprite_padrao para importar o tamanho da sprite do mapa
                    #no video o mapa está com tama dimenção de 86x86 enquanto que no nosso está 64x64
                    """

        #Água
        for obj in tmx_mapa.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), 64):#mesmo problema com o terreno com questões de tamanho 
                for y in range(int(obj.y), int(obj.y + obj.height), 64):#aqui tbm, dai coloca o 64 em vez de self.__config.tam_sprite_padrao 
                    SpriteAnimada(
                                    (x, y), 
                                    self.mapa_frames['water'], 
                                    self.all_sprites, 
                                    self.config.CAMADAS_MUNDO['water']
                                    )

        #Costa/Coast
        for obj in tmx_mapa.get_layer_by_name('Coast'):
            terreno = obj.properties['terrain']
            lado = obj.properties['side']
            SpriteAnimada(
                (obj.x, obj.y), 
                self.mapa_frames['coast'][terreno][lado], 
                self.all_sprites, self.config.CAMADAS_MUNDO['bg']
                )

        #Objetos
        for obj in tmx_mapa.get_layer_by_name('Objetos'):
            if obj.name == 'Top':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, self.config.CAMADAS_MUNDO['top'])
            else:
                ColisaoSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.colisao_sprites))

        #transição 
        for obj in tmx_mapa.get_layer_by_name('Transicao'):
            SpriteTransicao((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transicao_sprites)

        #colisão dos objetos
        for obj in tmx_mapa.get_layer_by_name('Colisao'): #No mundinho.txt de teste eu coloquei essa camada em PT-BR já 
            BordaSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.colisao_sprites)

            """ assim fica possivel ver a hitbox com o jogo aberto
            BordaSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.__all_sprites ,self.__colisao_sprites)) """

        #grama/areia (Áreas de Encontro)
        # Grama/areia (áreas de encontro) — biome define o fundo da batalha
        self.__areas_encontro.clear()
        for obj in tmx_mapa.get_layer_by_name('Grass'):
            area = SpriteAreaEncontro((obj.x, obj.y), obj.image, self.all_sprites, obj.properties['biome'])
            self.__areas_encontro.append(area)
            #Adicionar propriedade 'biome' nos matos/areias que vão fazer iniciar a batalha contra monstros pois isso define o bg na hora da batalha
            #adicionei um matinho de grama com a propriedade de 'sand' pra ver como fica uma bosta  
            #Temos esses biomes: forest, sand e ice
            
        #Entidades
        for obj in tmx_mapa.get_layer_by_name('Entidades'):
            if obj.name == 'Player':
                # Player (como já estava)
                if player_ini_pos == "dinamica":
                    self.player = Player(
                        pos = player_state["pos"],
                        frames = self.mapa_frames['characters']['player'],
                        groups = self.all_sprites,
                        olhando = player_state["direction"],
                        colisao_sprites = self.colisao_sprites
                    )
                elif obj.properties['pos'] == player_ini_pos:
                    self.player = Player(
                        pos = (obj.x, obj.y), 
                        frames = self.mapa_frames['characters']['player'], 
                        groups = self.all_sprites,
                        olhando = obj.properties['direction'],
                        colisao_sprites = self.colisao_sprites
                    ) 
            else:
                character_id = obj.properties['character_id']
                if character_id == 'Nurse':
                    # Nurse: cria NPC que CURA
                    Npc(
                        pos=(obj.x, obj.y),
                        frames=self.mapa_frames['characters'][obj.properties['graphic']],
                        groups=(self.all_sprites, self.colisao_sprites, self.npc_sprites),
                        olhando=obj.properties['direction'],
                        npc_dados=TRAINER_DATA['Nurse'],
                        player=self.player,
                        cria_dialogo=lambda npc: self.cria_dialogo_cura(npc),  # nova função de diálogo que cura
                        inicia_batalha=lambda npc: None,  # nurse não batalha
                        colisao_sprites=self.colisao_sprites,
                        raio=int(obj.properties.get('radius', 100))
                    )
                else:
                    # Demais NPCs: criam diálogo que vai terminar chamando a batalha
                    Npc(
                        pos=(obj.x, obj.y),
                        frames=self.mapa_frames['characters'][obj.properties['graphic']],
                        groups=(self.all_sprites, self.colisao_sprites, self.npc_sprites),
                        olhando=obj.properties['direction'],
                        npc_dados=TRAINER_DATA[character_id],
                        player=self.player,
                        cria_dialogo=lambda npc: self.cria_dialogo(npc),
                        inicia_batalha=lambda npc: self.iniciar_batalha_com_npc(npc),
                        colisao_sprites=self.colisao_sprites,
                        raio=int(obj.properties.get('radius', 100))
                    )

        

    #area do dialogo
    def input(self) -> None:
        if not self.arvore_dialogo:
            #INTERAÇÃO COM OS NPCs e trava a movimentação do player
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE]:
                for character in self.npc_sprites:
                    if Utils.detecta_entidade(100, self.player, character):
                        #bloquear o input do player enquanto interage
                        #entidades olham uma pra outra
                        character.muda_direcao_olhando(self.player.rect.center)
                        self.player.bloqueia()
                        character.pode_girar = False
                        self.cria_dialogo(character)
        elif self.pause_menu.active:
            self.player.bloqueia()
        elif self.mostrar_bag:
            self.player.bloqueia()
        else:
            self.player.desbloqueia()

        # Menu pause ativo -> bloqueia input do player
            return


    #transição entre mapas
    def checa_transicao(self) -> None:
        sprites = [sprite for sprite in self.transicao_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.player.bloqueia()
            self.transition_target = sprites[0].target
            self.tint_mode = 'tint'

    def pinta_tela(self, dt: float) -> None:
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                self.setup(self.tmx_mapa[self.transition_target[0]], self.transition_target[1])
                self.tint_mode = 'untint'
                self.transition_target = None

        self.tint_progress = max(0.0, min(self.tint_progress, 255.0))  # Garante que o valor esteja entre 0 e 255 e não negativo
        self.tint_surf.set_alpha(int(self.tint_progress))
        self.tela_exibicao.blit(self.tint_surf, (0, 0))
        
    def checa_encontro(self) -> None:
        '''Verifica se o jogador colidiu com uma área de encontro e aplica a chance de batalha.'''
        
        if not self.player or not self.__pode_iniciar_batalha:
            return

        player_hitbox = self.player.hitbox
        for area in self.__areas_encontro:
            if area.rect.colliderect(player_hitbox):
                if random.random() < 0.005:  # 0,5% de chance
                    print("Encontro iniciado!")
                    self.som_encontro.play()

                    ''' # Tipo do bioma (opcionalmente usado para lógica futura)
                    tipo_bioma = area.biome.lower()'''

                    # Gera o Pokémon inimigo do encontro
                    pokemon_inimigo = gerar_pokemon_encontro()

                    if pokemon_inimigo:
                        # Salva os Pokémon no contexto da batalha

                        player_team[:] =self. __bag_manager.get_selected_pokemons()
                        rival_pokemon = pokemon_inimigo

                        # Salva posição atual do jogador
                        player_state["map"] = self.transition_target[0] if self.transition_target else "mundo"
                        player_state["pos"] = self.player.rect.topleft
                        player_state["direction"] = self.player.olhando

                        # Executa a batalha e volta para a próxima cena
                        next_scene = run_battle(player_team, [rival_pokemon])

                        # Restaurar música do overworld após a batalha
                        pygame.mixer.music.load("assets/sounds/overworld.ogg")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(loops=-1)

                        self.__scene_manager.load_scene(next_scene)

                        self.__pode_iniciar_batalha = False
                        return
                    
                    
    def cria_dialogo(self, npc):
        if not self.arvore_dialogo:
            if not npc.npc_dados.get('defeated', False):
                # NPC não foi derrotado: cria diálogo e, ao terminar, chama batalha
                self.arvore_dialogo = ArvoreDeDialogo(
                    npc, 
                    self.player, 
                    self.all_sprites, 
                    self.fonts, 
                    lambda character: self.finaliza_dialogo_com_batalha(character)
                )
            else:
                # NPC já derrotado: cria diálogo que apenas termina
                self.arvore_dialogo = ArvoreDeDialogo(
                    npc,
                    self.player,
                    self.all_sprites,
                    self.fonts,
                    lambda character: self.finaliza_dialogo_sem_batalha(character)
                )
    def cura_pokemons(self, npc):
        self.__bag_manager.curar_todos_pokemons()

    def cria_dialogo_cura(self, npc):
        if not self.arvore_dialogo:
            self.arvore_dialogo = ArvoreDeDialogo(
                npc,
                self.player,
                self.all_sprites,
                self.fonts,
                lambda character: self.cura_pokemons(character)
            )
            
    def finaliza_dialogo_com_batalha(self, npc):
        self.arvore_dialogo = None
        self.player.desbloqueia()
        equipe_inimiga = []
        for _, (nome, nivel) in npc.npc_dados.get('monsters', {}).items():
            dados = self.__api_client.fetch_pokemon_data(nome)
            if dados:
                equipe_inimiga.append(Pokemon(nome, nivel, dados))
        
        if not equipe_inimiga:
            self.__bag_manager.curar_todos_pokemons()
            print("Todos os pokémons curados!")
            return

        equipe_jogador = self.__bag_manager.get_selected_pokemons()
        set_player_team(equipe_jogador)

        resultado = run_battle(equipe_jogador, equipe_inimiga)
        
        # ✅ Restaurar música do overworld após a batalha
        pygame.mixer.music.load("assets/sounds/overworld.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

        
        if resultado == "hospital":
            self.setup(self.tmx_mapa['hospital'], 'mundo')
        else:
            npc.npc_dados['defeated'] = True            
            if all(TRAINER_DATA[boss]['defeated'] for boss in ['wx', 'fx', 'px']):
                self.__scene_manager.load_scene('name_input')
            else:
                self.setup(self.tmx_mapa['mundo'], 'fogo')
                
                
    def finaliza_dialogo_sem_batalha(self, npc):
        self.arvore_dialogo = None
        self.player.desbloqueia()


    def executar(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.tela_exibicao.fill(self.config.CORES['black'])
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.pause_menu.active:
                    self.pause_menu.handle_event(evento)
                else:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            self.pause_menu.active = True
                        if evento.key == pygame.K_b:
                            self.mostrar_bag = not self.mostrar_bag
                    if self.mostrar_bag:
                        self.bag_window.handle_event(evento)

            if not self.pause_menu.active:
                self.input()
                self.checa_transicao()
                self.all_sprites.update(dt)
                self.checa_encontro()

            self.all_sprites.desenha(self.player)
            if self.arvore_dialogo:
                self.arvore_dialogo.update()
            self.pinta_tela(dt)
            if self.mostrar_bag:
                self.bag_window.draw(self.tela_exibicao)
            if self.pause_menu.active:
                self.pause_menu.draw(self.tela_exibicao)

            pygame.display.update()



            #UPDATES DA BOMBA
            self.input()
            self.checa_transicao()
            self.all_sprites.update(dt)   

            #desenhos sprites
            self.all_sprites.desenha(self.player) 

            #dialogo mano
            if self.arvore_dialogo: self.arvore_dialogo.update()

            #transição entre mapas
            self.pinta_tela(dt)
            
            #mostrar bag
            if self.mostrar_bag:
                self.bag_window.draw(self.tela_exibicao)
                
            #desenha pause por cima de tudo
            if self.pause_menu.active:
                self.pause_menu.draw(self.tela_exibicao)
            pygame.display.update()
            
            # Atualizações
            self.input()
            self.checa_transicao()
            self.all_sprites.update(dt)

            # ⬇️ Checa encontros na grama
            self.checa_encontro()

    def __del__(self):
        print("VOCÊ DEIXOU TUDO SER DESTRUIDO NA CLASSE Jogo >:(")