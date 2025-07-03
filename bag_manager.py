import json
import os
from pokemon import Pokemon
from api_client import APIClient

class BagManager:
    def __init__(self):
        self._bag_file = 'bag.json'
        self._api_client = APIClient()

    @property
    def bag_file(self):
        return self._bag_file

    @bag_file.setter
    def bag_file(self, path):
        self._bag_file = path

    @property
    def api_client(self):
        return self._api_client

    @api_client.setter
    def api_client(self, client):
        self._api_client = client

    def load_bag(self):
        if os.path.exists(self._bag_file):
            with open(self._bag_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"pokemons": [], "selected_for_battle": []}

    def save_bag(self, bag):
        with open(self._bag_file, 'w', encoding='utf-8') as f:
            json.dump(bag, f, indent=2)

    def reset_bag(self):
        if os.path.exists(self._bag_file):
            os.remove(self._bag_file)

    def set_initial_pokemon(self, pokemon_name):
        self.reset_bag()
        data = self._api_client.fetch_pokemon_data(pokemon_name)
        if not data:
            print(f"Erro ao buscar dados do Pokémon inicial {pokemon_name}")
            return

        front_sprite = data["sprites"].get("front_default") or \
                    data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default", "")

        if not front_sprite:
            print(f"⚠️ Sprite 'front_default' ausente para o Pokémon {pokemon_name}")

        poke = Pokemon(data["name"], 70, data)
        new_bag = {
            "pokemons": [{
                "name": data["name"],
                "id": data["id"],
                "sprites": {"front_default": front_sprite},
                "current_hp": poke.get_current_hp()
            }],
            "selected_for_battle": [data["name"]]
        }
        self.save_bag(new_bag)
        print(f"Pokémon inicial {pokemon_name} setado na bag e selecionado para batalha.")

    def add_pokemon_to_bag(self, pokemon_name, current_hp=None):
        data = self._api_client.fetch_pokemon_data(pokemon_name)
        if data:
            bag = self.load_bag()
            if any(p['name'].lower() == pokemon_name.lower() for p in bag["pokemons"]):
                print(f"{pokemon_name} já está na bag.")
                return

            front_sprite = data["sprites"].get("front_default") or \
                        data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default", "")

            if not front_sprite:
                print(f"⚠️ Sprite 'front_default' ausente para o Pokémon {pokemon_name}")

            poke = Pokemon(data["name"], 70, data)
            entry = {
                "name": data["name"],
                "id": data["id"],
                "sprites": {"front_default": front_sprite},
                "current_hp": current_hp if current_hp is not None else poke.get_current_hp()
            }
            bag["pokemons"].append(entry)
            self.save_bag(bag)
            print(f"{pokemon_name} adicionado à bag.")
        else:
            print(f"Falha ao buscar dados do Pokémon '{pokemon_name}' da API.")

    def select_pokemon_for_battle(self, pokemon_name):
        bag = self.load_bag()
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
        self.save_bag(bag)
        print(f"{pokemon_name} selecionado para batalha.")

    def deselect_pokemon(self, pokemon_name):
        bag = self.load_bag()
        if pokemon_name in bag.get("selected_for_battle", []):
            bag["selected_for_battle"].remove(pokemon_name)
            self.save_bag(bag)
            print(f"{pokemon_name} foi removido da seleção de batalha.")
        else:
            print(f"{pokemon_name} não estava selecionado.")

    def get_selected_pokemons(self):
        bag = self.load_bag()
        selected_names = bag.get("selected_for_battle", [])
        pokemons_bag = bag.get("pokemons", [])
        pokemons = []

        for selected_name in selected_names:
            match = next((p for p in pokemons_bag if p["name"].lower() == selected_name.lower()), None)
            if match:
                data = self._api_client.fetch_pokemon_data(match["name"])
                if data:
                    poke = Pokemon(match["name"], 70, data)
                    poke._current_hp = match.get("current_hp", poke._current_hp)
                    pokemons.append(poke)
        return pokemons

    def get_first_selected_pokemon_object(self):
        bag = self.load_bag()
        selected = bag.get("selected_for_battle", [])
        if not selected:
            return None

        name = selected[0]
        if isinstance(name, dict) and "name" in name:
            name = name["name"]
        elif not isinstance(name, str):
            raise ValueError("Elemento inesperado em selected_for_battle: esperada string")

        data = self._api_client.fetch_pokemon_data(name)
        return Pokemon(name, 50, data) if data else None

    def get_all_pokemon_names_in_bag(self):
        bag = self.load_bag()
        return [p["name"] for p in bag.get("pokemons", [])]

    def atualizar_hp_bag(self, pokemon_name, novo_hp):
        bag = self.load_bag()
        for p in bag.get("pokemons", []):
            if p["name"].lower() == pokemon_name.lower():
                p["current_hp"] = novo_hp
        self.save_bag(bag)

    def curar_todos_pokemons(self):
        bag = self.load_bag()
        for p in bag.get("pokemons", []):
            data = self._api_client.fetch_pokemon_data(p["name"])
            if data:
                poke = Pokemon(p["name"], 70, data)
                p["current_hp"] = poke.get_current_hp()
        self.save_bag(bag)