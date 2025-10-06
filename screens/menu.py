import pygame
import sys
from screens import cafe_destroyer

def run_menu():
    pygame.init()
    WIDTH, HEIGHT = 1000, 700
    WHITE = (255, 255, 255)
    YELLOW = (255, 215, 0)
    GREY = (50, 50, 50)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mittens - Main Menu")
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 50)

    def draw_button(text, center, width, height, color, hover_color, mouse_pos):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = center
        is_hovered = rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, hover_color if is_hovered else color, rect, border_radius=15)
        label = font_small.render(text, True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        return rect, is_hovered

    while True:
        screen.fill(GREY)
        mouse_pos = pygame.mouse.get_pos()

        title = font_large.render("Mittens the Mischievous", True, YELLOW)
        subtitle = font_large.render("Cafe Destroyer", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 260))

        play_button, hovered = draw_button("PLAY", (WIDTH//2, 450), 250, 80, (150, 100, 250), (180, 130, 255), mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and hovered:
                cafe_destroyer.run_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cafe_destroyer.run_game()

        pygame.display.flip()
        clock.tick(60)
