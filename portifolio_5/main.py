import pygame
from time import time
import sys
from board import Board
from solver import Solver
from utils import setImages

WIDTH = 512
HEIGHT = 550
ROWS = 16
COLS = 16
NUM_MINES= 35

# Cor de background
# BG_COLOR = (192, 192, 192)

# stores XY of mouse events
mouseX = 0
mouseY = 0
mouseButton = None

def terminate():
    pygame.quit()
    sys.exit()

def main():
    moves = 0
    AIsolver = False
    result = 0
    time = 0
    timeFlag = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    pygame.init()
    clock = pygame.time.Clock()
    # screen.fill(BG_COLOR)

    board = Board(screen, clock,ROWS, COLS, WIDTH//ROWS, NUM_MINES)
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
                if mouseY <= min(WIDTH, HEIGHT):
                    mouseButton = event.button
                    board.cellClicked(mouseX//(WIDTH // ROWS), mouseY//(min(WIDTH, HEIGHT) // COLS), mouseButton)
            elif result != 0 and event.type == 771:
                board.reset()
                solver.reset()
                result = 0
                time = 0
                pygame.time.delay(300)       

        # AI
        if AIsolver and result == 0:
            moves += 1
            print(f"----{moves}----")
            
            move = solver.makeMove()
            if move is None:
                print("No moves left to make.")
            else:
                board.cellClicked(move[0], move[1])
                solver.addKnowledge(move, board.revealedCells)
                board.addFlags(solver.mines)
                pygame.time.delay(400)       
        
        if result == 0:
            time += clock.tick(60) / 1000.0
            if int(time) != timeFlag:
                print(int(time))
                timeFlag = time
                board.infos(time)

            board.draw()
        result = board.checkResult()

if __name__ == "__main__":
    main()

    