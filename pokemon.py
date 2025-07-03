import random
from move import Move

class Pokemon:
    """
    Representa os dados e a lógica de um Pokémon, sem se preocupar com a parte visual.
    """
    def __init__(self, name: str, level: int, data: dict) -> None:
        self.name = name.capitalize()
        self.level = level
        self._json_data = data
        
        # Atributos privados para melhor encapsulamento
        self._current_hp = 0
        self._max_hp = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.num_potions = 3
        
        self._parse_stats()
        self.moves = self._get_moves()
        self.types = [t['type']['name'] for t in self._json_data['types']]

    def _parse_stats(self) -> None:
        """
        Extrai os status do JSON da API.
        """
        stats = self._json_data['stats']
        for stat in stats:
            stat_name = stat['stat']['name']
            if stat_name == 'hp':
                self._max_hp = stat['base_stat'] + self.level
                self._current_hp = self._max_hp
            elif stat_name == 'attack':
                self.attack = stat['base_stat']
            elif stat_name == 'defense':
                self.defense = stat['base_stat']
            elif stat_name == 'speed':
                self.speed = stat['base_stat']
    
    def _get_moves(self) -> list[Move]:
        """
        Filtra e seleciona até 4 movimentos para o Pokémon.
        """
        available_moves = []
        for move_info in self._json_data['moves']:
            # Lógica para filtrar movimentos (ex: apenas de 'red-blue' por level-up)
            for version in move_info['version_group_details']:
                if (version['version_group']['name'] == 'ultra-sun-ultra-moon' and 
                    version['move_learn_method']['name'] == 'level-up' and
                    self.level >= version['level_learned_at']):
                    
                    move = Move(move_info['move']['url'])
                    # Adiciona apenas movimentos que causam dano
                    if move.power is not None and move.power > 0:
                        available_moves.append(move)
                        
        if len(available_moves) > 4:
            return random.sample(available_moves, 4)
        return available_moves

    def take_damage(self, damage: int) -> None:
        self._current_hp -= damage
        if self._current_hp < 0:
            self._current_hp = 0

    def use_potion(self) -> bool:
        if self.num_potions > 0:
            self.num_potions -= 1
            self._current_hp += 30
            if self._current_hp > self._max_hp:
                self._current_hp = self._max_hp
            return True
        return False

    def get_hp_ratio(self) -> float:
        return self._current_hp / self._max_hp

    def get_current_hp(self) -> int:
        return self._current_hp

    def get_max_hp(self) -> int:
        return self._max_hp

    def is_fainted(self) -> bool:
        return self._current_hp == 0
    
    def get_sprite_url(self, side: str) -> str:
        """Retorna a URL do sprite ('front_default' ou 'back_default')."""
        return self._json_data['sprites'][side]