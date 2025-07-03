import pygame
import requests
import io
import time
from os.path import join as path_join
from bag_manager import BagManager
from api_client import APIClient
# Inicialização do mixer
pygame.mixer.init()
SOM_CLIQUE = pygame.mixer.Sound("assets/sounds/button_press_choice.mp3")  # Substitua o caminho se necessário

# Constantes
LARGURA_JANELA = 1280
ALTURA_JANELA = 720
COR_TRANSLUCIDA = (0, 0, 0, 180)
COR_JANELA = (30, 30, 30, 240)
COR_BORDA_JANELA = (0, 180, 255)
COR_SLOT = (255, 255, 255, 120)
COR_GRADE = (40, 40, 40, 200)
COR_SELECIONADO = (0, 120, 255, 160)
COR_BORDA_PISCA_1 = (0, 200, 255)
COR_BORDA_PISCA_2 = (0, 150, 200)
COR_BOTAO = (60, 60, 60)
COR_TEXTO = (255, 255, 255)
TAMANHO_SPRITE = 80

class BagWindow:
    def __init__(self):
        self.largura_slot = 100
        self.altura_slot = 100
        self.espacamento = 30
        self.selecionados = []
        self.bag_rects = []
        self.tempo_inicio_animacao = time.time()
        self.fonte  = pygame.font.Font(path_join("background", "PokemonGb-RAeo.ttf"), 20)
        self.fonte1  = pygame.font.SysFont("arial", 20)
        self.pagina_atual = 0
        self.pokemons_por_pagina = 15

    def carregar_sprite(self, url):
        try:
            response = requests.get(url)
            img_file = io.BytesIO(response.content)
            sprite = pygame.image.load(img_file).convert_alpha()
            return pygame.transform.scale(sprite, (TAMANHO_SPRITE, TAMANHO_SPRITE))
        except Exception as e:
            print(f"Erro ao carregar sprite: {e}")
            return pygame.Surface((TAMANHO_SPRITE, TAMANHO_SPRITE), pygame.SRCALPHA)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for idx, rect in enumerate(self.bag_rects):
                if rect.collidepoint(mouse_pos):
                    SOM_CLIQUE.play()
                    self._toggle_selection(idx)
                    return
            if self.botao_esquerda.collidepoint(mouse_pos):
                SOM_CLIQUE.play()
                self.pagina_atual = max(self.pagina_atual - 1, 0)
            elif self.botao_direita.collidepoint(mouse_pos):
                SOM_CLIQUE.play()
                max_pag = max(0, (len(BagManager().load_bag().get("pokemons", [])) - 1) // self.pokemons_por_pagina)
                self.pagina_atual = min(self.pagina_atual + 1, max_pag)

    def _toggle_selection(self, idx):
        bag = BagManager().load_bag()
        pokemons_bag = bag.get("pokemons", [])
        real_idx = self.pagina_atual * self.pokemons_por_pagina + idx
        if real_idx >= len(pokemons_bag):
            return

        pokemon = pokemons_bag[real_idx]
        nome = pokemon["name"]

        if pokemon in self.selecionados:
            self.selecionados.remove(pokemon)
            BagManager().deselect_pokemon(nome)
            if nome in bag.get("selected_for_battle", []):
                bag["selected_for_battle"].remove(nome)
        elif len(self.selecionados) < 3:
            self.selecionados.append(pokemon)
            BagManager().select_pokemon_for_battle(nome)
            if "selected_for_battle" not in bag:
                bag["selected_for_battle"] = []
            if nome not in bag["selected_for_battle"]:
                bag["selected_for_battle"].append(nome)

        # Salvar o estado atualizado
        BagManager().save_bag(bag)


    def draw(self, screen):
        overlay = pygame.Surface((LARGURA_JANELA, ALTURA_JANELA), pygame.SRCALPHA)
        overlay.fill(COR_TRANSLUCIDA)
        screen.blit(overlay, (0, 0))

        largura_janela = 900
        altura_janela = 600
        x_janela = (LARGURA_JANELA - largura_janela) // 2
        y_janela = (ALTURA_JANELA - altura_janela) // 2

        janela_surface = pygame.Surface((largura_janela, altura_janela), pygame.SRCALPHA)
        janela_surface.fill(COR_JANELA)
        pygame.draw.rect(janela_surface, COR_BORDA_JANELA, janela_surface.get_rect(), 3, border_radius=12)
        screen.blit(janela_surface, (x_janela, y_janela))

        bag = BagManager().load_bag()
        pokemons_bag = bag.get("pokemons", [])
        self.bag_rects = []

        # Topo - selecionados
        total_width_top = 3 * self.largura_slot + 2 * self.espacamento
        start_x_top = x_janela + (largura_janela - total_width_top) // 2
        y_top = y_janela + 40
        
        bag = BagManager().load_bag()
        selecionados_nomes = bag.get("selected_for_battle", [])
        pokemons_bag = bag.get("pokemons", [])
        self.selecionados = []

        for nome in selecionados_nomes:
            for p in pokemons_bag:
                if p["name"] == nome:
                    self.selecionados.append(p)
                    break


        for i in range(3):
            rect = pygame.Rect(
                start_x_top + i * (self.largura_slot + self.espacamento),
                y_top,
                self.largura_slot,
                self.altura_slot
            )
            pygame.draw.rect(screen, COR_SLOT, rect, border_radius=8)
            if i < len(self.selecionados):
                sprites = self.selecionados[i].get("sprites", {})
                sprite_url = sprites.get("front_default")

                if sprite_url:
                    sprite = self.carregar_sprite(sprite_url)
                else:
                    print(f"Sprite 'front_default' ausente para o Pokémon selecionado: {self.selecionados[i].get('name', 'desconhecido')}")
                    sprite = pygame.Surface((TAMANHO_SPRITE, TAMANHO_SPRITE), pygame.SRCALPHA)

                screen.blit(sprite, sprite.get_rect(center=rect.center))

        # Texto
        texto = self.fonte.render("Selecione seus pokémons para as batalhas!", True, COR_TEXTO)
        texto_rect = texto.get_rect(center=(LARGURA_JANELA // 2, y_top + self.altura_slot + 20))
        screen.blit(texto, texto_rect)

        tempo = time.time() - self.tempo_inicio_animacao
        intensidade = (abs((tempo % 1.0) - 0.5) * 2)
        cor_borda = [
            int(COR_BORDA_PISCA_1[i] * intensidade + COR_BORDA_PISCA_2[i] * (1 - intensidade))
            for i in range(3)
        ]

        # Grade
        colunas = 5
        linhas = 3
        total_width_grid = colunas * self.largura_slot + (colunas - 1) * self.espacamento
        start_x_grid = x_janela + (largura_janela - total_width_grid) // 2
        start_y_grid = y_top + self.altura_slot + 60

        inicio_idx = self.pagina_atual * self.pokemons_por_pagina
        fim_idx = inicio_idx + self.pokemons_por_pagina

        for idx, pokemon in enumerate(pokemons_bag[inicio_idx:fim_idx]):
            linha = idx // colunas
            coluna = idx % colunas
            x = start_x_grid + coluna * (self.largura_slot + self.espacamento)
            y = start_y_grid + linha * (self.altura_slot + self.espacamento)
            rect = pygame.Rect(x, y, self.largura_slot, self.altura_slot)
            self.bag_rects.append(rect)

            if pokemon in self.selecionados:
                pygame.draw.rect(screen, COR_SELECIONADO, rect, border_radius=6)
                pygame.draw.rect(screen, cor_borda, rect, width=3, border_radius=6)
            else:
                pygame.draw.rect(screen, COR_GRADE, rect, border_radius=6)

            sprite_url = pokemon.get("sprites", {}).get("front_default")
            if sprite_url:
                sprite = self.carregar_sprite(sprite_url)
            else:
                print(f"Sprite 'front_default' ausente para o Pokémon {pokemon.get('name', 'desconhecido')}")
                sprite = pygame.Surface((TAMANHO_SPRITE, TAMANHO_SPRITE), pygame.SRCALPHA)  # Sprite vazio

            screen.blit(sprite, sprite.get_rect(center=rect.center))
            
            # Mostrar HP abaixo do sprite
            hp_atual = pokemon.get("current_hp", "??")
            nivel = 70  # Se quiser tornar isso dinâmico, salve o nível no JSON

            # Buscar dados do Pokémon para calcular o HP máximo como na classe Pokemon
            data = APIClient().fetch_pokemon_data(pokemon["name"])
            if data and "stats" in data:
                base_hp = next((s["base_stat"] for s in data["stats"] if s["stat"]["name"] == "hp"), 50)
                hp_maximo = base_hp + nivel
            else:
                hp_maximo = "??"

            texto_hp = self.fonte1.render(f"HP: {hp_atual}/{hp_maximo}", True, COR_TEXTO)
            hp_rect = texto_hp.get_rect(center=(rect.centerx, rect.bottom + 10))
            screen.blit(texto_hp, hp_rect)


        # Botões de página
        self.botao_esquerda = pygame.Rect(x_janela + 30, y_janela + altura_janela - 50, 40, 30)
        self.botao_direita = pygame.Rect(x_janela + largura_janela - 70, y_janela + altura_janela - 50, 40, 30)
        pygame.draw.rect(screen, COR_BOTAO, self.botao_esquerda, border_radius=4)
        pygame.draw.rect(screen, COR_BOTAO, self.botao_direita, border_radius=4)

        seta_esq = self.fonte1.render("<", True, COR_TEXTO)
        seta_dir = self.fonte1.render(">", True, COR_TEXTO)
        screen.blit(seta_esq, seta_esq.get_rect(center=self.botao_esquerda.center))
        screen.blit(seta_dir, seta_dir.get_rect(center=self.botao_direita.center))

        total_paginas = max(1, (len(pokemons_bag) + self.pokemons_por_pagina - 1) // self.pokemons_por_pagina)
        texto_pagina = self.fonte.render(f"Página {self.pagina_atual + 1}/{total_paginas}", True, COR_TEXTO)
        screen.blit(texto_pagina, texto_pagina.get_rect(center=(LARGURA_JANELA // 2, y_janela + altura_janela - 35)))
