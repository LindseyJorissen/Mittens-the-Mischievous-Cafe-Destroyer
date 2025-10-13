import pygame
import sys

def run_screen():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Leaderboard")

    font = pygame.font.SysFont(None, 80)
    text = font.render("Leaderboard - Coming Soon!", True, (255, 255, 255))
    text_rect = text.get_rect(center=screen.get_rect().center)

    while True:
        screen.fill((30, 30, 30))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)
