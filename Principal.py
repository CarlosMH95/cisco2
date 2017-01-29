import sys
import random
import pygame
#Constantes para inicializar la imagen
IMAGE_FILE = "Wollemi.jpg"
IMAGE_SIZE = (800, 600)
TILE_WIDTH = 200
TILE_HEIGHT = 200
COLUMNS = 4
ROWS = 3

# Esquina inferior izquierda no contiene ninguna parte
EMPTY_TILE = (COLUMNS-1, ROWS-1)

BLACK = (0, 0, 0)

# Bordes para las partes
hor_border = pygame.Surface((TILE_WIDTH, 1))
hor_border.fill(BLACK)
ver_border = pygame.Surface((1, TILE_HEIGHT))
ver_border.fill(BLACK)

# Aqui cargo la imagen y la divido en partes

image = pygame.image.load(IMAGE_FILE)
tiles = {}
for c in range(COLUMNS) :
    for r in range(ROWS) :
        tile = image.subsurface (
            c*TILE_WIDTH, r*TILE_HEIGHT,
            TILE_WIDTH, TILE_HEIGHT)
        tiles [(c, r)] = tile
        if (c, r) != EMPTY_TILE:
            tile.blit(hor_border, (0, 0))
            tile.blit(hor_border, (0, TILE_HEIGHT-1))
            tile.blit(ver_border, (0, 0))
            tile.blit(ver_border, (TILE_WIDTH-1, 0))
            # make the corners a bit rounded
            tile.set_at((1, 1), BLACK)
            tile.set_at((1, TILE_HEIGHT-2), BLACK)
            tile.set_at((TILE_WIDTH-2, 1), BLACK)
            tile.set_at((TILE_WIDTH-2, TILE_HEIGHT-2), BLACK)
tiles[EMPTY_TILE].fill(BLACK)

# Para tener el registro de cual tile esta en que posicion
state = {(col, row): (col, row)
            for col in range(COLUMNS) for row in range(ROWS)}

# Para tener registro de en donde se encuentra la vacia
(emptyc, emptyr) = EMPTY_TILE

# Cuando empiezas el juego se inicializa el rompecabezas
pygame.init()
display = pygame.display.set_mode(IMAGE_SIZE)
pygame.display.set_caption("Shift Puzzle")
display.blit (image, (0, 0))
pygame.display.flip()

# Funciones de swap y shuffle
def shift (c, r) :
    global emptyc, emptyr
    display.blit(
        tiles[state[(c, r)]],
        (emptyc*TILE_WIDTH, emptyr*TILE_HEIGHT))
    display.blit(
        tiles[EMPTY_TILE],
        (c*TILE_WIDTH, r*TILE_HEIGHT))
    state[(emptyc, emptyr)] = state[(c, r)]
    state[(c, r)] = EMPTY_TILE
    (emptyc, emptyr) = (c, r)
    pygame.display.flip()

# Con eso se hacen movimientos aleatorios de los tiles
def shuffle() :
    global emptyc, emptyr
    
    last_r = 0
    for i in range(75):

        pygame.time.delay(20)
        while True:

            r = random.randint(1, 4)
            if (last_r + r == 5):

                continue
            if r == 1 and (emptyc > 0):
                shift(emptyc - 1, emptyr)
            elif r == 4 and (emptyc < COLUMNS - 1):
                shift(emptyc + 1, emptyr)
            elif r == 2 and (emptyr > 0):
                shift(emptyc, emptyr - 1)
            elif r == 3 and (emptyr < ROWS - 1):
                shift(emptyc, emptyr + 1)
            else:

                continue
            last_r=r
            break

# Aq1ui se procesan los mouse clicks
at_start = True
showing_solution = False
while True:
    event = pygame.event.wait()
    print(event)
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if pygame.key.get_pressed()[pygame.K_UP] and emptyr-1>-1:
            c=emptyc
            r=emptyr-1
            shift(c, r)
        elif pygame.key.get_pressed()[pygame.K_DOWN] and emptyr+1<3:
            c = emptyc
            r = emptyr+ 1
            shift(c, r)
        elif pygame.key.get_pressed()[pygame.K_LEFT] and emptyc-1>-1:
            c = emptyc-1
            r = emptyr
            shift(c, r)
        elif pygame.key.get_pressed()[pygame.K_RIGHT] and emptyc+1<4:
            c = emptyc+1
            r = emptyr
            shift(c, r)
        print(emptyc)
        print(emptyr)

    elif event.type == pygame.MOUSEBUTTONDOWN :
        if at_start:
            # se hace un shuffle en el primer click del mouse
            #shuffle()
            at_start = False

        elif event.dict['button'] == 3:
            # Muestra la imagen de solucion
            saved_image = display.copy()
            display.blit(image, (0, 0))
            origi=display.copy()
            pygame.display.flip()
            #print(saved_image)
            showing_solution = True
    elif showing_solution and (event.type == pygame.MOUSEBUTTONUP):
        # stop showing the solution
        display.blit (saved_image, (0, 0))
        pygame.display.flip()
    if display.copy()==image:
        print('entro')
        display = pygame.display.set_mode((559,420))
        pygame.display.set_caption("Shift Puzzle")
        display.blit('Win.jpg', (0, 0))
        pygame.display.flip()
        event2 = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

showing_solution = False