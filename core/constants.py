import os
import pygame

#game window
WIDTH = 1000
HEIGHT = 700

#colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
GREY = (50, 50, 50)

#paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

#font setup
def load_fonts():
    pygame.font.init()
    fonts = {
        "small": pygame.font.SysFont(None, 40),
        "medium": pygame.font.SysFont(None, 50),
        "large": pygame.font.SysFont(None, 80),
    }
    return fonts