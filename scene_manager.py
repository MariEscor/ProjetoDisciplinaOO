import sys
from bag_manager import get_first_selected_pokemon_object

def load_scene(name):
    if name == "menu":
        from menu import main_menu
        main_menu()
    elif name == "selection":
        from selection_scene import run_selection
        run_selection()
    elif name == "mundo_aberto":
        from mainproj import main
        main(start_scene="mundo_aberto")  # passa o nome como start_scene
        load_scene("menu")  # depois que o jogo termina, volta ao menu

    elif name == "hospital":  # aceitar ambos
        from mainproj import main
        main(start_scene="hospital")  # passa o nome como start_scene
        load_scene("menu")  # depois que o jogo termina, volta ao menu
        
    elif name  == "dinamica":
        from mainproj import main
        main()
    elif name == "battle":
        from battle_scene import run_battle
        import battle_context
        from bag_manager import get_first_selected_pokemon_object

        player_pokemon = get_first_selected_pokemon_object()
        rival_pokemon = battle_context.rival_pokemon

        if not player_pokemon:
            print("Nenhum Pokémon foi selecionado na bag!")
            from message_scene import show_message_scene
            show_message_scene("Selecione pelo menos um Pokémon na bag para batalhar.")
            load_scene("mundo_aberto")  # volta para o mapa
            return

        if rival_pokemon:
            next_scene = run_battle(player_pokemon, rival_pokemon)
            if next_scene:
                load_scene(next_scene)
        else:
            print("Erro: Pokémon rival não definido.")
            sys.exit(1)

    else:
        print(f"Unknown scene: {name}")
        sys.exit(1)
