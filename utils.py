import pygame
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame
from typing import Any 

class Utils:

    @staticmethod
    def importar_imagem(*path: str, alpha: bool = True, format: str = 'png') -> pygame.Surface:
        full_path = join(*path) + f'.{format}'
        surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
        return surf

    @staticmethod
    def importar_pasta(*path: str) -> list[pygame.Surface]:
        frames = []
        for folder_path, sub_folders, image_names in walk(join(*path)):
            for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0]) if name.split('.')[0].isdigit() else name):
                full_path = join(folder_path, image_name)
                surf = pygame.image.load(full_path).convert_alpha()
                frames.append(surf)
        return frames

    @staticmethod
    def importar_pasta_dicionario(*path: str) -> dict[str, pygame.Surface]:
        frames = {}
        for folder_path, sub_folders, image_names in walk(join(*path)):
            for image_name in image_names:
                full_path = join(folder_path, image_name)
                surf = pygame.image.load(full_path).convert_alpha()
                frames[image_name.split('.')[0]] = surf
        return frames

    @staticmethod
    def importar_mapas_tmx(*path: str) -> dict[str, Any]: 
        tmx_dict = {}
        for folder_path, sub_folders, file_names in walk(join(*path)):
            for file in file_names:
                if file.endswith('.tmx'):
                    tmx_dict[file.split('.')[0]] = load_pygame(join(folder_path, file))
        return tmx_dict
    
    @staticmethod
    def importar_tilemap(cols, rows, *path):
        frames = {}
        surf = Utils.importar_imagem(*path)
        cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
        for col in range(cols):
            for row in range(rows):
                cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
                cutout_surf = pygame.Surface((cell_width, cell_height), pygame.SRCALPHA)  # Suporte a transparência
                cutout_surf.blit(surf, (0, 0), cutout_rect)
                frames[(col, row)] = cutout_surf
        return frames

    @staticmethod
    def coast_importar(cols, rows, *path):
        frame_dict = Utils.importar_tilemap(cols, rows, *path)
        new_dict = {}
        terrains = ['grass', 'grass_i', 'sand', 'sand_i', 'rock', 'rock_i', 'ice', 'ice_i']
        sides = {
            'topleft': (0,0), 'top': (1,0), 'topright': (2,0),
            'left': (1,0), 'right': (2,1), 'bottomleft': (0,2),
            'bottom': (1,2), 'bottomright': (2,2),
        }
        for index, terrain in enumerate(terrains):
            new_dict[terrain] = {}
            for key, pos in sides.items():
                new_dict[terrain][key] = [frame_dict[(pos[0] + index * 3, pos[1] + row)] for row in range(0, rows, 3)]
            return new_dict