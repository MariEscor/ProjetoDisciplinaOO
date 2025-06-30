# utils.py

import pygame
from pygame.math import Vector2 as vector

from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame
from typing import List, Dict, Any, Union

from Projeto.config import Config

class Utils:

    @staticmethod
    def importar_imagem(*path: str, alpha: bool = True, formato: str = 'png') -> pygame.Surface:
        """
        Importa uma imagem de um caminho especificado.

        Args:
            *path (str): Componentes do caminho até a imagem (e.g., 'assets', 'graphics', 'player').
            alpha (bool): Se a imagem deve ser carregada com canal alpha (transparência). Padrão é True.
            formato (str): Formato do arquivo da imagem (e.g., 'png', 'jpg'). Padrão é 'png'.

        Returns:
            pygame.Surface: A superfície Pygame carregada com a imagem.
        """
        caminho_completo: str = join(*path) + f'.{formato}'
        surf = pygame.image.load(caminho_completo).convert_alpha() if alpha else pygame.image.load(caminho_completo).convert()
        return surf

    @staticmethod
    def importar_pasta(*path: str) -> List[pygame.Surface]:
        """
        Importa todas as imagens de uma pasta, ordenadas numericamente.

        Args:
            *path (str): Componentes do caminho até a pasta.

        Returns:
            List[pygame.Surface]: Uma lista de superfícies Pygame.
        """
        frames: List[pygame.Surface] = []
        for caminho_pasta, sub_pastas, img_nomes in walk(join(*path)):
            for img_nome in sorted(img_nomes, key = lambda name: int(name.split('.')[0])):
                caminho_completo: str = join(caminho_pasta, img_nome)
                surf: pygame.Surface = pygame.image.load(caminho_completo).convert_alpha()
                frames.append(surf)
        return frames

    @staticmethod
    def importar_tilemap(cols: int, rows: int, *path: str) -> Dict[tuple[int, int], pygame.Surface]:
        """
        Importa um tilemap de uma única imagem, dividindo-a em tiles.

        Args:
            cols (int): Número de colunas no tilemap.
            rows (int): Número de linhas no tilemap.
            *path (str): Componentes do caminho até a imagem do tilemap.

        Returns:
            Dict[tuple[int, int], pygame.Surface]: Um dicionário onde as chaves são (col, row)
                                                    e os valores são as superfícies dos tiles.
        """
        frames: Dict[tuple[int, int], pygame.Surface] = {}
        surf: pygame.Surface = Utils.importar_imagem(*path)
        largura_celula: float = surf.get_width() / cols
        altura_celula: float = surf.get_height() / rows

        for col in range(cols):
            for row in range(rows):
                recorte_rect = pygame.Rect(col * largura_celula, row * altura_celula, largura_celula, altura_celula)
                recorte_surf: pygame.Surface = pygame.Surface((largura_celula, altura_celula), pygame.SRCALPHA)
                recorte_surf.fill(Config.CORES['plant'])
                recorte_surf.set_colorkey(Config.CORES['plant'])
                recorte_surf.blit(surf, (0, 0), recorte_rect)
                frames[(col, row)] = recorte_surf
        return frames

    @staticmethod
    def importar_personagens(cols: int, rows: int, *path: str) -> Dict[str, List[pygame.Surface]]:
        """
        Importa frames de animação para um único personagem, organizando por direção.

        Args:
            cols (int): Número de colunas no spritesheet do personagem.
            rows (int): Número de linhas no spritesheet do personagem.
            *path (str): Componentes do caminho até o spritesheet.

        Returns:
            Dict[str, List[pygame.Surface]]: Um dicionário onde as chaves são direções
                                            (e.g., 'down', 'down_idle') e os valores são listas de superfícies.
        """
        frame_dict: Dict[tuple[int, int], pygame.Surface] = Utils.importar_tilemap(cols, rows, *path)
        novo_dict: Dict[str, List[pygame.Surface]] = {}
        for row, direcao in enumerate(['down', 'left', 'right', 'up']): #direções que o personagem pode iniciar
            novo_dict[direcao] = [frame_dict[(col, row)] for col in range(cols)]
            novo_dict[f'{direcao}_idle'] = [frame_dict[(0, row)]]
        return novo_dict

    @staticmethod
    def importar_todos_personagens(*path: str) -> Dict[str, Dict[str, List[pygame.Surface]]]:
        """
        Importa frames de animação para todos os personagens em uma pasta.

        Args:
            *path (str): Componentes do caminho até a pasta de personagens.

        Returns:
            Dict[str, Dict[str, List[pygame.Surface]]]: Um dicionário onde as chaves são nomes de personagens
                                                        e os valores são dicionários de frames por direção.
        """
        novo_dict: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        for _, __, img_nomes in walk(join(*path)):
            for img in img_nomes:
                img_nome: str = img.split('.')[0]
                novo_dict[img_nome] = Utils.importar_personagens(4, 4, *path, img_nome)
        return novo_dict

    @staticmethod
    def importar_coast(cols: int, rows: int, *path: str) -> Dict[str, Dict[str, List[pygame.Surface]]]:
        """
        Importa e organiza frames de tiles de "coast" (bordas de terreno).

        Args:
            cols (int): Número de colunas no spritesheet da coast.
            rows (int): Número de linhas no spritesheet da coast.
            *path (str): Componentes do caminho até o spritesheet.

        Returns:
            Dict[str, Dict[str, List[pygame.Surface]]]: Dicionário de frames organizados por terreno e lado.
        """
        frames_dict: Dict[tuple[int, int], pygame.Surface] = Utils.importar_tilemap(cols, rows, *path)
        novo_dict: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        #['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i'] == ['grass', 'grass_invertida', 'sand_invertida', 'sand', 'rock', 'rock_invertida', 'ice', 'ice_invertida']
        terrenos: List[str] = ['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i'] #se atentar ao colocar as coasts no TMX na propriedade side do Tiled
        
        """
        caso a gente queira usar a nomenclatura em PT-BR
        lados: Dict[str, tuple[int, int]] = {
            'topo_esquerda': (0, 0), 'topo': (1, 0), 'topo_direita': (2, 0),
            'esquerda': (0, 1), 'direita': (2, 1), 'inferior_esquerda': (0, 2),
            'inferior': (1, 2), 'inferior_direita': (2, 2)
        }"""
        
        lados: Dict[str, tuple[int, int]] = {
            'topleft': (0,0), 'top': (1,0), 'topright': (2,0), 
            'left': (0,1), 'right': (2,1), 'bottomleft': (0,2), 
            'bottom': (1,2), 'bottomright': (2,2)}
        
        for index, terreno in enumerate(terrenos):
            novo_dict[terreno] = {}
            for key, pos in lados.items():
                novo_dict[terreno][key] = [frames_dict[(pos[0] + index * 3  , pos[1] + row )] for row in range(0, rows, 3)]
        return novo_dict

    @staticmethod
    def detecta_entidade(raio: Union[int, float], entidade: Any, alvo: Any, tolerancia: Union[int, float] = 30) -> bool:
        """
        Verifica se uma entidade está dentro do raio de visão e direção de outra entidade.

        Args:
            raio (Union[int, float]): O raio de detecção.
            entidade (Any): A entidade que está detectando (com atributos 'olhando' e 'rect').
            alvo (Any): A entidade a ser detectada (com atributo 'rect').
            tolerancia (Union[int, float]): Tolerância para alinhamento direcional.

        Returns:
            bool: True se o alvo estiver dentro do raio e direção de visão, False caso contrário.
        """
        relacao: vector = vector(alvo.rect.center) - vector(entidade.rect.center)
        if relacao.length() < raio:
            # Acessa a propriedade 'olhando' da entidade para determinar a direção.
            # Assume que 'olhando' é uma propriedade (ou atributo) na classe Entidades.
            if entidade.olhando == 'left' and relacao.x < 0 and abs(relacao.y) < tolerancia or \
                entidade.olhando == 'right' and relacao.x > 0 and abs(relacao.y) < tolerancia or \
                entidade.olhando == 'up' and relacao.y < 0 and abs(relacao.x) < tolerancia or \
                entidade.olhando == 'down' and relacao.y > 0 and abs(relacao.x) < tolerancia:
                return True
        return False # Retorna False se o alvo estiver fora do raio de detecção

    @staticmethod
    def importar_tmx(*path: str) -> Dict[str, Any]:
        """
        Importa arquivos de mapa TMX usando pytmx.

        Args:
            *path (str): Componentes do caminho até a pasta dos arquivos .tmx.

        Returns:
            Dict[str, Any]: Um dicionário onde as chaves são os nomes dos arquivos TMX
                            (sem extensão) e os valores são os objetos de mapa carregados.
        """
        tmx_dict: Dict[str, Any] = {}
        for pasta_caminho, sub_pastas, nomes_arquivos in walk(join(*path)):
            for arquivo in nomes_arquivos:
                tmx_dict[arquivo.split('.')[0]] = load_pygame(join(pasta_caminho, arquivo))
        return tmx_dict