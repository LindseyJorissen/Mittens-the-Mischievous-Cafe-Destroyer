import pygame
import sys
from screens import cafe_destroyer,leaderboard_screen
from core.assets import load_images, load_sounds
from core.constants import BROWN_SHADOW
from core.utils import blit_centered_image

def run_menu():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Mittens - Main Menu")
    clock = pygame.time.Clock()

    images = load_images()
    pub_closed = images["pub_closed"]
    pub_open = images["pub_open"]

    sounds = load_sounds()
    menu_music = sounds["menu_music"]

    menu_music.set_volume(0.5)
    menu_music.play(-1)

    door_hovered_last = False
    base_door_rect = pygame.Rect(255, 370, 260, 490)
    base_leaderboard_rect = pygame.Rect(820, 185, 390, 130)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        image_rect = blit_centered_image(screen, pub_closed)
        orig_w, orig_h = pub_closed.get_size()

        sx = image_rect.width / orig_w
        sy = image_rect.height / orig_h

        door_rect = pygame.Rect(
            int(image_rect.x + base_door_rect.x * sx),
            int(image_rect.y + base_door_rect.y * sy),
            int(base_door_rect.width * sx),
            int(base_door_rect.height * sy)
        )
        leaderboard_rect = pygame.Rect(
            int(image_rect.x + base_leaderboard_rect.x * sx),
            int(image_rect.y + base_leaderboard_rect.y * sy),
            int(base_leaderboard_rect.width * sx),
            int(base_leaderboard_rect.height * sy)
        )

        is_hovered = door_rect.collidepoint(mouse_pos)

        if is_hovered:
            blit_centered_image(screen, pub_open)
            if not door_hovered_last:
                sounds["door_creak"].play()
            door_hovered_last = True
        else:
            blit_centered_image(screen, pub_closed)
            door_hovered_last = False

        if leaderboard_rect.collidepoint(mouse_pos):
            if not leaderboard_hovered_last:
                sounds["knock_wood"].play()
            leaderboard_hovered_last = True
            shadow = pygame.Surface(leaderboard_rect.size, pygame.SRCALPHA)
            shadow.fill(BROWN_SHADOW)  # translucent black overlay
            screen.blit(shadow, leaderboard_rect.topleft)
        else:
            leaderboard_hovered_last = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if door_rect.collidepoint(mouse_pos):
                    menu_music.stop()
                    from screens import name_entry
                    player_name = name_entry.run_name_entry()
                    if player_name:
                        cafe_destroyer.run_game(player_name)
                        menu_music.play(-1)
                elif leaderboard_rect.collidepoint(mouse_pos):
                    menu_music.stop()
                    leaderboard_screen.run_screen()
                    menu_music.play(-1)

        pygame.display.flip()
        clock.tick(60)
