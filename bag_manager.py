# bag_manager.py

import json
import os
from typing import Dict, List, Any, Union, Optional

from pokemon import Pokemon
from api_client import APIClient

class BagManager:
    """
    Gerencia a bag (mochila) do jogador, incluindo Pokémon capturados,
    seleção para batalha e salvamento/carregamento do progresso da bag.

    Atributos:
        __bag_file (str): O nome do arquivo JSON onde os dados da bag são salvos/carregados.
        __api_client (APIClient): Uma instância do cliente da API para buscar dados de Pokémon.
    """
    def __init__(self) -> None:
        self.__bag_file: str = 'bag.json'
        self.__api_client: APIClient = APIClient()

    @property
    def bag_file(self) -> str:
        return self.__bag_file

    @bag_file.setter
    def bag_file(self, path: str) -> None:
        if not isinstance(path, str) or not path:
            raise ValueError("O 'bag_file' deve ser uma string não vazia.")
        self.__bag_file = path

    @property
    def api_client(self) -> APIClient:
        return self.__api_client

    @api_client.setter
    def api_client(self, client: APIClient) -> None:
        if not isinstance(client, APIClient):
            raise TypeError("O 'api_client' deve ser uma instância de APIClient.")
        self.__api_client = client

    def load_bag(self) -> Dict[str, Any]:
        """
        Carrega o conteúdo da bag do arquivo JSON.

        Returns:
            Dict[str, Any]: Um dicionário representando o estado da bag.
                            Retorna uma bag vazia se o arquivo não existir.
        """
        if os.path.exists(self.bag_file):
            try:
                with open(self.bag_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erro ao carregar bag: {e}. Retornando bag vazia.")
                return {"pokemons": [], "selected_for_battle": []}
        return {"pokemons": [], "selected_for_battle": []}

    def save_bag(self, bag: Dict[str, Any]) -> None:
        with open(self.bag_file, 'w', encoding='utf-8') as f:
            json.dump(bag, f, indent=2)


    def reset_bag(self) -> None:

        if os.path.exists(self.bag_file):
            os.remove(self.bag_file)

    def set_initial_pokemon(self, pokemon_name: str) -> None:
        self.reset_bag() 
        data: Optional[Dict[str, Any]] = self.api_client.fetch_pokemon_data(pokemon_name) 
        if not data:
            print(f"Erro ao buscar dados do Pokémon inicial {pokemon_name}")
            return

        # Lógica para obter a URL do sprite frontal, preferindo 'front_default' ou 'official-artwork'
        front_sprite: str = data["sprites"].get("front_default") or \
                            data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default", "")

        if not front_sprite:
            print(f" Sprite 'front_default' ausente para o Pokémon {pokemon_name}")

        poke: Pokemon = Pokemon(data["name"], 70, data)
        new_bag: Dict[str, Any] = {
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

    def add_pokemon_to_bag(self, pokemon_name: str, current_hp: Optional[int] = None) -> None:
        data: Optional[Dict[str, Any]] = self.api_client.fetch_pokemon_data(pokemon_name)
        if data:
            bag: Dict[str, Any] = self.load_bag()
            if any(p['name'].lower() == pokemon_name.lower() for p in bag["pokemons"]):
                print(f"{pokemon_name} já está na bag.")
                return


            front_sprite: str = data["sprites"].get("front_default") or \
                                data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default", "")


            if not front_sprite:
                print(f" Sprite 'front_default' ausente para o Pokémon {pokemon_name}")

            poke: Pokemon = Pokemon(data["name"], 70, data)
            entry: Dict[str, Any] = {
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

    def select_pokemon_for_battle(self, pokemon_name: str) -> None:
        bag: Dict[str, Any] = self.load_bag() 
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
        bag: Dict[str, Any] = self.load_bag() # Chama o método
        if pokemon_name in bag.get("selected_for_battle", []): # Acessa bag
            bag["selected_for_battle"].remove(pokemon_name) # Acessa bag
            self.save_bag(bag) # Chama o método
            print(f"{pokemon_name} foi removido da seleção de batalha.")
        else:
            print(f"{pokemon_name} não estava selecionado.")

    def get_selected_pokemons(self) -> List[Pokemon]:

        bag: Dict[str, Any] = self.load_bag() 
        selected_names: List[str] = bag.get("selected_for_battle", []) 
        pokemons_bag: List[Dict[str, Any]] = bag.get("pokemons", []) 
        pokemons: List[Pokemon] = []

        for selected_name in selected_names:
            match: Optional[Dict[str, Any]] = next((p for p in pokemons_bag if p["name"].lower() == selected_name.lower()), None)
            if match:
                data: Optional[Dict[str, Any]] = self.api_client.fetch_pokemon_data(match["name"]) 
                if data:
                    poke: Pokemon = Pokemon(match["name"], 70, data)
                    poke._current_hp = match.get("current_hp", poke._current_hp) 
                    pokemons.append(poke)
        return pokemons


    def get_first_selected_pokemon_object(self) -> Optional[Pokemon]:

        bag: Dict[str, Any] = self.load_bag() 
        selected: List[Union[str, Dict[str, Any]]] = bag.get("selected_for_battle", []) 
        if not selected:
            return None

        name: str = selected[0]
        if isinstance(name, dict) and "name" in name:
            name = name["name"]
        elif not isinstance(name, str):
            raise ValueError("Elemento inesperado em selected_for_battle: esperada string")

        data: Optional[Dict[str, Any]] = self.api_client.fetch_pokemon_data(name) 
        return Pokemon(name, 50, data) if data else None

    def get_all_pokemon_names_in_bag(self) -> List[str]:
        bag: Dict[str, Any] = self.load_bag()
        return [p["name"] for p in bag.get("pokemons", [])]

    def atualizar_hp_bag(self, pokemon_name: str, novo_hp: int) -> None:
        bag: Dict[str, Any] = self.load_bag() 
        for p in bag.get("pokemons", []): 
            if p["name"].lower() == pokemon_name.lower(): 
                p["current_hp"] = novo_hp 
        self.save_bag(bag)

    def curar_todos_pokemons(self) -> None:
        bag: Dict[str, Any] = self.load_bag() 
        for p in bag.get("pokemons", []): 
            data: Optional[Dict[str, Any]] = self.api_client.fetch_pokemon_data(p["name"])
            if data:
                poke: Pokemon = Pokemon(p["name"], 70, data)
                p["current_hp"] = poke.get_current_hp() 
        self.save_bag(bag) 