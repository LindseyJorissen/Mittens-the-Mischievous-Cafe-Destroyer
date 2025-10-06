import os
import sys
import random
import pygame
from core.assets import load_images, load_sounds

def run_game():
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    WHITE = (255, 255, 255)
    RED = (200, 50, 50)

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
    SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mittens the Mischievous Cafe Destroyer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    # Load everything
    glass_ding, glass_break, game_music, mouse_sound = load_sounds(SOUND_DIR)
    images, cat_width, cat_height = load_images(IMG_DIR, WIDTH, HEIGHT)

    background_bar = images["background"]
    beer_img = images["beer"]
    broken_beer_img = images["broken_beer"]
    mouse_img = images["mouse"]
    tray_img = images["tray"]
    cat_frames = images["cat_frames"]

    cat_y = 140 - 65
    cat_frame_index = 0
    cat_anim_timer = 0
    cat_anim_speed = 0.15
    cat = pygame.Rect(WIDTH // 2 - cat_width // 2, cat_y, cat_width, cat_height)
    cat_speed = 1
    cat_base_speed = 1
    cat_max_speed = 5
    cat_dir = 1
    drop_timer = 0
    mouse_timer = 0

    tray_width, tray_height = 200,70
    tray = pygame.Rect(WIDTH // 2 - tray_width // 2, HEIGHT - 120, tray_width, tray_height)
    tray_speed = 7

    glass_ding.set_volume(0.6)

    cups = []
    cup_size = 25
    mice = []
    score = 0
    lives = 3

    game_music.play(-1)

    while True:
        screen.blit(background_bar, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Cat animation
        cat_anim_timer += cat_anim_speed
        if cat_anim_timer >= 1:
            cat_anim_timer = 0
            cat_frame_index = (cat_frame_index + 1) % len(cat_frames)

        # Cat movement
        cat.x += cat_speed * cat_dir
        if cat.right >= WIDTH - 140 or cat.left <= 0:
            cat_dir *= -1

        # Drop beers
        drop_timer += 1
        if drop_timer > random.randint(80, 160):
            cups.append({
                "rect": pygame.Rect(cat.centerx, cat.bottom, cup_size, cup_size),
                "angle": random.randint(-15, 15),
                "speed": random.uniform(2.0, 4.0),
                "state": "falling",
                "timer": 0
            })
            drop_timer = 0

        # Drop mice
        mouse_timer += 1
        if mouse_timer > random.randint(600, 1200):
            mice.append({
                "rect": pygame.Rect(cat.centerx, cat.bottom, 60, 40),
                "speed": random.uniform(5.0, 7.0),
                "angle": random.randint(-10, 10)
            })
            mouse_timer = 0

        # Tray movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and tray.left > 0:
            tray.x -= tray_speed
        if keys[pygame.K_RIGHT] and tray.right < WIDTH:
            tray.x += tray_speed

        # Update cups
        for cup in cups[:]:
            rect = cup["rect"]
            if cup["state"] == "falling":
                rect.y += cup["speed"]

                if rect.colliderect(tray):
                    glass_ding.play()
                    score += 1
                    cups.remove(cup)
                    cat_speed = min(cat_base_speed + (score // 10), cat_max_speed)

                elif rect.bottom >= HEIGHT - 10:
                    glass_break.play()
                    lives -= 1
                    cup["state"] = "broken"
                    cup["timer"] = 8
                    rect.bottom = HEIGHT - 50
                    cup["speed"] = 0
                    cup["angle"] = random.randint(-5, 5)

            elif cup["state"] == "broken":
                cup["timer"] -= 1
                if cup["timer"] <= 0:
                    cups.remove(cup)

        # Update mice
        for m in mice[:]:
            rect = m["rect"]
            rect.y += m["speed"]

            if rect.colliderect(tray):
                mouse_sound.play()
                score = max(0, score - 2)
                lives -= 1
                mice.remove(m)
            elif rect.top > HEIGHT:
                mice.remove(m)

        # Draw everything
        screen.blit(tray_img, tray.topleft)
        current_cat_image = cat_frames[cat_frame_index]
        if cat_dir == -1:
            current_cat_image = pygame.transform.flip(current_cat_image, True, False)
        screen.blit(current_cat_image, cat.topleft)

        for cup in cups:
            rotated = beer_img if cup["state"] == "falling" else broken_beer_img
            rotated_rect = rotated.get_rect(center=cup["rect"].center)
            screen.blit(rotated, rotated_rect.topleft)

        for m in mice:
            rotated_mouse = pygame.transform.rotate(mouse_img, m["angle"])
            rotated_rect = rotated_mouse.get_rect(center=m["rect"].center)
            screen.blit(rotated_mouse, rotated_rect.topleft)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

        if lives <= 0:
            over_text = font.render("GAME OVER", True, RED)
            screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        pygame.display.flip()
        clock.tick(60)
