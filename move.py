from api_client import APIClient

class Move:
    """
    Representa os dados de um movimento (ataque) de um Pokémon.
    """
    def __init__(self, url: str) -> None:
        self._api_client = APIClient()
        json_data = self._api_client.fetch_move_data(url)
        
        if json_data:
            self.name = json_data.get('name', 'unknown')
            self.power = json_data.get('power')
            type_info = json_data.get('type', {})
            self.type = type_info.get('name', 'normal')
        else:
            self.name = "Struggle"
            self.power = 50
            self.type = "normal"
            
    