import pygame
from menu import options
from os.path import join
from scene_manager import load_scene

class PauseMenu:
    def __init__(self, jogo):
        self.jogo = jogo
        self.active = False

        pygame.font.init()
        self.font = pygame.font.Font(join("background", "PokemonGb-RAeo.ttf"), 25)
        self.options = ["Continuar", "Opçoes", "Menu", "Sair"]
        self.selected = 0
        self.option_rects = []

        # Sons
        self.snd_hover = pygame.mixer.Sound(join('background', 'hover.mp3'))
        self.snd_click = pygame.mixer.Sound(join('background', 'click.mp3'))

        # Controle para tocar hover só quando mudar seleção
        self.last_selected = None

        # Fundo fade (alpha controlado)
        self.bg_surface = pygame.Surface(self.jogo.tela_exibicao.get_size(), pygame.SRCALPHA)
        self.bg_alpha = 0
        self.fade_in_speed = 400  # alpha por segundo

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.snd_click.play()
                self.execute_option()

        elif event.type == pygame.MOUSEMOTION:
            self.check_mouse_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.check_mouse_click(event.pos)

    def check_mouse_hover(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                if self.selected != i:
                    self.selected = i
                    self.snd_hover.play()
                break

    def check_mouse_click(self, mouse_pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                self.selected = i
                self.snd_click.play()
                self.execute_option()
                break

    def execute_option(self):
        option = self.options[self.selected]
        if option == "Continuar":
            self.active = False
        elif option == "Opçoes":
            options()
        elif option == "Menu":
            self.jogo.running = False  # sinaliza para o loop principal parar
        elif option == "Sair":
            pygame.quit()
            exit()

    def draw(self, surface):
        # Atualiza alpha para fade-in do fundo
        if self.active and self.bg_alpha < 180:
            self.bg_alpha += self.fade_in_speed * self.jogo.clock.get_time() / 1000
            if self.bg_alpha > 180:
                self.bg_alpha = 180
        elif not self.active and self.bg_alpha > 0:
            self.bg_alpha -= self.fade_in_speed * self.jogo.clock.get_time() / 1000
            if self.bg_alpha < 0:
                self.bg_alpha = 0

        self.bg_surface.fill((0, 0, 0, int(self.bg_alpha)))
        surface.blit(self.bg_surface, (0, 0))

        self.option_rects = []
        center_x = surface.get_width() // 2
        start_y = surface.get_height() // 2 - len(self.options) * 35

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (180, 180, 180)

            # Renderiza texto principal
            text = self.font.render(option, True, color)

            # Renderiza sombra/borda para destacar
            sombra = self.font.render(option, True, (0, 0, 0))
            pos = (center_x - text.get_width() // 2, start_y + i * 70)

            # Desenha sombra
            surface.blit(sombra, (pos[0] + 3, pos[1] + 3))
            # Desenha texto principal
            surface.blit(text, pos)

            # Guarda retângulo para detectar mouse hover/click
            self.option_rects.append(pygame.Rect(pos[0], pos[1], text.get_width(), text.get_height()))
