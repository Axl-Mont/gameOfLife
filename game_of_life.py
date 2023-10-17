import pygame
import numpy as np

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))

background = (25, 25, 25)
screen.fill(background)

celdaX, celdaY = 25, 25

celdaWidth = width // celdaX
celdaHeight = height // celdaY

while True:
    for y in range(0, celdaY):
        for x in range(0, celdaX):

            polygono = [((x)* celdaWidth, y * celdaHeight),
                        ((x + 1) * celdaWidth, y * celdaHeight),
                        ((x + 1) * celdaWidth, (y + 1) * celdaHeight),
                        ((x) * celdaWidth, (y + 1) * celdaHeight)]

            pygame.draw.polygon(screen, (128, 128, 128), polygono, 1)
            
    pygame.display.flip()