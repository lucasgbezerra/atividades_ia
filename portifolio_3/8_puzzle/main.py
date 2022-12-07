from board import Board
from aStar import aStarSolve


inicial = [0, 1, 3, 4, 2, 5, 7, 8, 6]
board = Board(estadoInicial=inicial)
aStarSolve(board)
