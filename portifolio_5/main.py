import pygame
from time import time
import sys
from board import Board
from solver import Solver
from utils import setImages

WIDTH = 512
HEIGHT = 512

rows = 8
cols = 8
SIZE = WIDTH // rows


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
    AIsolver = True
    setImages(WIDTH // rows, HEIGHT // cols)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen.fill(BG_COLOR)

    board = Board(screen, WIDTH, HEIGHT, SIZE)

    board.setupBoard()

    solver = Solver(rows,cols)

    run = True
    while run:

        AIsolver = False
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                mouseButton = event.button
                board.cellClicked(mouseX//SIZE, mouseY//SIZE, mouseButton)
            if event.type == 771:
                # print("Space")
                AIsolver = True

        # AI
        if AIsolver:
            move = solver.makeMove()
            if move is None:
                print("No moves left to make.")
            else:
                board.cellClicked(move[0], move[1])
                solver.addKnowledge(move, board.revealedCells)
                
            
            
        # board.draw()
        # pygame.time.delay(2000)
        


if __name__ == "__main__":
    main()

    