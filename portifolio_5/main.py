import pygame
from time import time
import sys
from board import Board
from solver import Solver
from utils import setImages

WIDTH = 512
HEIGHT = 512
ROWS = 16
COLS = 16
NUM_MINES= 35

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
    moves = 0
    AIsolver = True
    setImages(WIDTH // ROWS, HEIGHT // COLS)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    pygame.init()
    # FPSCLOCK = pygame.time.Clock()
    screen.fill(BG_COLOR)

    board = Board(screen, ROWS, COLS, WIDTH//ROWS, NUM_MINES)

    board.setupBoard()

    solver = Solver(ROWS,COLS)

    run = True
    while run:
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                mouseButton = event.button
                board.cellClicked(mouseX//(WIDTH // ROWS), mouseY//(HEIGHT // COLS), mouseButton)

        # AI
        if AIsolver:
            moves += 1
            print(f"----{moves}----")
            
            move = solver.makeMove()
            if move is None:
                print("No moves left to make.")
            else:
                board.cellClicked(move[0], move[1])
                solver.addKnowledge(move, board.revealedCells)
                # pygame.time.delay(100)       


if __name__ == "__main__":
    main()

    