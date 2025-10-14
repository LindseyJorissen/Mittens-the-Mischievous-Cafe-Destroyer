import os
import pygame

WIDTH = 1371
HEIGHT = 1031

#colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
GREY = (50, 50, 50)

#paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
LEADERBOARD_FILE = os.path.join(BASE_DIR,"data", "scores.json")

def load_fonts():
    pygame.font.init()
    fonts = {
        "small": pygame.font.Font(os.path.join(FONT_DIR, "BoldPixels.ttf"), 40),
        "medium": pygame.font.Font(os.path.join(FONT_DIR, "BoldPixels.ttf"), 60),
        "large": pygame.font.Font(os.path.join(FONT_DIR, "Ka1.ttf"), 80)
    }
    return fonts