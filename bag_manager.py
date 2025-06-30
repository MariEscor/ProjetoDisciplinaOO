import json
import os
import api_client
from pokemon import Pokemon

BAG_FILE = 'bag.json'

def load_bag():
    if os.path.exists(BAG_FILE):
        with open(BAG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "pokemons": [],
            "selected_for_battle": []
        }

def save_bag(bag):
    with open(BAG_FILE, 'w', encoding='utf-8') as f:
        json.dump(bag, f, indent=2)

def reset_bag():
    if os.path.exists(BAG_FILE):
        os.remove(BAG_FILE)

def set_initial_pokemon(pokemon_name):
    """
    Reseta a bag e adiciona o Pokémon inicial, já selecionado para batalha.
    """
    reset_bag()
    data = api_client.fetch_pokemon_data(pokemon_name)
    if not data:
        print(f"Erro ao buscar dados do Pokémon inicial {pokemon_name}")
        return

    # Verifica e corrige o sprite
    front_sprite = data["sprites"].get("front_default")
    if not front_sprite:
        front_sprite = data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default")

    if not front_sprite:
        print(f"⚠️ Sprite 'front_default' ausente para o Pokémon {pokemon_name}")
        front_sprite = ""

    poke = Pokemon(data["name"], 70, data)
    new_bag = {
        "pokemons": [{
            "name": data["name"],
            "id": data["id"],
            "sprites": {
                "front_default": front_sprite
            },
            "current_hp": poke.get_current_hp()  # <-- Isso que estava faltando
        }],
        "selected_for_battle": [data["name"]]
    }


    save_bag(new_bag)
    print(f"Pokémon inicial {pokemon_name} setado na bag e selecionado para batalha.")

def add_pokemon_to_bag(pokemon_name, current_hp=None):
    """
    Adiciona um Pokémon à bag sem alterar a seleção de batalha.
    """
    data = api_client.fetch_pokemon_data(pokemon_name)
    if data:
        bag = load_bag()

        if any(p['name'].lower() == pokemon_name.lower() for p in bag["pokemons"]):
            print(f"{pokemon_name} já está na bag.")
            return

        # Tenta obter o sprite padrão
        front_sprite = data["sprites"].get("front_default")

        # Se não tiver, tenta outro (por exemplo, artwork oficial)
        if not front_sprite:
            front_sprite = data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default")

        if not front_sprite:
            print(f"⚠️ Sprite 'front_default' ausente para o Pokémon {pokemon_name}")
            front_sprite = ""  # Ou sprite de fallback (ex: URL de uma imagem padrão sua)

        poke = Pokemon(data["name"], 70, data)
        entry = {
            "name": data["name"],
            "id": data["id"],
            "sprites": {
                "front_default": front_sprite
            },
            "current_hp": current_hp if current_hp is not None else poke.get_current_hp()
        }



        bag["pokemons"].append(entry)
        save_bag(bag)
        print(f"{pokemon_name} adicionado à bag.")
    else:
        print(f"Falha ao buscar dados do Pokémon '{pokemon_name}' da API.")


def select_pokemon_for_battle(pokemon_name):
    bag = load_bag()

    if "selected_for_battle" not in bag:
        bag["selected_for_battle"] = []

    if pokemon_name not in [p["name"] for p in bag["pokemons"]]:
        print(f"{pokemon_name} não está na bag.")
        return

    if pokemon_name in bag["selected_for_battle"]:
        print(f"{pokemon_name} já está selecionado.")
        return

    if len(bag["selected_for_battle"]) >= 3:
        print("Você já selecionou 3 Pokémon para batalha.")
        return

    bag["selected_for_battle"].append(pokemon_name)
    save_bag(bag)
    print(f"{pokemon_name} selecionado para batalha.")

def deselect_pokemon(pokemon_name):
    bag = load_bag()
    if "selected_for_battle" not in bag:
        bag["selected_for_battle"] = []

    if pokemon_name in bag["selected_for_battle"]:
        bag["selected_for_battle"].remove(pokemon_name)
        save_bag(bag)
        print(f"{pokemon_name} foi removido da seleção de batalha.")
    else:
        print(f"{pokemon_name} não estava selecionado.")

def get_selected_pokemons():
    bag = load_bag()
    selected_names = bag.get("selected_for_battle", [])
    pokemons_bag = bag.get("pokemons", [])
    pokemons = []

    for selected_name in selected_names:
        match = next((p for p in pokemons_bag if p["name"].lower() == selected_name.lower()), None)
        if match:
            data = api_client.fetch_pokemon_data(match["name"])
            if data:
                poke = Pokemon(match["name"], 70, data)
                if "current_hp" in match:
                    poke._current_hp = match["current_hp"]
                pokemons.append(poke)
    return pokemons


def get_first_selected_pokemon_object():
    bag = load_bag()
    selected = bag.get("selected_for_battle", [])
    if not selected:
        return None

    name = selected[0]
    if isinstance(name, dict) and "name" in name:
        name = name["name"]
    elif not isinstance(name, str):
        raise ValueError("Elemento inesperado em selected_for_battle: esperada string")

    data = api_client.fetch_pokemon_data(name)
    return Pokemon(name, 50, data)

def get_all_pokemon_names_in_bag():
    bag = load_bag()
    return [p["name"] for p in bag.get("pokemons", [])]

def atualizar_hp_bag(pokemon_name, novo_hp):
    bag = load_bag()
    for p in bag.get("pokemons", []):
        if p["name"].lower() == pokemon_name.lower():
            p["current_hp"] = novo_hp
    save_bag(bag)

def curar_todos_pokemons():
    bag = load_bag()
    for p in bag.get("pokemons", []):
        data = api_client.fetch_pokemon_data(p["name"])
        if data:
            poke = Pokemon(p["name"], 70, data)
            p["current_hp"] = poke.get_current_hp()  # HP cheio
    save_bag(bag)


