import math,sys,random,pygame

from core.assets import load_images, load_sounds,load_fonts
from core.constants import WHITE, RED
from core.utils import blit_centered_image, update_score
from screens import leaderboard_screen

def run_game(player_name):
    pygame.init()
    fonts = load_fonts()
    font = fonts["small"]

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Mittens the Mischievous Cafe Destroyer")
    clock = pygame.time.Clock()

    sounds = load_sounds()
    images= load_images()

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
    cat_width, cat_height = 130, 110
    drop_timer = 0
    mouse_timer = 0
    tray_speed = 10
    cups = []
    mice = []
    score = 0
    lives = 3
    disco_mode = False
    disco_timer = 0
    sounds["glass_ding"].set_volume(0.6)
    sounds["game_music"].play(-1)

    cat = pygame.Rect(0, 0, 1, 1)
    tray = pygame.Rect(0, 0, 1, 1)

    def drunk_distortion(surface, t):
        width, height = surface.get_size()
        distorted = pygame.Surface((width, height))
        for y in range(height):
            offset = int(math.sin(y / 30.0 + t / 200.0) * 8)
            src_rect = pygame.Rect(0, y, width, 1)
            dst_rect = pygame.Rect(offset, y, width, 1)
            distorted.blit(surface, dst_rect, src_rect)
        return distorted

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

############# DEBUG / DEMO #############
        if keys[pygame.K_1]:
            score = 0
        if keys[pygame.K_2]:
            score = 20
        if keys[pygame.K_3]:
            score = 50
        if keys[pygame.K_4]:
            score = 75
        if keys[pygame.K_5]:
            score = 100
########################################

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

        input_left = pygame.K_LEFT
        input_right = pygame.K_RIGHT

        if score >= 80:
            input_left, input_right = input_right, input_left

        tray.y = bg_rect.bottom - int(bg_rect.height * 0.17)
        TRAY_EDGE_MARGIN = int(bg_rect.width * 0.02)

        if keys[input_left] and tray.left > bg_rect.left + TRAY_EDGE_MARGIN:
            tray.x -= tray_speed
        if keys[input_right] and tray.right < bg_rect.right - TRAY_EDGE_MARGIN:
            tray.x += tray_speed

        if tray.width == 1:
            tray.width, tray.height = tray_scaled.get_size()
            tray.x = bg_rect.centerx - tray.width // 2

        drop_timer += 1
        min_interval = 60
        max_interval = 160 - int(score * 0.3)
        max_interval = max(min_interval, max_interval)
        base_speed = 3.0
        bonus = min(score * 0.015, 3.0)
        if drop_timer > random.randint(min_interval, max_interval):
            cups.append({
                "rect": pygame.Rect(cat.centerx, cat.bottom, int(37 * scale_factor), int(37 * scale_factor)),
                "angle": random.randint(-15, 15),
                "speed": random.uniform(base_speed + bonus, base_speed + 3 + bonus / 2),
                "state": "falling",
                "timer": 0
            })
            drop_timer = 0

        mouse_timer += 1
        mouse_min_interval = 900
        mouse_max_interval = max(1100, 1600 - score * 3)
        if mouse_timer > random.randint(mouse_min_interval, mouse_max_interval):
            mouse_x = cat.centerx + random.choice([-200, 200])
            mouse_x = max(bg_rect.left + 50, min(bg_rect.right - 50, mouse_x))
            mice.append({
                "rect": pygame.Rect(mouse_x, cat.bottom, int(82 * scale_factor), int(59 * scale_factor)),
                "speed": random.uniform(6.0, 9.0),
                "angle": random.randint(-10, 10)
            })
            mouse_timer = 0

        for cup in cups[:]:
            rect = cup["rect"]
            if cup["state"] == "falling":
                rect.y += cup["speed"]
                if rect.colliderect(tray):
                    sounds["glass_ding"].play()
                    score += 1
                    if score >= 50:
                        disco_mode = True
                    cups.remove(cup)
                    cat_speed = min(cat_base_speed + (score // 10), cat_max_speed)
                elif rect.bottom >= bg_rect.bottom:
                    sounds["glass_break"].play()
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
                sounds["mouse_sound"].play()
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
            sounds["game_music"].stop()

            pygame.display.flip()
            frozen_frame = screen.copy()

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))


            channel = sounds["game_over"].play()

            for alpha in range(0, 220, 5):
                screen.blit(frozen_frame, (0, 0))
                overlay.set_alpha(alpha)
                screen.blit(overlay, (0, 0))

                over_text = font.render("GAME OVER", True, RED)
                text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(over_text, text_rect)

                pygame.display.flip()
                pygame.time.delay(30)

            if channel is not None:
                while channel.get_busy():
                    pygame.time.wait(100)

            pygame.time.wait(500)

            update_score(player_name, score)
            pygame.mixer.stop()

            leaderboard_screen.run_screen(current_player_name=player_name)

            return

        if score >= 80:
            distorted = drunk_distortion(screen, pygame.time.get_ticks())
            screen.blit(distorted, (0, 0))

        pygame.display.flip()
        clock.tick(60)
