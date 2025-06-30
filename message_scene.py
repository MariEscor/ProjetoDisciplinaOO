import pygame
import constants

def show_message_scene(text: str):
    pygame.init()
    screen = pygame.display.set_mode((constants.LARGURA_JANELA, constants.ALTURA_JANELA))
    pygame.display.set_caption("Aviso")
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Cria a superfície da mensagem
    message = font.render(text, True, constants.BLACK)
    message_rect = message.get_rect(center=(constants.LARGURA_JANELA // 2, constants.ALTURA_JANELA // 2))

    running = True
    while running:
        screen.fill(constants.WHITE)
        screen.blit(message, message_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
