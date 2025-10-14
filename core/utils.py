import pygame
import json
import os
from core.constants import LEADERBOARD_FILE

def update_score(player_name, new_score):

    os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)

    data = {"players": []}
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    player_found = False
    for player in data["players"]:
        if player["name"].strip() == player_name.strip():
            player["score"] = max(player["score"], new_score)
            player_found = True
            break

    if not player_found:
        data["players"].append({"name": player_name, "score": new_score})

    data["players"].sort(key=lambda x: x["score"], reverse=True)

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def blit_centered_image(screen, image):
    screen_width, screen_height = screen.get_size()
    img_width, img_height = image.get_size()
    img_aspect = img_width / img_height
    screen_aspect = screen_width / screen_height

    if img_aspect > screen_aspect:
        new_width = screen_width
        new_height = int(screen_width / img_aspect)
        x, y = 0, (screen_height - new_height) // 2
    else:
        new_height = screen_height
        new_width = int(screen_height * img_aspect)
        x, y = (screen_width - new_width) // 2, 0

    scaled = pygame.transform.smoothscale(image, (new_width, new_height))
    screen.fill((0, 0, 0))
    screen.blit(scaled, (x, y))
    return pygame.Rect(x, y, new_width, new_height)
