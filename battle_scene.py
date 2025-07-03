#battle_scene.py

import pygame
import time
import random
import math
import constants
import sys
from ui import UI
from game_scene import GameScene
from pokemon import Pokemon
from pokemon_sprite import PokemonSprite
from bag_manager import BagManager
from battle_context import player_team
from bases.game_data import TRAINER_DATA


class BattleScene(GameScene):
    """
    Cena que gerencia toda a lógica e a apresentação de uma batalha Pokémon.
    """
    def __init__(self, player_team: list[Pokemon], rival_team: list[Pokemon]):
        super().__init__()
        self.player_team = player_team
        self.current_index = 0
        self.player_pokemon = self.player_team[self.current_index]
        self.rival_team = rival_team
        self.rival_index = 0
        self.rival_pokemon = self.rival_team[self.rival_index]
        self.battle_result = None
        self.next_scene = None
        self._ui = UI()
        self._bag_manager = BagManager()        
        try:
            self.background_img = pygame.image.load(constants.BATTLE_BACKGROUND_PATH).convert()
            self.background_img = pygame.transform.scale(self.background_img, (constants.LARGURA_JANELA, constants.ALTURA_JANELA))
        except pygame.error:
            self.background_img = pygame.Surface((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
            self.background_img.fill(constants.GREEN_GREY)

        self._setup_sprites()
        self.state = 'intro' 
        self.message = f"Vá {self.player_pokemon.name}!"
        self.buttons = []
    # --- MÉTODO CORRIGIDO PARA REPLICAR POSICIONAMENTO ORIGINAL ---
    def _setup_sprites(self) -> None:
        """
        Cria e posiciona os sprites para a batalha, usando a lógica do script original.
        """
        # Cria os objetos Sprite
        self.player_sprite = PokemonSprite(self.player_pokemon, 'back_default', size=450)
        self.rival_sprite = PokemonSprite(self.rival_pokemon, 'front_default', size=400)

        # Lógica de posicionamento do Pokémon do jogador (player)
        player_ground_y = constants.ALTURA_JANELA - constants.UI_AREA_HEIGHT + 130
        player_x = 170
        player_y = player_ground_y - self.player_sprite.rect.height
        self.player_sprite.rect.topleft = (player_x, player_y)

        # Lógica de posicionamento do Pokémon do rival
        rival_ground_y = (constants.ALTURA_JANELA // 2) + 40  # Original: altura_janela // 2 - (-40)
        rival_x = constants.LARGURA_JANELA - self.rival_sprite.rect.width - 160
        rival_y = rival_ground_y - self.rival_sprite.rect.height
        self.rival_sprite.rect.topleft = (rival_x, rival_y)

        # Adiciona os sprites ao grupo para desenho
        self.all_sprites = pygame.sprite.Group(self.player_sprite, self.rival_sprite)


    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Processa todos os eventos de input para a cena de batalha.
        """
        for event in events:
            if self.state in ['player_turn', 'player_move']:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, action, data in self.buttons:
                        if button_rect.collidepoint(event.pos):
                            action(data)
                            break 

    def update(self) -> None:
        """
        Atualiza a lógica da batalha a cada frame.
        """
        if self.state == 'intro':
            if self.rival_pokemon.speed > self.player_pokemon.speed:
                self.state = 'rival_turn'
            else:
                self.state = 'player_turn'
            self.message = f"O que {self.player_pokemon.name} fará?"

        elif self.state == 'rival_turn':
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(2)
            self._execute_rival_turn()

        if self.rival_pokemon.is_fainted():
            self.rival_index += 1
            if self.rival_index < len(self.rival_team):
                self.rival_pokemon = self.rival_team[self.rival_index]
                self._setup_sprites()
                self.message = f"{self.rival_pokemon.name} entrou na batalha!"
                self.draw(pygame.display.get_surface())
                pygame.display.flip()
                time.sleep(2)
                self.state = 'player_turn'
            else:
                if self.state != 'game_over':
                    self.message = f"Todos os Pokémon do treinador foram derrotados!"
                    self.draw(pygame.display.get_surface())
                    pygame.display.flip()
                    self.game_over_time = pygame.time.get_ticks()
                    self.state = 'game_over'
                    self.battle_result = "win"

        elif self.player_pokemon.is_fainted():
            self.current_index += 1
            if self.current_index < len(self.player_team):
                self.player_pokemon = self.player_team[self.current_index]
                self.message = f"{self.player_pokemon.name}, eu escolho você!"
                self._setup_sprites()
                self.draw(pygame.display.get_surface())
                pygame.display.flip()
                time.sleep(2)
                self.state = 'player_turn'
            else:
                if self.state != 'game_over':
                    self.message = f"Todos os seus Pokémon foram derrotados!"
                    self.draw(pygame.display.get_surface())
                    pygame.display.flip()
                    self.game_over_time = pygame.time.get_ticks()
                    self.state = 'game_over'
                    self.battle_result = "lose"

        if self.state == 'game_over' and self.game_over_time is not None:
            if pygame.time.get_ticks() - self.game_over_time > 2000:
                for p in self.player_team:
                    self._bag_manager.atualizar_hp_bag(p.name, p.get_current_hp())
                if self.battle_result == "lose":
                    self._bag_manager.curar_todos_pokemons()
                    self.next_scene = 'hospital'
                else:
                    self.next_scene = 'mundo_aberto'


    def _execute_rival_turn(self):
        if not self.rival_pokemon.is_fainted():
            self.message = f"{self.rival_pokemon.name} está pensando..."
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(2)

            if self.rival_pokemon.moves:  # verifica se tem algum movimento
                move = random.choice(self.rival_pokemon.moves)
                self._perform_attack(self.rival_pokemon, self.player_pokemon, move)
            else:
                self.message = f"{self.rival_pokemon.name} nao tem movimentos!"
                self.draw(pygame.display.get_surface())
                pygame.display.flip()
                time.sleep(2)

            if not self.player_pokemon.is_fainted():
                self.state = 'player_turn'
                self.message = f"O que {self.player_pokemon.name} fará?"

    def _perform_attack(self, attacker: Pokemon, target: Pokemon, move) -> None:
        """Calcula e aplica o dano de um ataque."""
        self.message = f"{attacker.name} usou {move.name.capitalize()}!"
        self.draw(pygame.display.get_surface()); pygame.display.flip(); time.sleep(1)
        
        power = move.power if move.power else 0
        damage = math.floor((((2 * attacker.level / 5 + 2) * power * attacker.attack / target.defense) / 50) + 2)

        if random.random() <= 0.0625:
            damage = math.floor(damage * 1.5)
            self.message = "Ataque crítico!"
            self.draw(pygame.display.get_surface()); pygame.display.flip(); time.sleep(1)

        target.take_damage(damage)
        
    def _action_select_move(self, move):
        self._perform_attack(self.player_pokemon, self.rival_pokemon, move)
        if not self.rival_pokemon.is_fainted():
            self.state = 'rival_turn'
        
    def _action_use_potion(self, _):
        if self.player_pokemon.num_potions > 0:
            self.player_pokemon.use_potion()
            self.message = f"{self.player_pokemon.name} usou poçao!"
        else:
            self.message = 'Sem mais poções sobrando!'
        
        self.draw(pygame.display.get_surface()); pygame.display.flip(); time.sleep(2)
        if self.state != 'game_over':
            self.state = 'rival_turn'
        
    def _action_show_moves(self, _):
        self.state = 'player_move'

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background_img, (0, 0))
        self.all_sprites.draw(screen)
        
        self._ui.draw_pokemon_hp(screen, self.player_pokemon, 'player')
        self._ui.draw_pokemon_hp(screen, self.rival_pokemon, 'rival')

        final_message = self.message

        self._ui.draw_message_box(screen, final_message)

        self.buttons.clear()
        if self.state == 'player_turn':
            button_width = (constants.LARGURA_JANELA - 200) // 2
            button_height = 45
            total_buttons_width = (button_width * 2) + 40
            start_x = (constants.LARGURA_JANELA - total_buttons_width) // 2
            start_y = constants.UI_AREA_Y + 110

            labels_and_actions = [
                ("Lutar", self._action_show_moves),
                (f"Usar Poçao({self.player_pokemon.num_potions})", self._action_use_potion),
                ("Capturar", self._action_capture_pokemon),
                ("Fugir", self._action_flee_battle)
            ]

            for i, (label, action) in enumerate(labels_and_actions):
                left = start_x + (i % 2) * (button_width + 40)
                top = start_y + (i // 2) * (button_height + 10)
                rect = pygame.Rect(left, top, button_width, button_height)
                self._ui.draw_button(screen, rect, label)
                self.buttons.append((rect, action, None))


            
        elif self.state == 'player_move':
            move_button_width = (constants.LARGURA_JANELA - 200) // 2
            move_button_height = 45
            total_buttons_width = (move_button_width * 2) + 40 
            start_x = (constants.LARGURA_JANELA - total_buttons_width) // 2 
            start_y = constants.UI_AREA_Y + 110

            for i, move in enumerate(self.player_pokemon.moves):
                left = start_x + (i % 2) * (move_button_width + 40)
                top = start_y + (i // 2) * (move_button_height + 10)
                move_rect = pygame.Rect(left, top, move_button_width, move_button_height)
                
                self._ui.draw_button(screen, move_rect, move.name.capitalize())
                self.buttons.append((move_rect, self._action_select_move, move))
                
    def _action_capture_pokemon(self, _):
        if self.rival_pokemon.is_fainted():
            self.message = "Nao pode capturar Pokémon derrotado!"
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(1.5)
            return

        # Simples lógica de captura: chance base 30% + chance extra se o rival estiver com pouco HP
        hp_ratio = self.rival_pokemon.get_hp_ratio()
        capture_chance = 1 + (1 - hp_ratio) * 0.5  # até 80% chance se muito ferido

        if random.random() < capture_chance:
            self.message = f"Você capturou {self.rival_pokemon.name}!"
            # Aqui adicione lógica para colocar o Pokémon na bag do jogador
            self._bag_manager.add_pokemon_to_bag(self.rival_pokemon.name, self.rival_pokemon.get_current_hp())
            
            for p in self.player_team:
                self._bag_manager.atualizar_hp_bag(p.name, p.get_current_hp())
                
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(2)
            self.state = 'game_over'
            self.game_over_time = pygame.time.get_ticks()
            self.next_scene = 'mundo_aberto'
        else:
            self.message = f"{self.rival_pokemon.name} escapou da Pokébola!"
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(1.5)
            self.state = 'rival_turn'

    def _action_flee_battle(self, _):
        # Chance simples de fuga: 50%
        if random.random() < 0.5:
            self.message = "Fugiu da batalha com sucesso!"
            
            for p in self.player_team:
                self._bag_manager.atualizar_hp_bag(p.name, p.get_current_hp())
                
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(1.5)
            self.state = 'game_over'
            self.game_over_time = pygame.time.get_ticks()
            self.next_scene = 'mundo_aberto'
        else:
            self.message = "Nao conseguiu fugir!"
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
            time.sleep(1.5)
            self.state = 'rival_turn'

def run_battle(player_team, rival_team):
    pygame.mixer.music.stop()  # Para qualquer música atual
    pygame.mixer.music.load("assets/sounds/battle.ogg")
    pygame.mixer.music.set_volume(0.5)  # Ajuste como quiser
    pygame.mixer.music.play(loops=-1)

    cena = BattleScene(player_team, rival_team)
    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        cena.handle_events(events)
        cena.update()
        cena.draw(pygame.display.get_surface())
        pygame.display.flip()
        clock.tick(60)

        # Caso sua classe BattleScene defina o atributo next_scene para indicar
        # que a batalha terminou e qual próxima cena carregar:
        if hasattr(cena, 'next_scene') and cena.next_scene:
            from bases.player_state import player_state
            if player_state.get("pos"):
                player_state["pos"] = None
                player_state["direction"] = "down"
                player_state["map"] = "mundo"
            return cena.next_scene
