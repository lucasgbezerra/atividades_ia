import pygame
from time import time
import sys
from board import Board
from solver import Solver

WIDTH = 512
HEIGHT = 550
ROWS = 16
COLS = 16

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
    AIsolver = True
    state = 1
    startTime = 0
    num_mines = 40

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    pygame.init()
    clock = pygame.time.Clock()

    board = Board(screen, clock,ROWS, COLS, WIDTH//ROWS, num_mines)
    board.setupBoard()

    solver = Solver(ROWS,COLS)

    run = True
    startTime = time()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if mouseY <= min(WIDTH, HEIGHT):
                    mouseButton = event.button
                    board.cellClicked(mouseX//(WIDTH // ROWS), mouseY//(min(WIDTH, HEIGHT) // COLS), mouseButton)
            elif state == 2 and  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                board.reset()
                solver.reset()
                state = 0
                startTime = time()
                pygame.time.delay(300)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                print("Trocou")
                AIsolver = not AIsolver


        if AIsolver and state == 1:
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


        if state == 1:
            board.infos(int(time() - startTime))
            board.draw()

        state = board.checkResult()

if __name__ == "__main__":
    main()

    