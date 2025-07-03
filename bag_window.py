import pygame
import requests
import io
import time
from os.path import join as path_join
from bag_manager import BagManager
from api_client import APIClient
from typing import List, Dict, Any, Union, Optional, Tuple
from pokemon import Pokemon 
from bases.config import Config
import os


# Inicialização do mixer
CAMINHO_SOM_CLIQUE: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds", "button_press_choice.mp3")
SOM_CLIQUE: pygame.mixer.Sound = pygame.mixer.Sound(CAMINHO_SOM_CLIQUE) 
SOM_CLIQUE.set_volume(0.5) 


class BagWindow:
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
    TAMANHO_SPRITE_BAG: int = 80
    
    # Cache para sprites de Pokémon carregadas da URL para evitar requisições repetidas
    _sprite_cache: Dict[str, pygame.Surface] = {}

    
    def __init__(self):
        self.__largura_slot: int = 100
        self.__altura_slot: int = 100
        self.__espacamento: int = 30
        self.__selecionados = [] # Assumindo que 'selecionados' guarda dicionários de pokémons
        self.__bag_rects: List[pygame.Rect] = [] # Assumindo que 'bag_rects' guarda objetos Rect do Pygame
        self.__tempo_inicio_animacao: float = time.time()
        
        try:
            self.__fonte: pygame.font.Font = pygame.font.Font(path_join("assets", "fonts", "PokemonGb-RAeo.ttf"), 20)
        except Exception:
            self.__fonte: pygame.font.Font = pygame.font.Font(None, 20) 
        self.__fonte1: pygame.font.Font = pygame.font.SysFont("arial", 20) # Fonte de sistema para uso geral (HP)
        
        self.__pagina_atual: int = 0
        self.__pokemons_por_pagina: int = 15

        # Atributos de grupo de botões (serão criados dinamicamente ou populados)
        self.__botao_esquerda: Optional[pygame.Rect] = None
        self.__botao_direita: Optional[pygame.Rect] = None

        # Gerenciadores de dependências
        self.__bag_manager: BagManager = BagManager()
        self.__api_client: APIClient = APIClient()
        
    # --- Propriedades (Getters e Setters) ---
    @property
    def largura_slot(self) -> int:
        return self.__largura_slot

    @largura_slot.setter
    def largura_slot(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("A 'largura_slot' deve ser um inteiro positivo.")
        self.__largura_slot = value

    @property
    def altura_slot(self) -> int:
        return self.__altura_slot

    @altura_slot.setter
    def altura_slot(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("A 'altura_slot' deve ser um inteiro positivo.")
        self.__altura_slot = value

    @property
    def espacamento(self) -> int:
        return self.__espacamento

    @espacamento.setter
    def espacamento(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("O 'espacamento' deve ser um inteiro não negativo.")
        self.__espacamento = value

    @property
    def selecionados(self) -> List[Dict[str, Any]]:
        return self.__selecionados

    @selecionados.setter
    def selecionados(self, value: List[Dict[str, Any]]) -> None:
        if not isinstance(value, list) or not all(isinstance(p, dict) for p in value):
            raise TypeError("A lista de 'selecionados' deve conter apenas dicionários de Pokémon.")
        self.__selecionados = value

    @property
    def bag_rects(self) -> List[pygame.Rect]:
        return self.__bag_rects

    @bag_rects.setter
    def bag_rects(self, value: List[pygame.Rect]) -> None:
        if not isinstance(value, list) or not all(isinstance(r, pygame.Rect) for r in value):
            raise TypeError("A 'bag_rects' deve ser uma lista de pygame.Rect.")
        self.__bag_rects = value

    @property
    def tempo_inicio_animacao(self) -> float:
        return self.__tempo_inicio_animacao

    @tempo_inicio_animacao.setter
    def tempo_inicio_animacao(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("O 'tempo_inicio_animacao' deve ser um número não negativo.")
        self.__tempo_inicio_animacao = float(value)

    @property
    def fonte(self) -> pygame.font.Font:
        return self.__fonte

    @fonte.setter
    def fonte(self, value: pygame.font.Font) -> None:
        if not isinstance(value, pygame.font.Font):
            raise TypeError("A 'fonte' deve ser uma instância de pygame.font.Font.")
        self.__fonte = value

    @property
    def fonte1(self) -> pygame.font.Font:
        return self.__fonte1

    @fonte1.setter
    def fonte1(self, value: pygame.font.Font) -> None:
        if not isinstance(value, pygame.font.Font):
            raise TypeError("A 'fonte1' deve ser uma instância de pygame.font.Font.")
        self.__fonte1 = value

    @property
    def pagina_atual(self) -> int:
        return self.__pagina_atual

    @pagina_atual.setter
    def pagina_atual(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("A 'pagina_atual' deve ser um inteiro não negativo.")
        self.__pagina_atual = value

    @property
    def pokemons_por_pagina(self) -> int:
        return self.__pokemons_por_pagina

    @pokemons_por_pagina.setter
    def pokemons_por_pagina(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("A 'pokemons_por_pagina' deve ser um inteiro positivo.")
        self.__pokemons_por_pagina = value

    @property
    def botao_esquerda(self) -> Optional[pygame.Rect]:
        return self.__botao_esquerda

    @botao_esquerda.setter
    def botao_esquerda(self, value: Optional[pygame.Rect]) -> None:
        if value is not None and not isinstance(value, pygame.Rect):
            raise TypeError("O 'botao_esquerda' deve ser uma instância de pygame.Rect ou None.")
        self.__botao_esquerda = value

    @property
    def botao_direita(self) -> Optional[pygame.Rect]:
        return self.__botao_direita

    @botao_direita.setter
    def botao_direita(self, value: Optional[pygame.Rect]) -> None:
        if value is not None and not isinstance(value, pygame.Rect):
            raise TypeError("O 'botao_direita' deve ser uma instância de pygame.Rect ou None.")
        self.__botao_direita = value

    @property
    def bag_manager(self) -> BagManager:
        return self.__bag_manager

    @bag_manager.setter
    def bag_manager(self, value: BagManager) -> None:
        if not isinstance(value, BagManager):
            raise TypeError("O 'bag_manager' deve ser uma instância de BagManager.")
        self.__bag_manager = value

    @property
    def api_client(self) -> APIClient:
        return self.__api_client

    @api_client.setter
    def api_client(self, value: APIClient) -> None:
        if not isinstance(value, APIClient):
            raise TypeError("O 'api_client' deve ser uma instância de APIClient.")
        self.__api_client = value

    # --- Métodos da Classe ---

    def carregar_sprite(self, url: str) -> pygame.Surface:
        """
        Carrega a imagem de um Pokémon a partir de uma URL e a redimensiona.
        Usa cache para evitar requisições de rede repetidas.
        """
        # Verifica se o sprite já está no cache
        if url in self._sprite_cache: 
            return self._sprite_cache[url]

        try:
            response = requests.get(url, timeout=5) 
            response.raise_for_status() 
            img_file = io.BytesIO(response.content)
            sprite = pygame.image.load(img_file).convert_alpha()
            
            # Acessa a constante TAMANHO_SPRITE_BAG desta classe para redimensionamento
            scaled_sprite = pygame.transform.scale(sprite, (self.TAMANHO_SPRITE_BAG, self.TAMANHO_SPRITE_BAG))
            
            self._sprite_cache[url] = scaled_sprite 
            return scaled_sprite
        except requests.exceptions.Timeout:
            print(f"Erro de timeout ao carregar sprite de {url}.")
            return pygame.Surface((self.TAMANHO_SPRITE_BAG, self.TAMANHO_SPRITE_BAG), pygame.SRCALPHA)
        except Exception as e:
            print(f"Erro ao carregar sprite de {url}: {e}")
            return pygame.Surface((self.TAMANHO_SPRITE_BAG, self.TAMANHO_SPRITE_BAG), pygame.SRCALPHA)



    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Processa eventos de input para a janela da bag.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos: Tuple[int, int] = event.pos
            for idx, rect in enumerate(self.bag_rects): 
                if rect.collidepoint(mouse_pos):
                    SOM_CLIQUE.play()
                    self.toggle_selection(idx) 
                    return
            if self.botao_esquerda and self.botao_esquerda.collidepoint(mouse_pos): 
                SOM_CLIQUE.play()
                self.pagina_atual = max(self.pagina_atual - 1, 0)
            elif self.botao_direita and self.botao_direita.collidepoint(mouse_pos): 
                SOM_CLIQUE.play()
                max_pag: int = max(0, (len(self.bag_manager.load_bag().get("pokemons", [])) - 1) // self.pokemons_por_pagina)
                self.pagina_atual = min(self.pagina_atual + 1, max_pag)


    def toggle_selection(self, idx: int) -> None:
        bag: Dict[str, Any] = self.bag_manager.load_bag() 
        pokemons_bag: List[Dict[str, Any]] = bag.get("pokemons", [])
        real_idx: int = self.pagina_atual * self.pokemons_por_pagina + idx
        if real_idx >= len(pokemons_bag):
            return

        pokemon: Dict[str, Any] = pokemons_bag[real_idx]
        nome: str = pokemon["name"]

        if pokemon in self.selecionados:
            self.selecionados.remove(pokemon)
            self.bag_manager.deselect_pokemon(nome) 
            if nome in bag.get("selected_for_battle", []):
                bag["selected_for_battle"].remove(nome)
        elif len(self.selecionados) < 3:
            self.selecionados.append(pokemon)
            self.bag_manager.select_pokemon_for_battle(nome) 
            if "selected_for_battle" not in bag:
                bag["selected_for_battle"] = []
            if nome not in bag["selected_for_battle"]:
                bag["selected_for_battle"].append(nome)

        self.bag_manager.save_bag(bag)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a janela da bag na tela.
        """
        overlay: pygame.Surface = pygame.Surface((Config().largura_tela, Config().altura_tela), pygame.SRCALPHA)
        overlay.fill(self.COR_TRANSLUCIDA) 
        screen.blit(overlay, (0, 0))

        largura_janela: int = 900
        altura_janela: int = 600
        x_janela: int = (Config().largura_tela - largura_janela) // 2 
        y_janela: int = (Config().altura_tela - altura_janela) // 2 

        janela_surface: pygame.Surface = pygame.Surface((largura_janela, altura_janela), pygame.SRCALPHA)
        janela_surface.fill(self.COR_JANELA) 
        pygame.draw.rect(janela_surface, self.COR_BORDA_JANELA, janela_surface.get_rect(), 3, border_radius=12) 
        screen.blit(janela_surface, (x_janela, y_janela))

        bag: Dict[str, Any] = self.bag_manager.load_bag()
        pokemons_bag: List[Dict[str, Any]] = bag.get("pokemons", [])
        self.bag_rects = [] 

        # Topo - slots de selecionados
        total_width_top: int = 3 * self.largura_slot + 2 * self.espacamento
        start_x_top: int = x_janela + (largura_janela - total_width_top) // 2
        y_top: int = y_janela + 40
        
        bag = self.bag_manager.load_bag() 
        selecionados_nomes: List[str] = bag.get("selected_for_battle", [])
        pokemons_bag = bag.get("pokemons", [])
        self.selecionados = [] 

        for nome in selecionados_nomes:
            for p in pokemons_bag:
                if p["name"] == nome:
                    self.selecionados.append(p)
                    break

        for i in range(3):
            rect: pygame.Rect = pygame.Rect(
                start_x_top + i * (self.largura_slot + self.espacamento),
                y_top,
                self.largura_slot,
                self.altura_slot
            )
            pygame.draw.rect(screen, self.COR_SLOT, rect, border_radius=8) 
            
            if i < len(self.selecionados):
                sprites: Dict[str, Any] = self.selecionados[i].get("sprites", {})
                sprite_url: Optional[str] = sprites.get("front_default")

                if sprite_url:
                    sprite = self.carregar_sprite(sprite_url) 
                else:
                    print(f"Sprite 'front_default' ausente para o Pokémon selecionado: {self.selecionados[i].get('name', 'desconhecido')}")
                    sprite = pygame.Surface((self.TAMANHO_SPRITE_BAG, self.TAMANHO_SPRITE_BAG), pygame.SRCALPHA) 

                screen.blit(sprite, sprite.get_rect(center=rect.center))

        # Texto "Selecione seus pokémons para as batalhas!"
        texto_msg: pygame.Surface = self.fonte.render("Selecione seus pokémons para as batalhas!", True, self.COR_TEXTO)
        texto_rect_msg: pygame.Rect = texto_msg.get_rect(center=(Config().largura_tela // 2, y_top + self.altura_slot + 20))
        screen.blit(texto_msg, texto_rect_msg)

        # Animação da borda (efeito de pisca)
        tempo: float = time.time() - self.tempo_inicio_animacao
        intensidade: float = (abs((tempo % 1.0) - 0.5) * 2)
        cor_borda: Tuple[int, int, int] = (
            int(self.COR_BORDA_PISCA_1[0] * intensidade + self.COR_BORDA_PISCA_2[0] * (1 - intensidade)),
            int(self.COR_BORDA_PISCA_1[1] * intensidade + self.COR_BORDA_PISCA_2[1] * (1 - intensidade)),
            int(self.COR_BORDA_PISCA_1[2] * intensidade + self.COR_BORDA_PISCA_2[2] * (1 - intensidade))
        )

        # Grade de Pokémon na bag
        colunas: int = 5
        linhas: int = 3
        total_width_grid: int = colunas * self.largura_slot + (colunas - 1) * self.espacamento
        start_x_grid: int = x_janela + (largura_janela - total_width_grid) // 2
        start_y_grid: int = y_top + self.altura_slot + 60

        inicio_idx: int = self.pagina_atual * self.pokemons_por_pagina
        fim_idx: int = inicio_idx + self.pokemons_por_pagina

        for idx, pokemon in enumerate(pokemons_bag[inicio_idx:fim_idx]):
            linha: int = idx // colunas
            coluna: int = idx % colunas
            x_rect: int = start_x_grid + coluna * (self.largura_slot + self.espacamento)
            y_rect: int = start_y_grid + linha * (self.altura_slot + self.espacamento)
            rect_slot: pygame.Rect = pygame.Rect(x_rect, y_rect, self.largura_slot, self.altura_slot)
            self.bag_rects.append(rect_slot) 

            if pokemon in self.selecionados:
                pygame.draw.rect(screen, self.COR_SELECIONADO, rect_slot, border_radius=6) 
                pygame.draw.rect(screen, cor_borda, rect_slot, width=3, border_radius=6)
            else:
                pygame.draw.rect(screen, self.COR_GRADE, rect_slot, border_radius=6) 

            sprite_url = pokemon.get("sprites", {}).get("front_default")
            if sprite_url:
                sprite = self.carregar_sprite(sprite_url)
            else:
                print(f"Sprite 'front_default' ausente para o Pokémon {pokemon.get('name', 'desconhecido')}")
                sprite = pygame.Surface((self.TAMANHO_SPRITE_BAG, self.TAMANHO_SPRITE_BAG), pygame.SRCALPHA) 

            screen.blit(sprite, sprite.get_rect(center=rect_slot.center))
            
            # Mostrar HP abaixo do sprite
            hp_atual: Union[int, str] = pokemon.get("current_hp", "??")
            nivel: int = 70 

            data_pokemon: Optional[Dict[str, Any]] = self.api_client.fetch_pokemon_data(pokemon["name"]) 
            if data_pokemon and "stats" in data_pokemon:
                base_hp: int = next((s["base_stat"] for s in data_pokemon["stats"] if s["stat"]["name"] == "hp"), 50)
                hp_maximo: int = base_hp + nivel
            else:
                hp_maximo = "??"

            texto_hp: pygame.Surface = self.fonte1.render(f"HP: {hp_atual}/{hp_maximo}", True, self.COR_TEXTO) 
            hp_rect: pygame.Rect = texto_hp.get_rect(center=(rect_slot.centerx, rect_slot.bottom + 10))
            screen.blit(texto_hp, hp_rect)


        # Botões de página
        self.botao_esquerda = pygame.Rect(x_janela + 30, y_janela + altura_janela - 50, 40, 30) 
        self.botao_direita = pygame.Rect(x_janela + largura_janela - 70, y_janela + altura_janela - 50, 40, 30) 
        
        pygame.draw.rect(screen, self.COR_BOTAO, self.botao_esquerda, border_radius=4) 
        pygame.draw.rect(screen, self.COR_BOTAO, self.botao_direita, border_radius=4) 

        seta_esq: pygame.Surface = self.fonte1.render("<", True, self.COR_TEXTO) 
        seta_dir: pygame.Surface = self.fonte1.render(">", True, self.COR_TEXTO) 
        screen.blit(seta_esq, seta_esq.get_rect(center=self.botao_esquerda.center))
        screen.blit(seta_dir, seta_dir.get_rect(center=self.botao_direita.center))

        total_paginas: int = max(1, (len(pokemons_bag) + self.pokemons_por_pagina - 1) // self.pokemons_por_pagina)
        texto_pagina: pygame.Surface = self.fonte.render(f"Página {self.pagina_atual + 1}/{total_paginas}", True, self.COR_TEXTO)
        screen.blit(texto_pagina, texto_pagina.get_rect(center=(Config().largura_tela // 2, y_janela + altura_janela - 35)))