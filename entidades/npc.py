# npc.py

import pygame
from pygame.math import Vector2 as vector
from random import choice
from typing import Dict, List, Any, Callable, TYPE_CHECKING

from entidades.entidades import Entidades
from Projeto.utils import Utils
from Projeto.timer import Timer

# Para evitar importações circulares, 'Player' e 'Sprite' são importados
# apenas para fins de verificação de tipo (type checking) usando TYPE_CHECKING.
if TYPE_CHECKING:
    from entidades.player import Player
    from sprites.sprite import Sprite

class Npc(Entidades):
    """
    Representa um personagem não jogável (NPC) no jogo.

    Esta classe herda de Entidades e implementa comportamentos específicos de NPC,
    como a capacidade de olhar ao redor, detectar o jogador, mover-se em sua direção
    e iniciar diálogos.

    Atributos:
        __npc_dados (Dict[str, Any]): Dicionário com os dados específicos do NPC
                                    (e.g., monstros, diálogos, direções de visão).
        __player (Player): A instância do jogador para detecção e interação.
        __cria_dialogo (Callable[['Npc'], None]): Função de callback para iniciar um diálogo.
        __colisao_rects (List[pygame.Rect]): Lista de retângulos de sprites de colisão do cenário
                                            para verificação da linha de visão.
        __pode_mover (bool): Indica se o NPC está atualmente em movimento em direção ao jogador.
        __pode_girar (bool): Indica se o NPC pode mudar sua direção de visão aleatoriamente.
        __notou_player (bool): Indica se o NPC já notou o jogador uma vez.
        __raio (int): O raio de visão do NPC para detectar o jogador.
        __visao_direcoes (List[str]): Lista de direções ('up', 'down', 'left', 'right')
                                    que o NPC pode olhar.
        __timers (Dict[str, Timer]): Dicionário de timers para controlar ações do NPC
                                    (e.g., 'look_around' para mudar direção, 'notice' para atrasar movimento).
    """
    def __init__(self, pos: tuple[int, int], frames: Dict[str, List[pygame.Surface]], groups: pygame.sprite.Group, olhando: str, npc_dados: Dict[str, Any], player: 'Player', cria_dialogo: Callable[['Npc'], None], colisao_sprites: pygame.sprite.Group, raio: int) -> None:
        super().__init__(pos, frames, groups, olhando)

        self.__npc_dados: Dict[str, Any] = npc_dados
        self.__player: 'Player' = player
        self.__cria_dialogo: Callable[['Npc'], None] = cria_dialogo
        # Extrai os retângulos para as colisões de linha de visão
        self.__colisao_rects: List[pygame.Rect] = [sprite.rect for sprite in colisao_sprites if sprite is not self]

        self.__pode_mover: bool = False # Controla se o NPC pode se movimentar
        self.__pode_girar: bool = True # Controla se o NPC pode mudar sua direção de visão
        self.__notou_player: bool = False # Controla se o NPC já notou o player
        
        self.__raio: int = int(raio) # Raio de visão do NPC
        self.__visao_direcoes: List[str] = npc_dados['directions'] # Direções para as quais o NPC pode olhar

        # Dicionário de timers para controlar ações específicas do NPC
        self.__timers: Dict[str, Timer] = {

            'look_around': Timer(1500, autostart = True, repete = True, funcao = self.olhada_aleatoria), # Timer para mudar direção de visão

            'notice': Timer(500, funcao=self.comeca_mover) # Timer para atrasar o início do movimento após notar o player

        }

    @property
    def npc_dados(self) -> Dict[str, Any]:
        return self.__npc_dados

    @npc_dados.setter
    def npc_dados(self, value: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("Os 'npc_dados' devem ser um dicionário.")
        self.__npc_dados = value

    @property
    def player(self) -> 'Player':
        return self.__player

    @player.setter
    def player(self, value: 'Player') -> None:
        if not isinstance(value, object) or not hasattr(value, 'rect') or not hasattr(value, 'bloqueia') or not hasattr(value, 'muda_direcao_olhando') or not hasattr(value, 'notificacao'):
            raise TypeError("O 'player' deve ser uma instância de Player ou similar.")
        self.__player = value

    @property
    def cria_dialogo(self) -> Callable[['Npc'], None]:
        return self.__cria_dialogo

    @cria_dialogo.setter
    def cria_dialogo(self, value: Callable[['Npc'], None]) -> None:
        if not callable(value):
            raise TypeError("A 'cria_dialogo' deve ser uma função de callback.")
        self.__cria_dialogo = value

    @property
    def colisao_rects(self) -> List[pygame.Rect]:
        return self.__colisao_rects

    @colisao_rects.setter
    def colisao_rects(self, value: List[pygame.Rect]) -> None:
        if not isinstance(value, list) or not all(isinstance(r, pygame.Rect) for r in value):
            raise TypeError("Os 'colisao_rects' devem ser uma lista de pygame.Rect.")
        self.__colisao_rects = value

    @property
    def pode_mover(self) -> bool:
        return self.__pode_mover

    @pode_mover.setter
    def pode_mover(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("O 'pode_mover' deve ser um valor booleano.")
        self.__pode_mover = value

    @property
    def pode_girar(self) -> bool:
        return self.__pode_girar

    @pode_girar.setter
    def pode_girar(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("O 'pode_girar' deve ser um valor booleano.")
        self.__pode_girar = value

    @property
    def notou_player(self) -> bool:
        return self.__notou_player

    @notou_player.setter
    def notou_player(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("O 'notou_player' deve ser um valor booleano.")
        self.__notou_player = value

    @property
    def raio(self) -> int:
        return self.__raio

    @raio.setter
    def raio(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("O 'raio' deve ser um inteiro positivo.")
        self.__raio = value

    @property
    def visao_direcoes(self) -> List[str]:
        return self.__visao_direcoes

    @visao_direcoes.setter
    def visao_direcoes(self, value: List[str]) -> None:
        if not isinstance(value, list) or not all(isinstance(d, str) for d in value):
            raise TypeError("As 'visao_direcoes' devem ser uma lista de strings.")
        self.__visao_direcoes = value

    @property
    def timers(self) -> Dict[str, Timer]:
        return self.__timers

    @timers.setter
    def timers(self, value: Dict[str, Timer]) -> None:
        if not isinstance(value, dict) or not all(isinstance(t, Timer) for t in value.values()):
            raise TypeError("Os 'timers' devem ser um dicionário com instâncias de Timer.")
        self.__timers = value

    #random_view_direction
    def olhada_aleatoria(self) -> None:
        if self.pode_girar:
            self.olhando = choice(self.visao_direcoes)

    #pega a area dialog de game_data e escolhe o dialogo entre o default e o defeated que será usado na arvorededialogo.py
    def obter_dialogo(self) -> List[str]:
        # Acessa npc_dados para determinar qual diálogo retornar
        return self.npc_dados['dialog'][f"{'defeated' if self.__npc_dados['defeated'] else 'default'}"] 

    #def raycast(self):
    def linha_visao(self) -> None:
        # Utils.detecta_entidade verifica se o player está no raio de visão e direção
        if Utils.detecta_entidade(self.raio, self, self.player) and self.to_te_vendu() and not self.pode_mover and not self.notou_player:
            self.player.bloqueia() # Bloqueia o movimento do jogador 
            self.player.muda_direcao_olhando(self.rect.center) # Faz o jogador olhar para o NPC 
            self.timers['notice'].ativado() # Ativa o timer de notificação do NPC 
            self.pode_girar = False # Impede o NPC de girar aleatoriamente
            self.notou_player = True # Marca que o NPC já notou o jogador
            self.player.notificacao = True # Ativa a notificação visual no jogador

    #def has_los(self):
    #isso é reposavel em fazer com que o npc não reaja com o player se tiver algo entre eles tipo alguma colisao do tmx
    def to_te_vendu(self):
        if vector(self.rect.center).distance_to(self.player.rect.center) < self.raio: # Verifica se o jogador está dentro do raio de visão 
            # Verifica se há alguma colisão entre a linha de visão do NPC e os objetos de colisão do cenário
            colisao: List[bool] = [bool(rect.clipline(self.rect.center, self.player.rect.center)) for rect in self.colisao_rects]
            return not any(colisao) # Retorna True se não houver nenhuma colisão (linha de visão limpa) 
        return False # Retorna False se o jogador estiver fora do raio de visão

    #faz o npc se movimentar até o player
    def comeca_mover(self) -> None:

        relacao: vector = (vector(self.player.rect.center) - vector(self.rect.center)).normalize()
        self.direcao = vector(round(relacao.x), round(relacao.y))

    #movendo
    def mexendo(self, dt: float) -> None:
        if not self.pode_mover and self.direcao:
            # Move o NPC se ele não colidiu com o jogador (com uma pequena margem)
            if not self.hitbox.inflate(10, 10).colliderect(self.player.hitbox):
                self.rect.center += self.direcao * self.velocidade * dt
                self.hitbox.center = self.rect.center
            else:
                # Se o NPC colidiu com o jogador, para o movimento, marca como 'pode_mover' (já se moveu)
                # e inicia o diálogo.
                self.direcao = vector()
                self.pode_mover = True
                self.cria_dialogo(self) # Chama a função de callback para criar o diálogo
                self.player.notificacao = False # Desativa a notificação visual do jogador


    def update(self, dt: float) -> None:
        for timer in self.timers.values():
            timer.update()

        self.mexe_ai_poh(dt) # Chama o método de animação da classe Entidades
        if self.npc_dados['look_around']: # Verifica se o NPC está configurado para olhar em volta
            self.linha_visao() # Verifica a linha de visão com o jogador
            self.mexendo(dt) # Controla o movimento em direção ao jogador
