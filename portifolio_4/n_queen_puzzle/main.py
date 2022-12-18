import pygame, sys
from time import time

from chessboard import drawChessBoard, drawSolution
from n_queen_puzzle import solverNQueen

# Número de rainhas
print ("Defina o número de Queens")
num_queens = int(input())

# Estado inicial do tabuleiro
board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],]

solution = []

start = time()
hasSolution = solverNQueen(board, 0, num_queens, solution)
end = time()
if (not hasSolution):
    printf("Não existe solução")
else:
    # Pygame
    pygame.init()

    SIZE = 800
    WINDOWS = pygame.display.set_mode((SIZE, SIZE))

    drawChessBoard(WINDOWS, SIZE, num_queens)
    drawSolution(WINDOWS, SIZE, solution)
    print(f"Tempo para encontrar solução: {(end-start) * 1000:.3f} ms")
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.display.update()

