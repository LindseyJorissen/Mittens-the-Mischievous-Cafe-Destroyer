import os
import sys
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
RED = (200, 50, 50)

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mittens the Mischievous Cafe Destroyer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

def load_images():
    images = {}

    # Background
    bg = pygame.image.load(os.path.join(IMG_DIR, "background_bar.jpeg")).convert()
    images["background"] = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # Beer
    beer = pygame.image.load(os.path.join(IMG_DIR, "beer.png")).convert_alpha()
    images["beer"] = pygame.transform.scale(beer, (90, 90))

    # Broken beer
    broken = pygame.image.load(os.path.join(IMG_DIR, "broken_beer.png")).convert_alpha()
    images["broken_beer"] = pygame.transform.scale(broken, (110, 110))

    # Mouse
    mouse = pygame.image.load(os.path.join(IMG_DIR, "mouse.png")).convert_alpha()
    images["mouse"] = pygame.transform.scale(mouse, (50, 160))

    # Tray
    tray = pygame.image.load(os.path.join(IMG_DIR, "tray_with_hands.png")).convert_alpha()
    images["tray"] = pygame.transform.scale(tray, (270, 110))

    # Cat frames
    cat_width, cat_height = 140, 120
    images["cat_frames"] = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(IMG_DIR, f"cat_walk{i}.png")).convert_alpha(),
            (cat_width, cat_height)
        )
        for i in range(1, 3)
    ]

    return images, cat_width, cat_height
def load_sounds():
    glass_ding = pygame.mixer.Sound(os.path.join(SOUND_DIR, "glass_ding.wav"))
    glass_break = pygame.mixer.Sound(os.path.join(SOUND_DIR, "glass_break.wav"))
    game_music = pygame.mixer.Sound(os.path.join(SOUND_DIR, "game_music.wav"))
    mouse_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "mouse.wav"))


    return glass_ding, glass_break, game_music,mouse_sound

glass_ding, glass_break, game_music,mouse_sound = load_sounds()

images, cat_width, cat_height = load_images()
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

#volume
glass_ding.set_volume(0.6)  # volume 0.0 - 1.0

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

    cat_anim_timer += cat_anim_speed
    if cat_anim_timer >= 1:
        cat_anim_timer = 0
        cat_frame_index = (cat_frame_index + 1) % len(cat_frames)

    cat.x += cat_speed * cat_dir
    if cat.right >= WIDTH - 140 or cat.left <= 0:
        cat_dir *= -1

    drop_timer += 1
    if drop_timer > random.randint(80, 160):
        cups.append({
            "rect": pygame.Rect(cat.centerx, cat.bottom, cup_size, cup_size),
            "angle": random.randint(-15, 15),
            "speed": random.uniform(2.0, 4.0),
            "state": "falling",  # "falling" or "broken"
            "timer": 0
        })
        drop_timer = 0

    mouse_timer += 1
    if mouse_timer > random.randint(600, 1200):  # every 10–20 seconds
        mice.append({
            "rect": pygame.Rect(cat.centerx, cat.bottom, 60, 40),
            "speed": random.uniform(5.0, 7.0),
            "angle": random.randint(-10, 10)
        })
        mouse_timer = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and tray.left > 0:
        tray.x -= tray_speed
    if keys[pygame.K_RIGHT] and tray.right < WIDTH:
        tray.x += tray_speed

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
                cup["timer"] = 8  # show for x frames
                rect.bottom = HEIGHT - 50
                cup["speed"] = 0
                cup["angle"] = random.randint(-5, 5)

        elif cup["state"] == "broken":
            cup["timer"] -= 1
            if cup["timer"] <= 0:
                cups.remove(cup)

    for mouse in mice[:]:
        rect = mouse["rect"]
        rect.y += mouse["speed"]

        if rect.colliderect(tray):
            mouse_sound.play()
            score = max(0, score - 2)
            lives -= 1
            mice.remove(mouse)

        elif rect.top > HEIGHT:
            mice.remove(mouse)

    screen.blit(tray_img, tray.topleft)

    current_cat_image = cat_frames[cat_frame_index]
    if cat_dir == -1:
        current_cat_image = pygame.transform.flip(current_cat_image, True, False)
    screen.blit(current_cat_image, cat.topleft)

    for cup in cups:
        if cup["state"] == "falling":
            rotated = pygame.transform.rotate(beer_img, cup["angle"])
        else:
            rotated = broken_beer_img

        rotated_rect = rotated.get_rect(center=cup["rect"].center)
        screen.blit(rotated, rotated_rect.topleft)

    for mouse in mice:
        rotated_mouse = pygame.transform.rotate(mouse_img, mouse["angle"])
        rotated_rect = rotated_mouse.get_rect(center=mouse["rect"].center)
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
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)
