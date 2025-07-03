import json
import os
from bases.game_data import TRAINER_DATA
from bases.timer import get_ticks, game_start_time

class SaveManager:
    def __init__(self, save_file="save.json"):
        self._save_file = save_file

    @property
    def save_file(self):
        return self._save_file

    @save_file.setter
    def save_file(self, value):
        self._save_file = value

    def save_progress(self):
        """
        Salva o progresso atual: bosses derrotados e tempo.
        """
        bosses_defeated = [key for key, value in TRAINER_DATA.items() if value.get("defeated", False) and key != 'Nurse']

        elapsed_time = get_ticks() - game_start_time if game_start_time is not None else 0

        data = {
            "bosses_defeated": bosses_defeated,
            "elapsed_time": elapsed_time
        }

        with open(self._save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("[SaveManager] Progresso salvo com sucesso.")

    def load_progress(self):
        """
        Carrega o progresso salvo, restaurando bosses derrotados e reiniciando timer.
        """
        if not os.path.exists(self._save_file):
            print("[SaveManager] Nenhum save encontrado.")
            return None

        with open(self._save_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        bosses_defeated = data.get("bosses_defeated", [])
        for boss_key in bosses_defeated:
            if boss_key in TRAINER_DATA:
                TRAINER_DATA[boss_key]["defeated"] = True

        elapsed_time = data.get("elapsed_time", 0)

        # Reinicia o timer global
        from pygame.time import get_ticks as pygame_get_ticks
        global game_start_time
        game_start_time = pygame_get_ticks() - elapsed_time

        print("[SaveManager] Progresso carregado com sucesso.")
        return data

# Instância global, se quiser importar direto
save_manager = SaveManager()
