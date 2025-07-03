import requests
from typing import Optional


class APIClient:
    """
    Cliente para acessar dados da PokeAPI.
    """

    def __init__(self, base_url: str = 'https://pokeapi.co/api/v2'):
        self.__base_url = base_url
        self.__session = requests.Session()
        
        # Getters e setters para a base_url, caso precise modificar externamente
    @property
    def base_url(self) -> str:
        return self.__base_url

    @base_url.setter
    def base_url(self, new_url: str):
        if not new_url.startswith('http'):
            raise ValueError("A nova base URL deve começar com http ou https")
        self.__base_url = new_url

    @property
    def session(self) -> requests.Session:
        return self.__session

    @session.setter
    def session(self, new_session: requests.Session):
        if not isinstance(new_session, requests.Session):
            raise ValueError("A nova sessão deve ser uma instância de requests.Session")
        self.__session = new_session

    def fetch_pokemon_data(self, name: str) -> Optional[dict]:
        """
        Busca os dados de um Pokémon pelo nome.
        """
        try:
            url = f'{self.__base_url}/pokemon/{name.lower()}'
            response = self.__session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERRO] Erro ao buscar dados do Pokémon '{name}': {e}")
            return None

    def fetch_move_data(self, url: str) -> Optional[dict]:
        """
        Busca os dados de um movimento pelo URL completo.
        """
        try:
            response = self.__session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERRO] Erro ao buscar dados do movimento: {e}")
            return None

    def close(self):
        """
        Encerra a sessão HTTP.
        """
        self.__session.close()


