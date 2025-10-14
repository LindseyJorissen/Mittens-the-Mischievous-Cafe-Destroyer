import os
WIDTH = 1371
HEIGHT = 1031

WHITE = (255, 255, 255) #leaderboard entries, score, lives
RED = (200, 50, 50) #game over text
GOLD = (197, 175, 108) #hint texts, leaderboard title
YELLOW = (255, 192, 0) #current player in leaderboard
BROWN_SHADOW = (51, 27, 5, 50) #overlay over knoppen

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
LEADERBOARD_FILE = os.path.join(BASE_DIR,"data", "scores.json")
