import pygame
import random
import os
import constants
import api_client
import ui
from game_scene import GameScene
from pokemon import Pokemon
from pokemon_sprite import PokemonSprite
from scene_manager import load_scene
from bag_manager import add_pokemon_to_bag
from bag_manager import set_initial_pokemon


class SelectionScene(GameScene):
    """
    Cena para o jogador escolher o seu Pokémon inicial.
    """
    def __init__(self) -> None:
        super().__init__()
        self.pokemons_to_load = ['bulbasaur', 'charmander', 'squirtle']
        self.pokemon_objects: list[Pokemon] = []
        self.pokemon_sprites = pygame.sprite.Group()
        self.selected_pokemon: Pokemon | None = None
        self.rival_pokemon: Pokemon | None = None
        
        # --- Adicionar o background aqui ---
        self.background_image: pygame.Surface = self._load_background('background', 'fundo_escolha.png')
        # ------------------------------------

        self._load_pokemons()

    def _load_background(self, folder: str, filename: str) -> pygame.Surface:
        """
        Carrega uma imagem de background de um caminho relativo.
        """
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, folder, filename)
        
        if not os.path.exists(image_path):
            print(f"Erro: Imagem de background não encontrada em: {image_path}")
            background_surface = pygame.Surface((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
            background_surface.fill(constants.GRAY) # Uma cor padrão se a imagem falhar
            return background_surface
            
        try:
            image = pygame.image.load(image_path).convert_alpha()
            # Opcional: Redimensionar a imagem para o tamanho da janela se necessário
            # image = pygame.transform.scale(image, (constants.LARGURA_JANELA, constants.ALTURA_JANELA))
            return image
        except pygame.error as e:
            print(f"Erro ao carregar imagem de background '{image_path}': {e}")
            background_surface = pygame.Surface((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
            background_surface.fill(constants.GRAY) # Uma cor padrão se a imagem falhar
            return background_surface

    def _load_pokemons(self) -> None:
        """
        Busca os dados dos Pokémon na API e cria os objetos e sprites.
        """
        x_pos_start = constants.LARGURA_JANELA * 0.2
        x_pos_step = constants.LARGURA_JANELA * 0.3
        y_pos = constants.ALTURA_JANELA * 0.5

        for i, name in enumerate(self.pokemons_to_load):
            data = api_client.fetch_pokemon_data(name)
            if data:
                level = 30
                pokemon = Pokemon(name, level, data)
                self.pokemon_objects.append(pokemon)
                
                # O sprite é a parte visual, o objeto Pokemon são os dados
                sprite = PokemonSprite(pokemon, 'front_default', size=250)
                sprite.rect.center = (x_pos_start + i * x_pos_step, y_pos)
                self.pokemon_sprites.add(sprite)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in self.pokemon_sprites:
                    if sprite.rect.collidepoint(event.pos):
                        self.selected_pokemon = sprite.pokemon_data
                        
                        # Escolhe o Pokémon do rival aleatoriamente
                        possible_rivals = [p for p in self.pokemon_objects if p != self.selected_pokemon]
                        self.rival_pokemon = random.choice(possible_rivals)
                        self.rival_pokemon.level = int(self.rival_pokemon.level * 0.8) # Dificuldade
                        
                        # Sinaliza para o main loop trocar para a cena de batalha
                        self.next_scene = 'battle'
                        break
                    
    def update(self) -> None:
        """
        A tela de seleção não tem lógica de atualização contínua,
        então o método pode ficar vazio.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        # --- Desenha o background PRIMEIRO ---
        screen.blit(self.background_image, (0, 0))
        # ------------------------------------

        # Desenha o título
        # Certifique-se de que ui.draw_text está importado e funcionando corretamente.
        ui.draw_text(screen, 'Escolha seu Pokémon Inicial!', 42, constants.BLACK, (constants.LARGURA_JANELA // 2, 80))
        
        # --- Lógica para desenhar os Pokémon com destaque de hover ---
        mouse_pos = pygame.mouse.get_pos()
        
        for sprite in self.pokemon_sprites:
            # Verifica se o mouse está sobre o sprite atual
            if sprite.rect.collidepoint(mouse_pos):
                # Preenche o fundo do retângulo do sprite com branco
                # O border_radius=5 pode ser ajustado para um arredondamento suave
                pygame.draw.rect(screen, constants.GREEN_BACK, sprite.rect, border_radius=6)
                
                # Desenha a borda preta (opcional, já estava no seu código e funciona como um destaque)
                pygame.draw.rect(screen, constants.BLACK, sprite.rect, 3, border_radius=6)
            
            # Desenha o sprite do Pokémon por cima do possível fundo branco e borda
            # Esta linha é CRUCIAL e deve ser chamada para CADA sprite
            screen.blit(sprite.image, sprite.rect)
        # --- Fim da lógica de desenho dos Pokémon ---


from scene_manager import load_scene
from bag_manager import add_pokemon_to_bag


def run_selection():
    pygame.init()
    screen = pygame.display.set_mode((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
    pygame.display.set_caption("Escolha seu Pokémon")
    scene = SelectionScene()
    clock = pygame.time.Clock()
    FPS = 60
    
    pokemon_salvo = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        scene.handle_events(events)
        scene.update()
        scene.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

                # Se o jogador escolheu um Pokémon, salvar e ir para o mundo aberto
        if getattr(scene, "next_scene", None) == "battle" and not pokemon_salvo:
            if scene.selected_pokemon:
                set_initial_pokemon(scene.selected_pokemon.name)
                pokemon_salvo = True
                load_scene("mundo_aberto")
            break
