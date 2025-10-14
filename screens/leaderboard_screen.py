import pygame
import sys
import json
import os
from core.constants import GOLD,WHITE,LEADERBOARD_FILE,YELLOW
from core.utils import blit_centered_image
from core.assets import load_images,load_fonts

def run_screen(current_player_name=None):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Leaderboard")

    images= load_images()
    bg = images["leaderboard"]

    fonts = load_fonts()
    hint_font = fonts["small"]
    font_entry = fonts["medium"]
    font_title = fonts["large"]

    scores = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                data = json.load(f)
                scores = sorted(data["players"], key=lambda x: x["score"], reverse=True)[:6]
            except Exception as e:
                print("Error reading leaderboard:", e)
                scores = []

    running = True
    while running:
        screen.fill((0, 0, 0))
        bg_rect = blit_centered_image(screen, bg)

        title_surface = font_title.render("TOP SCORES", True, GOLD)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, bg_rect.y + 150))
        screen.blit(title_surface, title_rect)

        start_y = bg_rect.y + 330
        spacing = 80

        if not scores:
            no_score = font_entry.render("No scores yet!", True, WHITE)
            rect = no_score.get_rect(center=(WIDTH // 2, start_y))
            screen.blit(no_score, rect)
        else:
            for i, entry in enumerate(scores):
                name = entry["name"]
                score = entry["score"]
                color = YELLOW if name == current_player_name else WHITE

                rank_surf = font_entry.render(f"{i + 1}.", True, color)
                name_surf = font_entry.render(name.upper(), True, color)
                score_surf = font_entry.render(str(score), True, color)

                y = start_y + i * spacing

                rank_x = WIDTH // 2 - 320
                name_x = WIDTH // 2 - 130
                score_x = WIDTH // 2 + 310

                screen.blit(rank_surf, (rank_x, y))
                screen.blit(name_surf, (name_x, y))
                screen.blit(score_surf, (score_x - score_surf.get_width(), y))

        hint_text = hint_font.render("Press ESC to return", True, GOLD)
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(hint_text, hint_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)
