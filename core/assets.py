import os
import pygame

def load_images(img_dir, width, height):
    images = {}

    #Bar backgrounds
    bg = pygame.image.load(os.path.join(img_dir, "background_bar.jpeg")).convert()
    images["background"] = pygame.transform.scale(bg, (width, height))

    disco_bg1 = pygame.image.load(os.path.join(img_dir, "disco_bg1.jpeg")).convert()
    images["disco_bg1"] = pygame.transform.scale(disco_bg1, (width, height))

    disco_bg2 = pygame.image.load(os.path.join(img_dir, "disco_bg2.jpeg")).convert()
    images["disco_bg2"] = pygame.transform.scale(disco_bg2, (width, height))

    menu_bg = pygame.image.load(os.path.join(img_dir, "background_bar.jpeg")).convert()
    images["menu_bg"] = pygame.transform.scale(menu_bg, (width, height))

    #Beer
    beer = pygame.image.load(os.path.join(img_dir, "beer.png")).convert_alpha()
    images["beer"] = pygame.transform.scale(beer, (90, 90))

    #Broken beer
    broken = pygame.image.load(os.path.join(img_dir, "broken_beer.png")).convert_alpha()
    images["broken_beer"] = pygame.transform.scale(broken, (110, 110))

    #Mouse
    mouse = pygame.image.load(os.path.join(img_dir, "mouse.png")).convert_alpha()
    images["mouse"] = pygame.transform.scale(mouse, (50, 160))

    #Tray
    tray = pygame.image.load(os.path.join(img_dir, "tray_with_hands.png")).convert_alpha()
    images["tray"] = pygame.transform.scale(tray, (270, 110))

    #Cat frames
    cat_width = 140
    cat_height = 120

    cat_frame_1 = pygame.image.load(os.path.join(img_dir, "cat_walk1.png")).convert_alpha()
    cat_frame_1 = pygame.transform.scale(cat_frame_1, (cat_width, cat_height))

    cat_frame_2 = pygame.image.load(os.path.join(img_dir, "cat_walk2.png")).convert_alpha()
    cat_frame_2 = pygame.transform.scale(cat_frame_2, (cat_width, cat_height))

    images["cat_frames"] = [cat_frame_1, cat_frame_2]

    return images, cat_width, cat_height


def load_sounds(sound_dir):

    glass_ding = pygame.mixer.Sound(os.path.join(sound_dir, "glass_ding.wav"))
    glass_break = pygame.mixer.Sound(os.path.join(sound_dir, "glass_break.wav"))
    game_music = pygame.mixer.Sound(os.path.join(sound_dir, "game_music.wav"))
    mouse_sound = pygame.mixer.Sound(os.path.join(sound_dir, "mouse.wav"))
    menu_music = pygame.mixer.Sound(os.path.join(sound_dir, "menu_music.wav"))  # <---

    return glass_ding, glass_break, game_music, mouse_sound, menu_music
