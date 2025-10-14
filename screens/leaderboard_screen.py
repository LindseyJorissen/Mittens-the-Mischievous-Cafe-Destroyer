import pygame
import sys
import json
import os
from core.constants import IMG_DIR,load_fonts
from core.utils import blit_centered_image

def run_screen():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Leaderboard")

    bg_path = os.path.join(IMG_DIR, "leaderboard.jpeg")
    bg = pygame.image.load(bg_path).convert()


    fonts = load_fonts()
    hint_font = fonts["small"]
    font_entry = fonts["medium"]
    font_title = fonts["large"]

    leaderboard_path = os.path.join(os.path.dirname(__file__), "..", "data", "scores.json")
    leaderboard_path = os.path.normpath(leaderboard_path)

    scores = []
    if os.path.exists(leaderboard_path):
        with open(leaderboard_path, "r") as f:
            try:
                data = json.load(f)
                scores = sorted(data["players"], key=lambda x: x["score"], reverse=True)[:6]
            except Exception as e:
                print("Error reading leaderboard:", e)
                scores = []


    color_title = (255, 230, 160) # warm gold
    color_entry = (255, 255, 255) # white

    running = True
    while running:
        screen.fill((0, 0, 0))
        bg_rect = blit_centered_image(screen, bg)

        title_surface = font_title.render("TOP SCORES", True, color_title)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, bg_rect.y + 200))
        screen.blit(title_surface, title_rect)

        start_y = bg_rect.y + 330
        spacing = 80

        if not scores:
            no_score = font_entry.render("No scores yet!", True, color_entry)
            rect = no_score.get_rect(center=(WIDTH // 2, start_y))
            screen.blit(no_score, rect)
        else:
            for i, entry in enumerate(scores):
                name = entry["name"]
                score = entry["score"]
                text = f"{i+1}. {name:<10}  {score:>5}"
                surf = font_entry.render(text, True, color_entry)
                rect = surf.get_rect(center=(WIDTH // 2, start_y + i * spacing))
                screen.blit(surf, rect)

        hint_text = hint_font.render("Press ESC to return", True, (255, 230, 160))
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        screen.blit(hint_text, hint_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)
