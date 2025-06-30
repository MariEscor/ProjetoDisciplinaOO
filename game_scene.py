#game_scene.py
# game_scene.py
import pygame

class GameScene:
    """
    Classe base abstrata para todas as cenas do jogo.
    Todas as cenas devem herdar desta classe e implementar seus métodos.
    """
    def __init__(self) -> None:
        # Sinaliza a próxima cena para a qual o jogo deve transicionar.
        # Definido para None por padrão, indicando que não há transição pendente.
        self.next_scene: str | None = None
        
        # Um dicionário para passar dados entre cenas (ex: nome do jogador, Pokémon escolhido).
        self.scene_data: dict | None = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Processa todos os eventos de entrada (mouse, teclado) para a cena atual.
        Deve ser implementado pelas subclasses.
        """
        pass

    def update(self) -> None:
        """
        Atualiza a lógica da cena (movimento, animações, estado do jogo).
        Deve ser implementado pelas subclasses.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha os elementos da cena na tela.
        Deve ser implementado pelas subclasses.
        """
        pass

    def cleanup(self) -> None:
        """
        Opcional: Limpa recursos específicos da cena quando ela é desativada.
        (Ex: descarregar imagens ou sons pesados).
        """
        pass