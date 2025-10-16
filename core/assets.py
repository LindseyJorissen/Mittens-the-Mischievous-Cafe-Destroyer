import os
import pygame
from core.constants import IMG_DIR,FONT_DIR,SOUND_DIR

def load_fonts():
    pygame.font.init()
    fonts = {
        "small": pygame.font.Font(os.path.join(FONT_DIR, "BoldPixels.ttf"), 40),
        "medium": pygame.font.Font(os.path.join(FONT_DIR, "BoldPixels.ttf"), 60),
        "large": pygame.font.Font(os.path.join(FONT_DIR, "Ka1.ttf"), 80)
    }
    return fonts

def load_images():

    images = {}

    bg = pygame.image.load(os.path.join(IMG_DIR, "background_bar.jpeg")).convert()
    images["background"] = bg

    disco_bg1 = pygame.image.load(os.path.join(IMG_DIR, "disco_bg1.jpeg")).convert()
    images["disco_bg1"] = disco_bg1

    disco_bg2 = pygame.image.load(os.path.join(IMG_DIR, "disco_bg2.jpeg")).convert()
    images["disco_bg2"] = disco_bg2

    pub_open = pygame.image.load(os.path.join(IMG_DIR, "pub_open.jpeg")).convert()
    images["pub_open"] = pub_open

    pub_closed = pygame.image.load(os.path.join(IMG_DIR, "pub_closed.jpeg")).convert()
    images["pub_closed"] = pub_closed

    images["leaderboard"] = pygame.image.load(os.path.join(IMG_DIR, "leaderboard.jpeg")).convert()
    images["name_input"] = pygame.image.load(os.path.join(IMG_DIR, "name_input.jpeg")).convert()
    images["tutorial"] = pygame.image.load(os.path.join(IMG_DIR, "tutorial.jpeg")).convert()

    beer = pygame.image.load(os.path.join(IMG_DIR, "beer.png")).convert_alpha()
    images["beer"] = pygame.transform.scale(beer, (90, 90))

    broken = pygame.image.load(os.path.join(IMG_DIR, "broken_beer.png")).convert_alpha()
    images["broken_beer"] = pygame.transform.scale(broken, (110, 110))

    mouse = pygame.image.load(os.path.join(IMG_DIR, "mouse.png")).convert_alpha()
    images["mouse"] = pygame.transform.scale(mouse, (50, 160))

    tray = pygame.image.load(os.path.join(IMG_DIR, "tray_with_hands.png")).convert_alpha()
    images["tray"] = pygame.transform.scale(tray, (260, 100))

    cat_frame_1 = pygame.image.load(os.path.join(IMG_DIR, "cat1.png")).convert_alpha()
    cat_frame_1 = pygame.transform.scale(cat_frame_1, (130, 110))
    cat_frame_2 = pygame.image.load(os.path.join(IMG_DIR, "cat2.png")).convert_alpha()
    cat_frame_2 = pygame.transform.scale(cat_frame_2, (130, 110))
    cat_frame_3 = pygame.image.load(os.path.join(IMG_DIR, "cat3.png")).convert_alpha()
    cat_frame_3 = pygame.transform.scale(cat_frame_3, (130, 110))
    cat_frame_4 = pygame.image.load(os.path.join(IMG_DIR, "cat4.png")).convert_alpha()
    cat_frame_4 = pygame.transform.scale(cat_frame_4, (130, 110))
    images["cat_frames"] = [cat_frame_1, cat_frame_2,cat_frame_3,cat_frame_4]

    return images

def load_sounds():
    sounds = {
        "glass_ding": pygame.mixer.Sound(os.path.join(SOUND_DIR, "glass_ding.wav")),
        "glass_break": pygame.mixer.Sound(os.path.join(SOUND_DIR, "glass_break.wav")),
        "game_music": pygame.mixer.Sound(os.path.join(SOUND_DIR, "game_music.mp3")),
        "mouse_sound": pygame.mixer.Sound(os.path.join(SOUND_DIR, "mouse.mp3")),
        "menu_music": pygame.mixer.Sound(os.path.join(SOUND_DIR, "menu_music.wav")),
        "door_creak": pygame.mixer.Sound(os.path.join(SOUND_DIR, "door_creak.wav")),
        "knock_wood": pygame.mixer.Sound(os.path.join(SOUND_DIR, "knock_wood.wav")),
        "cat_meow": pygame.mixer.Sound(os.path.join(SOUND_DIR, "cat_meow.mp3")),
        "game_over": pygame.mixer.Sound(os.path.join(SOUND_DIR, "game_over.mp3"))

    }
    return sounds
