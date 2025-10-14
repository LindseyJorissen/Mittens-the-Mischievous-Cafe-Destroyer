import pygame
from screens import menu

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
menu.run_menu()
