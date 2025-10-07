import sys
import random
import pygame
from core.assets import load_images, load_sounds
from core.constants import WHITE, RED, IMG_DIR, SOUND_DIR, load_fonts
from core.utils import blit_centered_image

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

def run_game():
    pygame.init()
    fonts = load_fonts()
    font = fonts["small"]

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Mittens the Mischievous Cafe Destroyer")
    clock = pygame.time.Clock()

    glass_ding, glass_break, game_music, mouse_sound, menu_music, door_creak = load_sounds(SOUND_DIR)
    images, cat_width, cat_height = load_images(IMG_DIR, WIDTH, HEIGHT)
    background_bar = images["background"]
    disco_bg1 = images["disco_bg1"]
    disco_bg2 = images["disco_bg2"]
    beer_img = images["beer"]
    broken_beer_img = images["broken_beer"]
    mouse_img = images["mouse"]
    tray_img = images["tray"]
    cat_frames = images["cat_frames"]

    cat_speed = 1.4
    cat_base_speed = 1.4
    cat_max_speed = 7
    cat_dir = 1
    drop_timer = 0
    mouse_timer = 0
    tray_speed = 10
    cups = []
    mice = []
    score = 0
    lives = 3
    disco_mode = False
    disco_timer = 0
    glass_ding.set_volume(0.6)
    game_music.play(-1)

    cat = pygame.Rect(0, 0, 1, 1)
    tray = pygame.Rect(0, 0, 1, 1)

    while True:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        if disco_mode:
            disco_timer += 1
            bg = disco_bg1 if (pygame.time.get_ticks() // 200) % 2 == 0 else disco_bg2
        else:
            bg = background_bar

        bg_rect = blit_centered_image(screen, bg)

        scale_factor = bg_rect.height / 700
        cat_scaled = [pygame.transform.smoothscale(f, (int(cat_width * scale_factor), int(cat_height * scale_factor))) for f in cat_frames]
        tray_scaled = pygame.transform.smoothscale(tray_img, (int(270 * scale_factor), int(110 * scale_factor)))
        beer_scaled = pygame.transform.smoothscale(beer_img, (int(90 * scale_factor), int(90 * scale_factor)))
        broken_scaled = pygame.transform.smoothscale(broken_beer_img, (int(110 * scale_factor), int(110 * scale_factor)))
        mouse_scaled = pygame.transform.smoothscale(mouse_img, (int(50 * scale_factor), int(160 * scale_factor)))

        cat_anim_timer = pygame.time.get_ticks() / 1000.0 * 0.15
        cat_frame_index = int(cat_anim_timer) % len(cat_scaled)

        if cat.width == 1:
            cat.width, cat.height = cat_scaled[0].get_size()
            cat.x = bg_rect.left + int(bg_rect.width * 0.05)
            cat.y = bg_rect.top + int(bg_rect.height * 0.12)

        cat.x += cat_speed * cat_dir

        CAT_LEFT_MARGIN = int(bg_rect.width * 0.02)
        CAT_RIGHT_MARGIN = int(bg_rect.width * 0.12)
        if cat.right >= bg_rect.right - CAT_RIGHT_MARGIN or cat.left <= bg_rect.left + CAT_LEFT_MARGIN:
            cat_dir *= -1

        if tray.width == 1:
            tray.width, tray.height = tray_scaled.get_size()
            tray.x = bg_rect.centerx - tray.width // 2

        tray.y = bg_rect.bottom - int(bg_rect.height * 0.17)
        TRAY_EDGE_MARGIN = int(bg_rect.width * 0.02)
        if keys[pygame.K_LEFT] and tray.left > bg_rect.left + TRAY_EDGE_MARGIN:
            tray.x -= tray_speed
        if keys[pygame.K_RIGHT] and tray.right < bg_rect.right - TRAY_EDGE_MARGIN:
            tray.x += tray_speed

        drop_timer += 1
        if drop_timer > random.randint(80, 160):
            cups.append({
                "rect": pygame.Rect(cat.centerx, cat.bottom, int(37 * scale_factor), int(37 * scale_factor)),
                "angle": random.randint(-15, 15),
                "speed": random.uniform(3.0, 6.0),
                "state": "falling",
                "timer": 0
            })
            drop_timer = 0

        mouse_timer += 1
        if mouse_timer > random.randint(600, 1200):
            mice.append({
                "rect": pygame.Rect(cat.centerx, cat.bottom, int(82 * scale_factor), int(59 * scale_factor)),
                "speed": random.uniform(7.0, 10.0),
                "angle": random.randint(-10, 10)
            })
            mouse_timer = 0

        for cup in cups[:]:
            rect = cup["rect"]
            if cup["state"] == "falling":
                rect.y += cup["speed"]
                if rect.colliderect(tray):
                    glass_ding.play()
                    score += 1
                    if score >= 50:
                        disco_mode = True
                    cups.remove(cup)
                    cat_speed = min(cat_base_speed + (score // 10), cat_max_speed)
                elif rect.bottom >= bg_rect.bottom:
                    glass_break.play()
                    lives -= 1
                    cup["state"] = "broken"
                    cup["timer"] = 8
                    rect.bottom = bg_rect.bottom - int(bg_rect.height * 0.05)
                    cup["speed"] = 0
                    cup["angle"] = random.randint(-5, 5)
            elif cup["state"] == "broken":
                cup["timer"] -= 1
                if cup["timer"] <= 0:
                    cups.remove(cup)

        screen.blit(tray_scaled, tray.topleft)

        current_cat_image = cat_scaled[cat_frame_index]
        if cat_dir == -1:
            current_cat_image = pygame.transform.flip(current_cat_image, True, False)
        screen.blit(current_cat_image, cat.topleft)

        for cup in cups:
            rotated = pygame.transform.rotate(
                beer_scaled if cup["state"] == "falling" else broken_scaled,
                cup["angle"]
            )
            rotated_rect = rotated.get_rect(center=cup["rect"].center)
            screen.blit(rotated, rotated_rect.topleft)

        for m in mice[:]:
            rect = m["rect"]
            rect.x += random.choice([-1, 0, 1])
            rect.y += m["speed"]

            if rect.colliderect(tray):
                mouse_sound.play()
                score = max(0, score - 2)
                lives -= 1
                mice.remove(m)
            elif rect.top > bg_rect.bottom:
                mice.remove(m)

        for m in mice:
            screen.blit(mouse_scaled, m["rect"].topleft)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        hud_y = bg_rect.top + 20
        screen.blit(score_text, (bg_rect.left + 20, hud_y))
        screen.blit(lives_text, (bg_rect.right - lives_text.get_width() - 20, hud_y))

        if lives <= 0:
            over_text = font.render("GAME OVER", True, RED)
            screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.mixer.stop()
            return

        pygame.display.flip()
        clock.tick(60)
