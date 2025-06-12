#25-06-11 23h30 ok
import pygame

class Animacao(pygame.sprite.Sprite):
    def __init__(self, posicao: tuple, quadros: dict, estado_inicial: str, direcao_inicial: str, velocidade_animacao: float) -> None:
        super().__init__()
        self.__quadros = quadros
        self.__indice_quadro = 0.0        
        self.__estado = estado_inicial
        self.__direcao = direcao_inicial
        self.__velocidade_animacao = velocidade_animacao

        try:
            self.__image = self.__quadros[f'{self.__direcao}_{self.__estado}'][int(self.__indice_quadro)]
            self.__rect = self.__image.get_rect(topleft=posicao)
        except KeyError as e:
            raise ValueError(f"Erro imagem inicial. quadros contem: '{self.__direcao}_{self.__estado}': {e}")
        except IndexError as e:
            raise ValueError(f"Erro índice ao carreagar a imagem inicial. O quadro {int(self.__indice_quadro)} não existe para '{self.__direcao}_{self.__estado}': {e}")

        print("Instância de Animacao ta ok(eu acho)")

    @property
    def quadros(self) -> dict:
        return self.__quadros
    
    @quadros.setter
    def quadros(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise TypeError("Quadros deve ser um dicionário.")
        self.__quadros = value

    @property
    def indice_quadro(self) -> float:
        return self.__indice_quadro
    
    @indice_quadro.setter
    def indice_quadro(self, value: float) -> None:
        if not isinstance(value, float) or value < 0:
            raise TypeError("Índice do quadro deve ser um float não negativo.")
        self.__indice_quadro = value

    @property
    def estado(self) -> str:
        return self.__estado
    
    @estado.setter
    def estado(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Estado deve ser uma string.")
        self.__estado = value
        self.__atualizar_imagem_e_rect()

    @property
    def direcao(self) -> str:
        return self.__direcao
    
    @direcao.setter
    def direcao(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Direção deve ser uma string.")
        self.__direcao = value
        self.__atualizar_imagem_e_rect()

    @property
    def velocidade_animacao(self) -> float:
        return self.__velocidade_animacao
    
    @velocidade_animacao.setter
    def velocidade_animacao(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Velocidade da animação deve ser um número positivo.")
        self.__velocidade_animacao = value

    @property
    def image(self) -> pygame.Surface:
        return self.__image
    
    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if not isinstance(value, pygame.Surface):
            raise TypeError("Imagem deve ser uma instância de pygame.Surface.")
        self.__image = value
    
    @property
    def rect(self) -> pygame.Rect:
        return self.__rect
    
    @rect.setter
    def rect(self, value: pygame.Rect) -> None:
        if not isinstance(value, pygame.Rect):
            raise TypeError("Rect deve ser uma instância de pygame.Rect.")
        self.__rect = value

    def __atualizar_imagem_e_rect(self) -> None:
        try:
            chave_animacao = f'{self.__direcao}_{self.__estado}'
            if chave_animacao not in self.__quadros or not self.__quadros[chave_animacao]:
                raise ValueError(f"Quadros não contém a chave '{chave_animacao}' ou está vazio.")
            
            num_quadros = len(self.__quadros[chave_animacao])
            if self.__indice_quadro >= num_quadros:
                self.__indice_quadro = 0.0

            nova_imagem = self.__quadros[chave_animacao][int(self.__indice_quadro)]
            novo_rect = nova_imagem.get_rect(topleft=self.rect.topleft)

            self.__image = nova_imagem
            self.__rect = novo_rect
        except Exception as e:
            print(f"impossível atualizar imagem/rect para '{chave_animacao}': {e}")

    def update(self, dt: float) -> None:
        self.__indice_quadro += self.__velocidade_animacao * dt
            
        chave_animacao = f'{self.__direcao}_{self.__estado}'
        if chave_animacao in self.__quadros and self.__quadros[chave_animacao]:
            num_quadros = len(self.__quadros[chave_animacao])
            if num_quadros > 0:
                self.__indice_quadro %= num_quadros
            self.__image = self.__quadros[chave_animacao][int(self.__indice_quadro)]
        else:
            print(f"Chave de animação '{chave_animacao}' não encontrada ou sem quadros.")

    def __del__(self):
        print("CÊ MATOU A ANIMAÇÃO >:(")