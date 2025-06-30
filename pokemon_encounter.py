import random
from api_client import fetch_pokemon_data
from pokemon import Pokemon
from bag_manager import get_all_pokemon_names_in_bag

# Pokémon da 1ª geração por tipo
POKEMONS_ENCONTRAVEIS = [
        "bulbasaur", "ivysaur", "venusaur", "oddish", "gloom",
        "vileplume", "bellsprout", "weepinbell", "victreebel", "exeggcute",
        "charmander", "charmeleon", "charizard", "vulpix", "ninetales",
        "growlithe", "arcanine", "ponyta", "rapidash", "magmar",
        "squirtle", "wartortle", "blastoise", "psyduck", "golduck",
        "poliwag", "poliwhirl", "poliwrath", "tentacool", "tentacruel",
        "pikachu", "raichu", "magnemite", "magneton", "voltorb",
        "electrode", "electabuzz", "jolteon", "zapdos", "pichu",
        "gastly", "haunter", "gengar", "cubone", "marowak",
        "misdreavus", "mimikyu", "banette", "dusclops", "shedinja"  # vários aqui são de outras gerações
]

def gerar_pokemon_encontro():
    """
    Gera um Pokémon aleatório que não esteja na bag.
    """
    bag = get_all_pokemon_names_in_bag()

    # Filtra os que ainda não estão na bag
    candidatos = [p for p in POKEMONS_ENCONTRAVEIS if p not in bag]

    if not candidatos:
        print("Todos os Pokémon já estão na bag.")
        return None

    nome = random.choice(candidatos)
    data = fetch_pokemon_data(nome)

    if data:
        level = 70
        return Pokemon(nome, level, data)

    return None
