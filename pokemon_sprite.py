import pygame
import io
from urllib.request import urlopen, URLError
from pokemon import Pokemon

class PokemonSprite(pygame.sprite.Sprite):
    """
    Representa a parte visual de um Pokémon na tela. Herda de pygame.sprite.Sprite.
    """
    def __init__(self, pokemon_data: Pokemon, side: str, size: int) -> None:
        super().__init__()
        self.pokemon_data = pokemon_data
        self.image = self._load_sprite(pokemon_data.get_sprite_url(side), size)
        self.rect = self.image.get_rect()

    def _load_sprite(self, url: str, size: int) -> pygame.Surface:
        """
        Carrega a imagem do Pokémon a partir de uma URL e a redimensiona.
        """
        try:
            image_stream = urlopen(url).read()
            image_file = io.BytesIO(image_stream)
            image = pygame.image.load(image_file).convert_alpha()
            
            # Redimensiona mantendo a proporção
            scale = size / image.get_width()
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            return pygame.transform.scale(image, (new_width, new_height))
        except (URLError, pygame.error) as e:
            print(f"Erro ao carregar sprite de {url}: {e}")
            # Retorna uma superfície vazia em caso de erro
            fallback_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            fallback_surface.fill((0,0,0,0)) # Transparente
            return fallback_surface