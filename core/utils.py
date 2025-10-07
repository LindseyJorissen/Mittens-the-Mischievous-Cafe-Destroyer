import pygame

def blit_centered_image(screen, image):
    sw, sh = screen.get_size()
    iw, ih = image.get_size()
    image_ratio = iw / ih
    screen_ratio = sw / sh

    if image_ratio > screen_ratio:
        new_width = sw
        new_height = int(sw / image_ratio)
        x = 0
        y = (sh - new_height) // 2
    else:
        new_height = sh
        new_width = int(sh * image_ratio)
        x = (sw - new_width) // 2
        y = 0

    screen.fill((0, 0, 0))
    scaled = pygame.transform.smoothscale(image, (new_width, new_height))
    screen.blit(scaled, (x, y))

    return pygame.Rect(x, y, new_width, new_height)
