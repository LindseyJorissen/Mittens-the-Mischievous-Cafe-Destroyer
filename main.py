import pygame, random, sys, os

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")

background_bar = pygame.image.load(os.path.join(IMG_DIR, "background_bar.jpeg")).convert()
background_bar = pygame.transform.scale(background_bar, (WIDTH, HEIGHT))
beer_img = pygame.image.load(os.path.join(IMG_DIR, "beer.png")).convert_alpha()
beer_img = pygame.transform.scale(beer_img, (90, 90))
cat_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "cat_walk1.png")).convert_alpha(), (20, 10)),
    pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "cat_walk2.png")).convert_alpha(), (20, 10))
]
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREY = (100, 100, 100)

cat_width, cat_height = 140, 120
cat_y = 140 - 65

cat_frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_DIR, "cat_walk1.png")).convert_alpha(),
        (cat_width, cat_height)
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_DIR, "cat_walk2.png")).convert_alpha(),
        (cat_width, cat_height)
    )
]

cat_frame_index = 0
cat_anim_timer = 0
cat_anim_speed = 0.15
cat = pygame.Rect(WIDTH // 2 - cat_width // 2, cat_y, cat_width, cat_height)
cat_speed = 1
cat_dir = 1
drop_timer = 0


tray_width, tray_height = 100, 20
tray = pygame.Rect(WIDTH//2 - tray_width//2, HEIGHT - 100, tray_width, tray_height)
tray_speed = 7

cups = []
cup_size = 25

score = 0
lives = 3

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
    RIGHT_LIMIT = WIDTH - 140
    LEFT_LIMIT = 0

    if cat.right >= RIGHT_LIMIT or cat.left <= LEFT_LIMIT:
        cat_dir *= -1

    drop_timer += 1
    if drop_timer > random.randint(80, 160):
        cups.append({
            "rect": pygame.Rect(cat.centerx, cat.bottom, cup_size, cup_size),
            "angle": random.randint(-15, 15),
            "speed": random.uniform(2.0, 4.0)
        })
        drop_timer = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and tray.left > 0:
        tray.x -= tray_speed
    if keys[pygame.K_RIGHT] and tray.right < WIDTH:
        tray.x += tray_speed

    for cup in cups[:]:
        rect = cup["rect"]
        rect.y += cup["speed"]

        if rect.colliderect(tray):
            score += 1
            cups.remove(cup)
        elif rect.bottom >= HEIGHT:
            lives -= 1
            cups.remove(cup)

    pygame.draw.rect(screen, GREY, tray)

    current_cat_image = cat_frames[cat_frame_index]
    if cat_dir == -1:
        current_cat_image = pygame.transform.flip(current_cat_image, True, False)

    screen.blit(current_cat_image, cat.topleft)

    for cup in cups:
        rect = cup["rect"]
        angle = cup["angle"]
        rotated = pygame.transform.rotate(beer_img, angle)
        rotated_rect = rotated.get_rect(center=rect.center)
        screen.blit(rotated, rotated_rect.topleft)

    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

    if lives <= 0:
        over_text = font.render("GAME OVER", True, RED)
        screen.blit(over_text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)
