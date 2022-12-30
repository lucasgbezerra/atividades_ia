import random
import pygame
import sys
from mineswepper import Board


pygame.init()

WIDTH = 512
HEIGHT = 512

SIZE = 32

# Legendas
# ['-1', 'F','0', '1', '2', '3', '4', '5', '6', '7', '8']

# Constants to define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (192, 192, 192)


# stores XY of mouse events
mouseX = 0
mouseY = 0
mouseButton = None

def terminate():
    pygame.quit()
    sys.exit()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    FPSCLOCK = pygame.time.Clock()
    screen.fill(BG_COLOR)

    board = Board(screen, WIDTH, HEIGHT, SIZE)

    board.setupBoard()

    while True:

        # event handling loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                mouseButton = event.button
                print(mouseX, mouseY, mouseButton)
                board.cellClicked(mouseX, mouseY, mouseButton)


        pygame.display.update()


if __name__ == "__main__":
    main()