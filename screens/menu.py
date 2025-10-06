import pygame
import sys
import os
from screens import cafe_destroyer
from core.assets import load_images, load_sounds
from core.constants import WIDTH, HEIGHT, WHITE, YELLOW, IMG_DIR, SOUND_DIR,load_fonts

def run_menu():
    pygame.init()

    fonts = load_fonts()
    font_large = fonts["large"]
    font_small = fonts["medium"]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mittens - Main Menu")
    clock = pygame.time.Clock()

    images, cat_width, cat_height = load_images(IMG_DIR, WIDTH, HEIGHT)
    menu_bg = images["menu_bg"]

    glass_ding, glass_break, game_music, mouse_sound,menu_music = load_sounds(SOUND_DIR)

    menu_music.set_volume(0.5)
    menu_music.play(-1)

    button_img = pygame.image.load(os.path.join(IMG_DIR, "button.png")).convert()
    button_img = pygame.transform.scale(button_img, (250, 150))

    def draw_button(text, center, image, mouse_pos):
        rect = image.get_rect(center=center)
        is_hovered = rect.collidepoint(mouse_pos)

        if is_hovered:
            hover_img = image.copy()
            hover_img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(hover_img, rect.topleft)
        else:
            screen.blit(image, rect.topleft)

        label = font_small.render(text, True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        return rect, is_hovered

    while True:
        screen.blit(menu_bg, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)  # transparency: 0–255
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        title = font_large.render("Mittens the Mischievous", True, YELLOW)
        subtitle = font_large.render("Cafe Destroyer", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 260))

        play_button, hovered = draw_button("PLAY", (WIDTH // 2, 450), button_img, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hovered:
                    menu_music.stop()
                    cafe_destroyer.run_game()
                    menu_music.play(-1)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                menu_music.stop()
                cafe_destroyer.run_game()
                menu_music.play(-1)

        pygame.display.flip()
        clock.tick(60)
