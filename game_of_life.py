import pygame # Biblioteca para crear juegos
import numpy as np # Biblioteca para operaciones numéricas
import time # Biblioteca para gestionar el tiempo
import os # Biblioteca para interactuar con el sistema operativo

# Configuración de la ventana de Pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Game of Life")

# Tamaño de la ventana
width, height = 700, 700
screen = pygame.display.set_mode((width, height))

# Color de fondo
background_color = (25, 25, 25)
screen.fill(background_color)

# Número de celdas en cada eje
num_celdas_x, num_celdas_y = 50, 50
# Ancho y alto de cada celda
ancho_celda = width // num_celdas_x
alto_celda = height // num_celdas_y

# Estructura de datos que contiene todos los estados de las diferentes celdas
# Estados de las celdas: Vivas = 1 - Muertas = 0
estado_celdas = np.zeros((num_celdas_y, num_celdas_x))

# Bandera para pausa
pausa = True
# Bandera para finalizar
finalizar = False
# Contador de generaciones
generacion = 0
# Contador de Poblacion de celdas vivas
poblacion = 0

# Reloj de Pygame para limitar la velocidad de actualización
clock = pygame.time.Clock()

while not finalizar:
    
    # Conjunto para el próximo estado
    nuevoEstado = np.copy(estado_celdas)

    screen.fill(background_color)

    time.sleep(0.1)

    evento = pygame.event.get()

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
                generacion = 0
                estado_celdas = np.zeros((num_celdas_x, num_celdas_y))
                nuevoEstado = np.zeros((num_celdas_x, num_celdas_y))
                pausa = True
            else:
                # Culquier otra tecla pausa o reanuda el juego
                pausa = not pausa 

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            # Click del medio pausa / reanuda el juego
            if mouseClick[1]:

                pausa = not pausa

            else:
                posicion_x, posicion_y = pygame.mouse.get_pos()
                celda_x, celda_y =int(np.floor(posicion_x / ancho_celda)),int( np.floor(posicion_y / alto_celda))
                # Click izquierdo celada vida y derecho para celda muerta
                nuevoEstado[celda_x, celda_y] = not mouseClick[2]

    if not pausa:
        # Incremento el contador de generaciones
        generacion += 1

    for y in range(0, num_celdas_y):

        for x in range(0, num_celdas_x):

            if not pausa:

             #Calcula las 8 posiciones de las celdas vecinas
                celda_vecina = estado_celdas[(x-1) % num_celdas_x, (y-1) % num_celdas_y] + \
                              estado_celdas[(x  ) % num_celdas_x, (y-1) % num_celdas_y] + \
                              estado_celdas[(x+1) % num_celdas_x, (y-1) % num_celdas_y] + \
                              estado_celdas[(x-1) % num_celdas_x, (y  ) % num_celdas_y] + \
                              estado_celdas[(x+1) % num_celdas_x, (y  ) % num_celdas_y] + \
                              estado_celdas[(x-1) % num_celdas_x, (y+1) % num_celdas_y] + \
                              estado_celdas[(x  ) % num_celdas_x, (y+1) % num_celdas_y] + \
                              estado_celdas[(x+1) % num_celdas_x, (y+1) % num_celdas_y]

                #Regla 1: Una celula muerta con exactamente 3 vecinas vivas, Revive!
                if estado_celdas[x,y] == 0 and celda_vecina == 3:
                    nuevoEstado[x,y] = 1
                #Regla 2: Una celula viva con menos de 2 o mas de 3 vecinas vivas, Muere!
                elif estado_celdas[x,y] == 1 and (celda_vecina < 2 or celda_vecina > 3):
                    nuevoEstado[x,y] = 0

            if estado_celdas[x, y] == 1:
                poblacion += 1

            # poligono de cada celda que se dibuja
            poligono = [((x)* ancho_celda, y * alto_celda),
                        ((x + 1) * ancho_celda, y * alto_celda),
                        ((x + 1) * ancho_celda, (y + 1) * alto_celda),
                        ((x) * ancho_celda, (y + 1) * alto_celda)]

            if nuevoEstado[x,y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poligono, 1)
            else:
                if pausa:
                    pygame.draw.polygon(screen, (128, 128, 128), poligono, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poligono, 0)

     # Actualizo el título de la ventana
    titulo = f"Juego de la vida:  Población: {poblacion} Generación: {generacion}"
    if pausa:
        titulo += " - [PAUSA]"
    pygame.display.set_caption(titulo)

    estado_celdas = np.copy(nuevoEstado)

    pygame.display.flip()

    clock.tick(60)

print("Juego finalizado")
