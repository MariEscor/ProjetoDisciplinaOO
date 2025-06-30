import requests

BASE_URL = 'https://pokeapi.co/api/v2'

def fetch_pokemon_data(name: str) -> dict | None:
    """
    Busca os dados de um Pokémon na PokeAPI.
    Retorna um dicionário com os dados ou None em caso de erro.
    """
    try:
        req = requests.get(f'{BASE_URL}/pokemon/{name.lower()}')
        req.raise_for_status()  # Lança uma exceção para erros HTTP (4xx ou 5xx)
        return req.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados para {name}: {e}")
        return None

def fetch_move_data(url: str) -> dict | None:
    """
    Busca os dados de um movimento (move) na PokeAPI.
    Retorna um dicionário com os dados ou None em caso de erro.
    """
    try:
        req = requests.get(url)
        req.raise_for_status()
        return req.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados do movimento em {url}: {e}")
        return None