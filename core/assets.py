import os
import pygame

def load_images(img_dir, width, height):
    images = {}

    #Bar backgrounds
    bg = pygame.image.load(os.path.join(img_dir, "background_bar.jpeg")).convert()
    images["background"] = bg

    disco_bg1 = pygame.image.load(os.path.join(img_dir, "disco_bg1.jpeg")).convert()
    images["disco_bg1"] = disco_bg1

    disco_bg2 = pygame.image.load(os.path.join(img_dir, "disco_bg2.jpeg")).convert()
    images["disco_bg2"] = disco_bg2

    pub_open = pygame.image.load(os.path.join(img_dir, "pub_open.jpeg")).convert()
    images["pub_open"] = pub_open

    pub_closed = pygame.image.load(os.path.join(img_dir, "pub_closed.jpeg")).convert()
    images["pub_closed"] = pub_closed

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
    images["tray"] = pygame.transform.scale(tray, (260, 100))

    #Cat frames
    cat_width = 130
    cat_height = 110

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
    menu_music = pygame.mixer.Sound(os.path.join(sound_dir, "menu_music.wav"))
    door_creak = pygame.mixer.Sound(os.path.join(sound_dir, "door_creak.wav"))
    return glass_ding, glass_break, game_music, mouse_sound, menu_music, door_creak
