# scene_manager.py
import sys
from bag_manager import BagManager

class SceneManager:
    def __init__(self):
        self._bag_manager = BagManager()

    def load_scene(self, name):
        if name == "menu":
            from menu_manager import MenuManager
            MenuManager().run_game()
        elif name == "selection":
            from selection_scene import SelectionScene
            SelectionScene.run_selection()
        elif name == "mundo_aberto":
            from inicia_mundo import main
            main(start_scene="mundo_aberto")
            self.load_scene("menu")
        elif name == "hospital":
            from inicia_mundo import main
            main(start_scene="hospital")
            self.load_scene("menu")
        elif name == "name_input":
            from name_input_scene import NameInputScene
            NameInputScene().run()
        elif name == "leaderboard":
            from bases.leaderboard_scene import LeaderboardScene
            LeaderboardScene().run()
        elif name == "dinamica":
            from inicia_mundo import main
            main()
        elif name == "battle":
            from battle_scene import BattleScene
            import battle_context

            player_pokemon = self._bag_manager.get_first_selected_pokemon_object()
            rival_pokemon = battle_context.rival_pokemon

            if not player_pokemon:
                print("Nenhum Pokémon foi selecionado na bag!")
                from message_scene import MessageScene
                MessageScene().show_message("Selecione pelo menos um Pokémon na bag para batalhar.")
                self.load_scene("mundo_aberto")
                return

            if rival_pokemon:
                next_scene = BattleScene.run_battle(player_pokemon, rival_pokemon)
                if next_scene:
                    self.load_scene(next_scene)
            else:
                print("Erro: Pokémon rival não definido.")
                sys.exit(1)
        else:
            print(f"Unknown scene: {name}")
            sys.exit(1)
