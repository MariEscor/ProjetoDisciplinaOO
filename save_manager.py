# save_manager.py

import json
import os

SAVE_FILE = 'savegame.json'

def save_progress(data: dict) -> None:
    """
    Salva os dados do jogo em um arquivo JSON.
    """
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_progress() -> dict:
    """
    Carrega os dados salvos do jogo. Retorna um dicionário.
    """
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def has_saved_game() -> bool:
    """
    Verifica se existe um savegame.
    """
    return os.path.exists(SAVE_FILE)
