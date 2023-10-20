import pygame
import numpy as np
import time

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))

background = (25, 25, 25)
screen.fill(background)


celdaX, celdaY = 50, 50

celdaWidth = width // celdaX
celdaHeight = height // celdaY

estadoCelda = np.zeros((celdaY, celdaX))

estadoCelda[21,21] = 1
estadoCelda[22,22] = 1
estadoCelda[22,23] = 1
estadoCelda[21,23] = 1
estadoCelda[20,23] = 1

pause = False

while True:

    nuevoEstado = np.copy(estadoCelda)

    screen.fill(background)

    time.sleep(0.1)

    evento = pygame.event.get()

    for ev in evento:
        if ev.type == pygame.KEYDOWN:
            pause = not pause

        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY =int(np.floor(posX / celdaWidth)),int( np.floor(posY / celdaHeight))
            nuevoEstado[celX, celY] = 1

    for y in range(0, celdaY):

        for x in range(0, celdaX):

            if not pause:

             #Calcula las 8 posiciones de las celdas vecinas
                celdaVecina = estadoCelda[(x-1) % celdaX, (y-1) % celdaY] + \
                              estadoCelda[(x  ) % celdaX, (y-1) % celdaY] + \
                              estadoCelda[(x+1) % celdaX, (y-1) % celdaY] + \
                              estadoCelda[(x-1) % celdaX, (y  ) % celdaY] + \
                              estadoCelda[(x+1) % celdaX, (y  ) % celdaY] + \
                              estadoCelda[(x-1) % celdaX, (y+1) % celdaY] + \
                              estadoCelda[(x  ) % celdaX, (y+1) % celdaY] + \
                              estadoCelda[(x+1) % celdaX, (y+1) % celdaY]

                #Regla 1: Una celula muerta con exactamente 3 vecinas vivas, Revive!
                if estadoCelda[x,y] == 0 and celdaVecina == 3:
                    nuevoEstado[x,y] = 1
                #Regla 2: Una celula viva con menos de 2 o mas de 3 vecinas vivas, Muere!
                elif estadoCelda[x,y] == 1 and (celdaVecina < 2 or celdaVecina > 3):
                    nuevoEstado[x,y] = 0

            # poligono de cada celda que se dibuja
            polygono = [((x)* celdaWidth, y * celdaHeight),
                        ((x + 1) * celdaWidth, y * celdaHeight),
                        ((x + 1) * celdaWidth, (y + 1) * celdaHeight),
                        ((x) * celdaWidth, (y + 1) * celdaHeight)]

            if nuevoEstado[x,y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), polygono, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), polygono, 0)

    estadoCelda = np.copy(nuevoEstado)

    pygame.display.flip()
