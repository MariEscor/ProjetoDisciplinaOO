# entidades.py

import pygame
from pygame.math import Vector2 as vector
from bases.config import Config
from typing import Dict, List, Any

class Entidades(pygame.sprite.Sprite):
    """
    Classe base para todas as entidades dinâmicas do jogo, como o jogador e NPCs.

    Esta classe gerencia propriedades e comportamentos comuns a todas as entidades,
    incluindo gráficos, movimento, colisão e estados de animação.

    Atributos:
        __z (float): A camada de profundidade da sprite para ordenação de desenho.
        __frames_index (float): Índice de frame atual para controle de animação.
        __frames (Dict[str, List[pygame.Surface]]): Dicionário contendo as superfícies de animação
                                                    para diferentes estados (ex: 'up_idle', 'down', 'left').
        __olhando (str): A direção para a qual a entidade está olhando ('up', 'down', 'left', 'right').
        __direcao (vector): Vetor de direção do movimento da entidade.
        __velocidade (float): Velocidade de movimento da entidade em pixels por segundo.
        __bloqueado (bool): Indica se a entidade está atualmente bloqueada e não pode se mover.
        __image (pygame.Surface): A superfície visual atual da entidade.
        __rect (pygame.Rect): O retângulo que define a posição e o tamanho da entidade no jogo.
        __hitbox (pygame.Rect): O retângulo usado para detecção de colisões da entidade,
                                frequentemente menor que o 'rect' para colisões mais precisas.
        __y_sort (float): Valor para ordenação de sprites na tela (profundidade de desenho).
    """
    def __init__(self, pos: tuple[int, int], frames: Dict[str, List[pygame.Surface]], groups: pygame.sprite.Group, olhando: str) -> None:
        super().__init__(groups)
        self.__z: float = Config().CAMADAS_MUNDO['main']  


        # Gráficos
        self.__frames_index: float = 0.0
        self.__frames: Dict[str, List[pygame.Surface]] = frames
        self.__olhando: str = olhando 

        # Movimento
        self.__direcao: vector = vector()
        self.__velocidade: float = 250.0
        self.__bloqueado: bool = False

        # Configuração da sprite (imagem e retângulos)
        self.__image: pygame.Surface = self.frames[self.mexeu()][int(self.frames_index)]
        self.__rect: pygame.Rect = self.__image.get_frect(center = pos)
        # Ajusta a hitbox para ser 60% menor em altura, centralizada verticalmente, como em colisao_sprite.py
        self.__hitbox: pygame.Rect = self.__rect.inflate(-self.__rect.width / 2, -int(self.rect.height * 0.6))

        self.__y_sort: float = float(self.rect.centery)

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("A camada z deve ser um número(float ou int).")
        self.__z = value

    @property
    def frames_index(self) -> float:
        return self.__frames_index

    @frames_index.setter
    def frames_index(self, value: float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("O 'frames_index' deve ser um número(float ou int).")
        self.__frames_index = float(value)

    @property
    def frames(self) -> Dict[str, List[pygame.Surface]]:
        return self.__frames

    @frames.setter
    def frames(self, value: Dict[str, List[pygame.Surface]]) -> None:
        if not isinstance(value, dict) or not all(isinstance(k, str) and isinstance(v, list) and all(isinstance(s, pygame.Surface) for s in v) for k, v in value.items()):
            raise TypeError("Os 'frames' devem ser um dicionário com listas de superfícies Pygame.")
        self.__frames = value

    @property
    def olhando(self) -> str:
        return self.__olhando

    @olhando.setter
    def olhando(self, value: str) -> None:
        if not isinstance(value, str) or value not in ['up', 'down', 'left', 'right']: #possivel erro caso troque para PT-BR as direções
            raise ValueError("A direção 'olhando' deve ser uma string válida ('up', 'down', 'left', 'right').")
        self.__olhando = value

    @property
    def direcao(self) -> vector:
        return self.__direcao

    @direcao.setter
    def direcao(self, value: vector) -> None:
        if not isinstance(value, vector):
            raise TypeError("A 'direcao' deve ser um pygame.math.Vector2.")
        self.__direcao = value

    @property
    def velocidade(self) -> float:
        return self.__velocidade

    @velocidade.setter
    def velocidade(self, value: float) -> None:
        if not isinstance(value, (float, int)) or value < 0:
            raise ValueError("A 'velocidade' deve ser um número positivo (float ou int).")
        self.__velocidade = value

    @property
    def bloqueado(self) -> bool:
        return self.__bloqueado

    @bloqueado.setter
    def bloqueado(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("O 'bloqueado' deve ser um booleano.")
        self.__bloqueado = value

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'image' deve ser uma superfície Pygame.")
        self.__image = value

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @rect.setter
    def rect(self, value: pygame.Rect) -> None:
        if not isinstance(value, (pygame.Rect, pygame.FRect)):
            raise TypeError("O 'rect' deve ser um pygame.Rect.")
        self.__rect = value

    @property
    def hitbox(self) -> pygame.Rect:
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, value: pygame.Rect) -> None:
        if not isinstance(value, (pygame.Rect, pygame.FRect)):
            raise TypeError("A 'hitbox' deve ser um pygame.Rect.")
        self.__hitbox = value

    @property
    def y_sort(self) -> float:
        return self.__y_sort

    @y_sort.setter
    def y_sort(self, value: float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("O 'y_sort' deve ser um número (float ou int).")
        self.__y_sort = value


    def mexe_ai_poh(self, dt: float) -> None: #mexe_ai_poh == animate()
        self.frames_index += Config().vel_animacao * dt
        self.image = self.frames[self.mexeu()][int(self.frames_index) % len(self.frames[self.mexeu()])]

    def mexeu(self) -> str: #mexeu == get_state()
        movendo: bool = bool(self.direcao)
        if movendo:
            if self.direcao.x != 0:
                self.olhando = 'right' if self.direcao.x > 0 else 'left'
            if self.direcao.y != 0:
                self.olhando = 'down' if self.direcao.y > 0 else 'up'
        
        # Retorna o estado combinando a direção de "olhando" com "_idle" se não estiver movendo
        return f'{self.olhando}{"" if movendo else "_idle"}'

    #muda a direção que a entidade está olhando, baseado com o input do player 
    def muda_direcao_olhando(self, alvo_pos: tuple[int, int]) -> None:

        # Calcula o vetor de relação entre a entidade e o alvo
        relacao: vector = vector(alvo_pos) - vector(self.rect.center)
        
        # Se a diferença em Y for pequena, a direção horizontal é mais relevante
        if abs(relacao.y) < 30:
            self.olhando = 'right' if relacao.x > 0 else 'left'
        else:
            self.olhando = 'down' if relacao.y > 0 else 'up'

    #bloqueia a entidade, impedindo movimento
    def bloqueia(self) -> None:
        self.bloqueado = True
        self.direcao = vector(0,0)

    #desbloqueia a entidade, permitindo movimento
    def desbloqueia(self) -> None:
        self.bloqueado = False