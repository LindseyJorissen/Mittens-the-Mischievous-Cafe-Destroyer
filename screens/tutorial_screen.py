import pygame
import sys
from core.assets import load_images, load_fonts
from core.constants import GOLD
from core.utils import blit_centered_image

def run_tutorial():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Tutorial")
    clock = pygame.time.Clock()

    images = load_images()
    fonts = load_fonts()

    tutorial_bg = images["tutorial"]
    hint_font = fonts["small"]

    running = True
    blink_timer = 0

    while running:
        bg_rect = blit_centered_image(screen, tutorial_bg)

        blink_timer += 1
        if (blink_timer // 30) % 2 == 0:  #every 0.5sec
            hint_surface = hint_font.render("Press any key to start", True, GOLD)
            hint_rect = hint_surface.get_rect(center=(bg_rect.centerx, bg_rect.bottom - 120))
            screen.blit(hint_surface, hint_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        pygame.display.flip()
        clock.tick(60)
