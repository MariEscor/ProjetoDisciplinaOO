import pygame
import constants
from selection_scene import SelectionScene
from battle_scene import BattleScene

class Game:
    """
    Classe principal que gerencia o jogo, o loop principal e as cenas.
    """
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
        pygame.display.set_caption('Batalha Pokemon')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Dicionário de cenas para fácil transição
        self.scenes = {
            'selection': SelectionScene(),
            'battle': None  # A cena de batalha será criada quando um Pokémon for escolhido
        }
        self.current_scene = self.scenes['selection']

    def run(self) -> None:
        """
        Inicia e executa o loop principal do jogo.
        """
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Delega o processamento de eventos e a lógica de atualização para a cena atual
            self.current_scene.handle_events(events)
            self.current_scene.update()
            
            # Verifica se a cena sinalizou uma transição
            next_scene_key = self.current_scene.next_scene
            if next_scene_key is not None:
                self.switch_scene(next_scene_key)

            # Desenha a cena atual na tela
            self.current_scene.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def switch_scene(self, scene_key: str) -> None:
        """
        Muda para uma nova cena.
        """
        if scene_key == 'battle':
            # Cria uma nova instância da cena de batalha com os Pokémon selecionados
            player_pokemon = self.current_scene.selected_pokemon
            rival_pokemon = self.current_scene.rival_pokemon
            self.scenes['battle'] = BattleScene(player_pokemon, rival_pokemon)
            self.current_scene = self.scenes['battle']
        elif scene_key == 'selection':
            # Cria uma nova instância da cena de seleção para um novo jogo
            self.scenes['selection'] = SelectionScene()
            self.current_scene = self.scenes['selection']
        elif scene_key == 'quit':
            self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()