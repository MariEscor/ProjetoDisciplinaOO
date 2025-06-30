# player.py

import pygame
from pygame.math import Vector2 as vector
from entidades.entidades import Entidades

class Player(Entidades):
    """
    Representa o personagem jogável principal do jogo.

    Esta classe herda de Entidades e adiciona funcionalidades específicas
    ao jogador, como processamento de input do teclado, movimentação baseada
    no jogador e detecção de notificação.

    Atributos:
        __colisao_sprites (pygame.sprite.Group): Grupo de sprites com as quais
                                                o jogador pode colidir.
        __notificacao (bool): Indica se o jogador foi notificado (e.g., visto
                            por um NPC, ativando um diálogo).
    """
    def __init__(self, pos: tuple[int, int], frames: dict[str, list[pygame.Surface]], groups: pygame.sprite.Group, olhando: str, colisao_sprites: pygame.sprite.Group) -> None:
        super().__init__(pos, frames, groups, olhando)

        self.__colisao_sprites: pygame.sprite.Group = colisao_sprites
        self.__notificacao: bool = False # notificação por ser visto

    @property
    def colisao_sprites(self) -> pygame.sprite.Group:
        return self.__colisao_sprites

    @colisao_sprites.setter
    def colisao_sprites(self, value: pygame.sprite.Group) -> None:
        if not isinstance(value, pygame.sprite.Group):
            raise TypeError("O 'colisao_sprites' deve ser um grupo de sprites Pygame.")
        self.__colisao_sprites = value

    @property
    def notificacao(self) -> bool:
        return self.__notificacao

    @notificacao.setter
    def notificacao(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("A 'notificacao' deve ser um valor booleano.")
        self.__notificacao = value

    def input(self) -> None:
        keys = pygame.key.get_pressed()
        input_vector: vector = vector()
        
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1

        # Normaliza o vetor de input para garantir velocidade consistente em diagonais
        self.direcao = input_vector.normalize() if input_vector else input_vector

    def move(self, dt: float) -> None:
        
        # Movimento horizontal
        self.rect.centerx += self.direcao.x * self.velocidade * dt / 2
        self.hitbox.centerx = self.rect.centerx
        self.colisao('horizontal')

        # Movimento vertical
        self.rect.centery += self.direcao.y * self.velocidade * dt / 2
        
        self.hitbox.centery = self.rect.centery
        self.colisao('vertical')

    def colisao(self, eixo: str) -> None:
        for sprite in self.colisao_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if eixo == 'horizontal':
                    if self.direcao.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direcao.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else: # eixo == 'vertical'
                    if self.direcao.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direcao.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def update(self, dt: float) -> None:
        self.y_sort = self.rect.centery
        if not self.bloqueado: 
            self.input()
            self.move(dt)
        self.mexe_ai_poh(dt) 

    def __del__(self) -> None:
        print("CÊ MATOU O PLAYER >:(")