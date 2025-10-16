import pygame
import sys
import json
import os
from core.constants import LEADERBOARD_FILE, GOLD, BROWN_SHADOW , DEBUG_RED,DEBUG_RED_OVERLAY
from core.utils import blit_centered_image
from core.assets import load_images,load_fonts,load_sounds

def run_name_entry():
    debug_toggle = False
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    sounds = load_sounds()

    images= load_images()
    bg = images["name_input"]
    bg_rect = blit_centered_image(screen, bg)

    fonts = load_fonts()
    hint_font = fonts["small"]
    font = fonts["medium"]

    name = ""
    running = True

    base_buttons = {
        'A': pygame.Rect(205, 335, 65, 75),
        'B': pygame.Rect(285, 335, 65, 75),
        'C': pygame.Rect(365, 335, 65, 75),
        'D': pygame.Rect(445, 335, 65, 75),
        'E': pygame.Rect(525, 335, 65, 75),
        'F': pygame.Rect(605, 335, 65, 75),
        'G': pygame.Rect(685, 335, 65, 75),
        'H': pygame.Rect(205, 428, 65, 75),
        'I': pygame.Rect(285, 428, 65, 75),
        'J': pygame.Rect(365, 428, 65, 75),
        'K': pygame.Rect(445, 428, 65, 75),
        'L': pygame.Rect(525, 428, 65, 75),
        'M': pygame.Rect(605, 428, 65, 75),
        'N': pygame.Rect(685, 428, 65, 75),
        'O': pygame.Rect(205, 521, 65, 75),
        'P': pygame.Rect(285, 521, 65, 75),
        'Q': pygame.Rect(365, 521, 65, 75),
        'R': pygame.Rect(445, 521, 65, 75),
        'S': pygame.Rect(525, 521, 65, 75),
        'T': pygame.Rect(605, 521, 65, 75),
        'U': pygame.Rect(205, 618, 65, 75),
        'V': pygame.Rect(285, 618, 65, 75),
        'W': pygame.Rect(365, 618, 65, 75),
        'X': pygame.Rect(445, 618, 65, 75),
        'Y': pygame.Rect(525, 618, 65, 75),
        'Z': pygame.Rect(605, 618, 65, 75),
        'SPACE': pygame.Rect(685, 521, 130, 75),
        'READY': pygame.Rect(685, 200, 130, 75),
        'UNDO': pygame.Rect(685, 618, 130, 75),

    }

    orig_w, orig_h = 1024, 768
    sx = WIDTH / orig_w
    sy = HEIGHT / orig_h
    buttons = {
        k: pygame.Rect(int(v.x * sx), int(v.y * sy), int(v.width * sx), int(v.height * sy))
        for k, v in base_buttons.items()
    }

    while running:
        bg_rect = blit_centered_image(screen, bg)

        name_surface = font.render(name, True, GOLD)
        name_rect = name_surface.get_rect(
            center=(bg_rect.centerx - 110, bg_rect.centery - 200)
        )
        screen.blit(name_surface, name_rect)

        mouse_pos = pygame.mouse.get_pos()
        for label, rect in buttons.items():
            if rect.collidepoint(mouse_pos):
                shadow = pygame.Surface(rect.size, pygame.SRCALPHA)
                shadow.fill(BROWN_SHADOW)
                screen.blit(shadow, rect.topleft)

        hint_text = hint_font.render("Press ESC to return", True, GOLD)
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(hint_text, hint_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        sounds["knock_wood"].play()
                        if label == 'SPACE':
                            name += ' '
                        elif label == 'UNDO':
                            if len(name) > 0:
                                name = name[:-1]
                        elif label == 'READY':
                            sounds["cat_meow"].play()
                            if name.strip():
                                save_name(name.strip())
                            return name.strip()
                        else:
                            if len(name) < 12:
                                name += label

        ######### DEBUG HOVER ##########
        if debug_toggle:
            for label, rect in buttons.items():
                pygame.draw.rect(screen, DEBUG_RED, rect, 2)

                overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
                overlay.fill(DEBUG_RED_OVERLAY)
                screen.blit(overlay, rect.topleft)
        ################################

        pygame.display.flip()
        clock.tick(60)


def save_name(name):
    os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)
    data = {"players": []}
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
    if name not in [p["name"] for p in data["players"]]:
        data["players"].append({"name": name, "score": 0})
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)
