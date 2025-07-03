import random
from api_client import APIClient
from pokemon import Pokemon
from bag_manager import BagManager

# Pokémon da 1ª geração por tipo
POKEMONS_ENCONTRAVEIS = [
        "sceptile", "leafeon", "venusaur", "exeggutor", "roserade",
        "amoonguss", "abomasnow", "parasect", "ludicolo", "celebi",

        "charizard", "typhlosion", "houndoom", "chandelure", "ninetales",
        "blaziken", "arcanine", "flareon", "rapidash", "entei",

        "gyarados", "feraligatr", "blastoise", "psyduck", "vaporeon",
        "swampert", "greninja", "poliwrath", "tentacruel", "suicune",

        "pikachu", "manectric", "luxray", "magnezone", "ampharos",
        "rotom", "galvantula", "jolteon", "zebstrika", "raikou",

        "shedinja", "spiritomb", "gengar", "aegislash", "sableye",
        "misdreavus", "mimikyu", "banette", "dusclops", "lunala"
]

def gerar_pokemon_encontro():
    """
    Gera um Pokémon aleatório que não esteja na bag.
    """
    bag = BagManager().get_all_pokemon_names_in_bag()

    # Filtra os que ainda não estão na bag
    candidatos = [p for p in POKEMONS_ENCONTRAVEIS if p not in bag]

    if not candidatos:
        print("Todos os Pokémon já estão na bag.")
        return None

    nome = random.choice(candidatos)
    data = APIClient().fetch_pokemon_data(nome)

    if data:
        level = 70
        return Pokemon(nome, level, data)

    return None
