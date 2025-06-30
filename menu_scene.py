import pygame
import constants
import ui
from game_scene import GameScene
from trainers import TRAINER_DATA

class MenuScene(GameScene):
    """
    A tela inicial do jogo, onde o jogador escolhe qual ginásio enfrentar.
    """
    def __init__(self):
        super().__init__()
        self.buttons = []
        
        # Cria um botão para cada treinador definido em TRAINER_DATA
        for i, battle_id in enumerate(TRAINER_DATA.keys()):
            # O 'data' do botão será o ID da batalha ('water', 'fire', etc.)
            self.buttons.append({
                'label': f"Ginásio de {battle_id.capitalize()}",
                'battle_id': battle_id,
                'index': i
            })

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # A lógica de clique agora é baseada nos retângulos gerados no 'draw'
                for button_info in self.buttons:
                    if button_info['rect'].collidepoint(event.pos):
                        # Sinaliza para mudar para a SelectionScene, passando o ID da batalha
                        self.next_scene = ('selection', {'battle_id': button_info['battle_id']})
                        break

    def update(self) -> None:
        pass # O menu não tem lógica de atualização contínua

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(constants.WHITE)
        ui.draw_text(screen, 'Escolha seu Desafio!', 48, constants.BLACK, (constants.LARGURA_JANELA // 2, 100))
        
        # Desenha os botões e armazena seus retângulos para a detecção de clique
        button_width = 400
        button_height = 60
        start_y = 200
        
        for button_info in self.buttons:
            left = (constants.LARGURA_JANELA - button_width) // 2
            top = start_y + button_info['index'] * (button_height + 20)
            rect = pygame.Rect(left, top, button_width, button_height)
            
            ui.draw_button(screen, rect, button_info['label'])
            button_info['rect'] = rect # Armazena o rect para uso no handle_events