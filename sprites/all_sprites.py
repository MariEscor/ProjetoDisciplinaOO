# all_sprites.py

import pygame
from pygame.math import Vector2 as vector

from bases.config import Config
from entidades.entidades import Entidades
from bases.utils import Utils
from typing import List, Union

class AllSprites(pygame.sprite.Group):
    """
    Grupo de sprites personalizado responsável por gerenciar e desenhar
    todas as sprites visuais do jogo na tela.

    Esta classe implementa uma "câmera" simples, centralizando a visão no jogador,
    e organiza as sprites por camadas de profundidade (z-index) para uma
    renderização correta (elementos do fundo, principais, da frente).
    Também lida com a renderização de sombras e notificações para o jogador.

    Atributos:
        __tela_exibicao (pygame.Surface): A superfície principal onde as sprites são desenhadas.
        __offset (vector): O vetor de deslocamento da câmera, usado para simular o movimento do mundo.
        __config (Config): Uma instância da classe de configuração do jogo para acesso a dimensões de tela e camadas.
        __sombrinha (pygame.Surface): A superfície da imagem da sombra a ser desenhada sob as entidades.
        __notificacao_surf (pygame.Surface): A superfície da imagem de notificação do jogador.
    """
    def __init__(self, config_obj: Config) -> None:
        super().__init__()
        self.__tela_exibicao: pygame.Surface = pygame.display.get_surface()
        self.__offset = vector()
        self.__config: Config = config_obj
        self.__sombrinha: pygame.Surface = Utils.importar_imagem('assets', 'graphics', 'other', 'shadow')
        self.__notificacao_surf: pygame.Surface = Utils.importar_imagem('assets', 'graphics', 'ui', 'notice')

    @property
    def tela_exibicao(self) -> pygame.Surface:
        return self.__tela_exibicao

    @tela_exibicao.setter
    def tela_exibicao(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'tela_exibicao' deve ser uma instância de pygame.Surface.")
        self.__tela_exibicao = value

    @property
    def offset(self) -> vector:
        return self.__offset

    @offset.setter
    def offset(self, value: vector) -> None:
        if not isinstance(value, vector):
            raise TypeError("O 'offset' deve ser um pygame.math.Vector2.")
        self.__offset = value

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, value: Config) -> None:
        if not isinstance(value, Config):
            raise TypeError("O 'config' deve ser uma instância da classe Config.")
        self.__config = value

    @property
    def sombrinha(self) -> pygame.Surface:
        return self.__sombrinha

    @sombrinha.setter
    def sombrinha(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'sombrinha' deve ser uma instância de pygame.Surface.")
        self.__sombrinha = value

    @property
    def notificacao_surf(self) -> pygame.Surface:
        return self.__notificacao_surf

    @notificacao_surf.setter
    def notificacao_surf(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("A 'notificacao_surf' deve ser uma instância de pygame.Surface.")
        self.__notificacao_surf = value

    def desenha(self, player: pygame.sprite.Sprite) -> None:
        """
        Desenha todas as sprites do grupo na tela, aplicando o deslocamento da câmera
        e ordenando por camadas de profundidade.

        Args:
            player (pygame.sprite.Sprite): A sprite do jogador, usada para centralizar a câmera.
        """
        #câmera
        self.offset.x = - (player.rect.centerx - self.config.largura_tela / 2)
        self.offset.y = - (player.rect.centery - self.config.altura_tela / 2)

        # Organiza as sprites por camadas de profundidade
        bg_sprites: List[pygame.sprite.Sprite] = [sprite for sprite in self if sprite.z < (self.config.CAMADAS_MUNDO['main'])]
        main_sprites: List[pygame.sprite.Sprite] = sorted(
                                [sprite for sprite in self if sprite.z == self.config.CAMADAS_MUNDO['main']], 
                                key = lambda sprite: sprite.y_sort
                            )
        fg_sprites: List[pygame.sprite.Sprite] = [sprite for sprite in self if sprite.z > self.config.CAMADAS_MUNDO['main']]

        # Itera sobre as camadas e desenha as sprites
        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                # Desenha a sombra se a sprite for uma Entidade (Jogador ou NPC)
                if isinstance(sprite, Entidades):
                    self.tela_exibicao.blit(self.sombrinha, sprite.rect.topleft + self.offset + vector(40, 110))
                
                self.tela_exibicao.blit(sprite.image, sprite.rect.topleft + self.offset)

                # Desenha a notificação se a sprite for o jogador e a notificação estiver ativa
                if sprite == player and hasattr(player, 'notificacao') and player.notificacao:
                    rect_notificacao = self.notificacao_surf.get_frect(midbottom = sprite.rect.midtop)
                    self.tela_exibicao.blit(self.notificacao_surf, rect_notificacao.topleft + self.offset)