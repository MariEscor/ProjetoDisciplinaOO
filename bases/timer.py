# timer.py

from pygame.time import get_ticks
from typing import Callable, Union
game_start_time = None
class Timer:
	"""
    Classe para criar e gerenciar timers no jogo.

    Um timer pode ser configurado para ativar uma função após uma certa duração,
    com opções de repetição e auto-inicialização.

    Atributos:
        __duracao (int): Duração do timer em milissegundos.
        __time_inicio (int): O tempo (ticks do Pygame) em que o timer foi ativado.
        __ativo (bool): Indica se o timer está atualmente ativo.
        __repete (bool): Se o timer deve ser reiniciado automaticamente após completar.
        __funcao (Callable[..., None]): A função a ser chamada quando o timer completa.
    """
	def __init__(self, duracao: int, repete: bool = False, autostart: bool = False, funcao: Callable[..., None] = None) -> None:
		self.__duracao = duracao
		self.__time_inicio = 0
		self.__ativo = False
		self.__repete = repete
		self.__funcao = funcao
		if autostart:
			self.ativado()

	@property
	def duracao(self) -> int:
		return self.__duracao

	@duracao.setter
	def duracao(self, value: int) -> None:
		if not isinstance(value, int) or value < 0:
			raise ValueError("A 'duracao' deve ser um inteiro não negativo.")
		self.__duracao = value

	@property
	def time_inicio(self) -> int:
		return self.__time_inicio

	@time_inicio.setter
	def time_inicio(self, value: int) -> None:
		if not isinstance(value, int) or value < 0:
			raise ValueError("O 'time_inicio' deve ser um inteiro não negativo.")
		self.__time_inicio = value

	@property
	def ativo(self) -> bool:
		return self.__ativo

	@ativo.setter
	def ativo(self, value: bool) -> None:
		if not isinstance(value, bool):
			raise ValueError("O 'ativo' deve ser um valor booleano.")
		self.__ativo = value

	@property
	def repete(self) -> bool:
		return self.__repete

	@repete.setter
	def repete(self, value: bool) -> None:
		if not isinstance(value, bool):
			raise ValueError("O 'repete' deve ser um valor booleano.")
		self.__repete = value

	@property
	def funcao(self) -> Callable[..., None]:
		return self.__funcao

	@funcao.setter
	def funcao(self, value: Callable[..., None]) -> None:
		if value is not None and not callable(value):
			raise TypeError("A 'funcao' deve ser uma função chamável ou None.")
		self.__funcao = value

	def ativado(self) -> None:
		self.ativo = True
		self.time_inicio = get_ticks()

	def desativado(self):
		self.ativo = False
		self.time_inicio = 0
		if self.repete:
			self.ativado()

	def update(self):
		if self.ativo:
			time_atual: int = get_ticks()
			if time_atual - self.time_inicio >= self.duracao:
				if self.funcao: self.funcao()
				self.desativado()