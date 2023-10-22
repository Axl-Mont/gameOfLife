import pygame
import numpy as np
import time
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

pygame.display.set_caption("Game of Life")

width, height = 700, 700
screen = pygame.display.set_mode((width, height))

background = (25, 25, 25)
screen.fill(background)

# Cantidad de celdas en cada eje
celdaX, celdaY = 50, 50
# Ancho y alto de cada celda
celdaWidth = width // celdaX
celdaHeight = height // celdaY

# Estructura de datos que contiene todos los estados de las diferentes celdas
# Estados de las celdas: Vivas = 1 - Muertas = 0
estadoCelda = np.zeros((celdaY, celdaX))

pause = True

finalizar = False

iteraciones = 0

clock = pygame.time.Clock()

while not finalizar:

    nuevoEstado = np.copy(estadoCelda)

    screen.fill(background)

    time.sleep(0.1)

    evento = pygame.event.get()

    poblacion = 0

    for ev in evento:
        if ev.type == pygame.QUIT:
            finalizar = True
            break

        if ev.type == pygame.KEYDOWN:

         # Tecla ESC para finalizar el juego
            if ev.key == pygame.K_ESCAPE:
                finalizar = True
                break
            # Tecla R para limpiar la grilla, resetear población e iteración y pausa el juego
            if ev.key == pygame.K_r:
                iteraciones = 0
                estadoCelda = np.zeros((celdaX, celdaY))
                nuevoEstado = np.zeros((celdaX, celdaY))
                pause = True
            else:
                # Culquier otra tecla pausa o reanuda el juego
                pause = not pause 

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            # Click del medio pausa / reanuda el juego
            if mouseClick[1]:

                pause = not pause

            else:
                posX, posY = pygame.mouse.get_pos()
                celX, celY =int(np.floor(posX / celdaWidth)),int( np.floor(posY / celdaHeight))
                # Click izquierdo celada vida y derecho para celda muerta
                nuevoEstado[celX, celY] = not mouseClick[2]

    if not pause:
        # Incremento el contador de generaciones
        iteraciones += 1

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

            if estadoCelda[x, y] == 1:
                poblacion += 1

            # poligono de cada celda que se dibuja
            poligono = [((x)* celdaWidth, y * celdaHeight),
                        ((x + 1) * celdaWidth, y * celdaHeight),
                        ((x + 1) * celdaWidth, (y + 1) * celdaHeight),
                        ((x) * celdaWidth, (y + 1) * celdaHeight)]

            if nuevoEstado[x,y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poligono, 1)
            else:
                if pause:
                    pygame.draw.polygon(screen, (128, 128, 128), poligono, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poligono, 0)

     # Actualizo el título de la ventana
    title = f"Juego de la vida:  Población: {poblacion} Generación: {iteraciones}"
    if pause:
        title += " - [PAUSA]"
    pygame.display.set_caption(title)

    estadoCelda = np.copy(nuevoEstado)

    pygame.display.flip()

    clock.tick(60)

print("Juego finalizado")
