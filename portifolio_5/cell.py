from utils import IMGS
# Butões do mouse
MOUSEBUTTONLEFT = 1
MOUSEBUTTONRIGHT = 3

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasMine = False
        self.adjacentMines = 0
        self.flag = False
        self.image = None

    def __str__(self):
        return f"Pos X: {self.x},  Pos Y: {self.y} => Mina: {self.hasMine}, Vizinhos: {self.adjacentMines}, Flag: {self.flag}"

    # def getNeighbors(self, rows, cols):
    #     neighbors = set()
    #     for i in range(self.x-1, self.x+2):
    #         for j in range(self.y-1, self.y+2):
    #             if i >= 0 and  i < rows and j >= 0 and j < cols:
    #                 if (i, j) != (self.x, self.y):
    #                     neighbors.add((i, j))
    #     return neighbors

    def getPosition(self):
        return (self.x, self.y)
