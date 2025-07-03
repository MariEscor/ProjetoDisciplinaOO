import pygame
import constants

class MessageScene:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
        pygame.display.set_caption("Aviso")
        self._font = pygame.font.SysFont(None, 36)
        self._clock = pygame.time.Clock()

    @property
    def screen(self):
        return self._screen

    @property
    def font(self):
        return self._font

    def show_message(self, text: str):
        message = self._font.render(text, True, constants.BLACK)
        message_rect = message.get_rect(center=(constants.LARGURA_JANELA // 2, constants.ALTURA_JANELA // 2))

        running = True
        while running:
            self._screen.fill(constants.WHITE)
            self._screen.blit(message, message_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()
