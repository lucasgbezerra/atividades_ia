import pygame
from time import time
import sys
from board import Board
from solver import Solver

FACIL = ((8, 10), 10)
MEDIO = ((14, 18), 40)
DIFICIL = ((20,24), 99)

COLS = MEDIO[0][1]
ROWS = MEDIO[0][0]
WIDTH = 32*ROWS
HEIGHT = (32*COLS)+38

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
    num_mines = MEDIO[1]

    # AMOSTRA
    amostra = 100

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')
    pygame.init()

    board = Board(screen, ROWS, COLS, 32, num_mines)
    board.setupBoard()

    solver = Solver(ROWS, COLS, num_mines)

    run = True
    startTime = time()
    while run:
        if state != 1:
            if amostra == 0:
                terminate()
            if moves > 1:
                amostra -= 1
                text = f'''----- STATUS {100 - amostra} -----\nResultado: {state == 2}\nMoves Prob: {solver.numProbMoves}\nMoves Random: {solver.numRandomMoves}\nMoves Safe: {solver.numSafeMoves}\nTempo: {int(time() - startTime)} s\n'''
                with open("result.txt", "a") as file:
                    file.write(text)

            moves = 0
            board.reset()
            solver.reset()
            state = 1
            startTime = time()
            pygame.time.delay(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if mouseY <= min(WIDTH, HEIGHT):
                    mouseButton = event.button
                    board.cellClicked(
                        mouseX//(WIDTH // ROWS), mouseY//(min(WIDTH, HEIGHT) // COLS), mouseButton)
                    # solver.probsOfMine(board.numMines, ROWS*COLS, board)
            # elif state == 2 and  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                print("Trocou")
                AIsolver = not AIsolver

        if AIsolver and state == 1:
            moves += 1
            print(f"----{moves}----")

            move = solver.makeMove()
            if move is None:
                move = solver.probBasedMove(board.numMines, ROWS*COLS, board)
                # move = solver.makeRandomMove()
            if move is None:
                print("No moves left to make.")
            else:
                board.cellClicked(move[0], move[1])
                solver.addKnowledge(move, board.revealedCells)
                board.addFlags(solver.mines)
                # pygame.time.delay(400)

            # AIsolver = False
        if state == 1:
            board.infos(int(time() - startTime), AIsolver)
            board.draw()

        state = board.checkResult()


if __name__ == "__main__":
    main()
