# arvore_de_dialogo.py

import pygame
from sprites.sprite_dialogo import SpriteDialogo
from Projeto.timer import Timer
from typing import Callable, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from entidades.entidades import Entidades

class ArvoreDeDialogo:
    """
    Gerencia a sequência de diálogos entre o jogador e um personagem (NPC).

    Esta classe controla o fluxo das mensagens, avança para a próxima fala ao interagir
    e sinaliza o fim do diálogo através de um callback.

    Atributos:
        __player (Entidades): A instância do jogador.
        __character (Entidades): A instância do personagem (NPC) com quem o diálogo está ocorrendo.
        __fonts (Dict[str, pygame.font.Font]): Dicionário de fontes do jogo, usado para renderizar o texto.
        __all_sprites (pygame.sprite.Group): Grupo de sprites principal do jogo para adicionar/remover o SpriteDialogo.
        __finaliza_dialogo (Callable[[Entidades], None]): Função de callback a ser chamada quando o diálogo termina.
        __dialogo (List[str]): Lista de strings, cada uma representando uma linha de diálogo.
        __dialogo_num (int): Número total de linhas de diálogo.
        __dialogo_index (int): Índice da linha de diálogo atual sendo exibida.
        __dialogo_atual (SpriteDialogo): A instância da sprite de diálogo atualmente visível.
        __timer_dialogo (Timer): Um timer para controlar o tempo entre o avanço dos diálogos.
    """
    def __init__(self, character: 'Entidades', player: 'Entidades', all_sprites: pygame.sprite.Group, fonts: Dict[str, pygame.font.Font], finaliza_dialogo: Callable[['Entidades'], None]) -> None:
        self.__player: 'Entidades' = player
        self.__character: 'Entidades' = character
        self.__fonts: Dict[str, pygame.font.Font] = fonts
        self.__all_sprites: pygame.sprite.Group = all_sprites
        # Callable[[Entidades], None] indica que a função espera um objeto Entidades e não retorna nada.
        self.__finaliza_dialogo: Callable[['Entidades'], None] = finaliza_dialogo

        self.__dialogo: List[str] = self.character.obter_dialogo()
        self.__dialogo_num: int = len(self.dialogo)
        self.__dialogo_index: int = 0


        self.__dialogo_atual: SpriteDialogo = SpriteDialogo(
            self.dialogo[self.dialogo_index],
            self.character,
            self.all_sprites,
            self.fonts['dialog']
        )

        self.__timer_dialogo: Timer = Timer(500, autostart = True) 

    @property
    def player(self) -> 'Entidades':
        return self.__player

    @player.setter
    def player(self, value: 'Entidades') -> None:
        if not isinstance(value, object) or not hasattr(value, 'rect'):
            raise TypeError("O 'player' deve ser uma instância de Entidades ou similar com atributo 'rect'.")
        self.__player = value

    @property
    def character(self) -> 'Entidades':
        return self.__character

    @character.setter
    def character(self, value: 'Entidades') -> None:
        if not isinstance(value, object) or not hasattr(value, 'rect'):
            raise TypeError("O 'character' deve ser uma instância de Entidades ou similar com atributo 'rect'.")
        self.__character = value

    @property
    def fonts(self) -> Dict[str, pygame.font.Font]:
        return self.__fonts

    @fonts.setter
    def fonts(self, value: Dict[str, pygame.font.Font]) -> None:
        if not isinstance(value, dict) or not all(isinstance(f, pygame.font.Font) for f in value.values()):
            raise TypeError("As 'fonts' devem ser um dicionário onde os valores são instâncias de pygame.font.Font.")
        self.__fonts = value

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        return self.__all_sprites

    @all_sprites.setter
    def all_sprites(self, value: pygame.sprite.Group) -> None:
        if not isinstance(value, pygame.sprite.Group):
            raise TypeError("O 'all_sprites' deve ser um grupo de sprites de Pygame.")
        self.__all_sprites = value

    @property
    def finaliza_dialogo(self) -> Callable[['Entidades'], None]:
        return self.__finaliza_dialogo

    @finaliza_dialogo.setter
    def finaliza_dialogo(self, value: Callable[['Entidades'], None]) -> None:
        if not callable(value):
            raise TypeError("O 'finaliza_dialogo' deve ser uma função de callback.")
        self.__finaliza_dialogo = value

    @property
    def dialogo(self) -> List[str]:
        return self.__dialogo

    @dialogo.setter
    def dialogo(self, value: List[str]) -> None:
        if not isinstance(value, list) or not all(isinstance(s, str) for s in value):
            raise TypeError("O 'dialogo' deve ser uma lista de strings.")
        self.__dialogo = value

    @property
    def dialogo_num(self) -> int:
        return self.__dialogo_num

    @dialogo_num.setter
    def dialogo_num(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise TypeError("O 'dialogo_num' deve ser um inteiro não negativo.")
        self.__dialogo_num = value

    @property
    def dialogo_index(self) -> int:
        return self.__dialogo_index

    @dialogo_index.setter
    def dialogo_index(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise TypeError("O 'dialogo_index' deve ser um inteiro não negativo.")
        self.__dialogo_index = value

    @property
    def dialogo_atual(self) -> SpriteDialogo:
        return self.__dialogo_atual

    @dialogo_atual.setter
    def dialogo_atual(self, value: SpriteDialogo) -> None:
        if not isinstance(value, SpriteDialogo):
            raise TypeError("O 'dialogo_atual' deve ser uma instância de SpriteDialogo.")
        self.__dialogo_atual = value

    @property
    def timer_dialogo(self) -> Timer:
        return self.__timer_dialogo

    @timer_dialogo.setter
    def timer_dialogo(self, value: Timer) -> None:
        if not isinstance(value, Timer):
            raise TypeError("O 'timer_dialogo' deve ser uma instância de Timer.")
        self.__timer_dialogo = value

    def input(self) -> None:
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and not self.timer_dialogo.ativo:
            self.dialogo_atual.kill()
            self.dialogo_index += 1

            if self.dialogo_index < self.dialogo_num:
                self.dialogo_atual = SpriteDialogo(
                    self.dialogo[self.dialogo_index], 
                    self.character, 
                    self.all_sprites, 
                    self.fonts['dialog']
                    )
                self.timer_dialogo.ativado()
            else:
                self.finaliza_dialogo(self.character)

    def update(self) -> None:
        self.timer_dialogo.update()
        self.input()