import os
import pygame

def load_images(img_dir, width, height):
    images = {}

    # Background
    bg = pygame.image.load(os.path.join(img_dir, "background_bar.jpeg")).convert()
    images["background"] = pygame.transform.scale(bg, (width, height))

    # Beer
    beer = pygame.image.load(os.path.join(img_dir, "beer.png")).convert_alpha()
    images["beer"] = pygame.transform.scale(beer, (90, 90))

    # Broken beer
    broken = pygame.image.load(os.path.join(img_dir, "broken_beer.png")).convert_alpha()
    images["broken_beer"] = pygame.transform.scale(broken, (110, 110))

    # Mouse
    mouse = pygame.image.load(os.path.join(img_dir, "mouse.png")).convert_alpha()
    images["mouse"] = pygame.transform.scale(mouse, (50, 160))

    # Tray
    tray = pygame.image.load(os.path.join(img_dir, "tray_with_hands.png")).convert_alpha()
    images["tray"] = pygame.transform.scale(tray, (270, 110))

    # Cat frames
    cat_width, cat_height = 140, 120
    images["cat_frames"] = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(img_dir, f"cat_walk{i}.png")).convert_alpha(),
            (cat_width, cat_height)
        )
        for i in range(1, 3)
    ]
    return images, cat_width, cat_height


def load_sounds(sound_dir):

    glass_ding = pygame.mixer.Sound(os.path.join(sound_dir, "glass_ding.wav"))
    glass_break = pygame.mixer.Sound(os.path.join(sound_dir, "glass_break.wav"))
    game_music = pygame.mixer.Sound(os.path.join(sound_dir, "game_music.wav"))
    mouse_sound = pygame.mixer.Sound(os.path.join(sound_dir, "mouse.wav"))

    return glass_ding, glass_break, game_music, mouse_sound
