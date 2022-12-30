import random
import pygame
from collections import deque
from cell import Cell, cellImg, flagImg, mineImg, cellImgList

MOUSEBUTTONLEFT = 1
MOUSEBUTTONRIGHT = 3

mapa = [(3, 13), (10, 6), (13, 11), (11, 11), (2, 8), (6, 2), (6, 11), (4, 2), (5, 12), (11, 1), (9, 10), (8, 8), (10, 11), (9, 13), (0, 4),
        (10, 8), (15, 4), (13, 10), (6, 4), (6, 13), (14, 8), (5, 5), (8, 4), (5, 8), (8, 7), (13, 0), (10, 13), (15, 0), (11, 15), (1, 10)]


class Board():
    def __init__(self, screen, width, height, size):
        self.numMines = 30
        self.grid = []
        self.coveredField = set()
        self.flags = set()
        self.mines = set()
        self.screen = screen
        self.rows = width // size
        self.cols = height // size
        self.size = size

    def setupBoard(self):
        self.buildGrid()
        self.buildMapRandom()
        self.fillingBoard()
        self.draw()

    def buildGrid(self):
        for line in range(self.rows):
            self.grid.append([])
            for column in range(self.rows):
                self.grid[line].append(Cell(line, column))
                # self.coveredField.add(self.grid[line][column])
    #

    def buildMapRandom(self):
        # while len(self.mines) < self.numMines:
        #     row = random.randint(0, self.rows-1)
        #     col = random.randint(0, self.rows-1)
        #     if self.grid[row][col].hasMine:
        #         continue
        #     self.grid[row][col].hasMine = True
        #     self.mines.add((row, col))
        # print(self.mines)
        self.mines = mapa
        for mine in self.mines:
            row, col = mine
            self.grid[row][col].hasMine = True

    def adjacentMines(self, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < self.rows and j >= 0 and j < self.rows:
                    if self.grid[i][j].hasMine:
                        self.grid[x][y].adjacentMines += 1

        self.grid[x][y].image = cellImgList[self.grid[x][y].adjacentMines]

    def fillingBoard(self):
        for i in range(self.rows):
            for j in range(self.rows):
                if self.grid[i][j].hasMine:
                    self.grid[i][j].image = mineImg
                else:
                    self.adjacentMines(i, j)

    def draw(self):
        for x in range(self.rows):
            for y in range(self.rows):
                cell = self.grid[x][y]
                if cell in self.flags:
                    self.screen.blit(
                        flagImg, (cell.x * self.size, cell.y * self.size))
                elif cell not in self.coveredField:
                    self.screen.blit(cellImg, (cell.x * self.size, cell.y * self.size))
                else:
                    self.screen.blit(cell.image, (cell.x * self.size, cell.y * self.size))

            pygame.display.update()

    def uncoverCells(self, clickedCell):
        """
        Utiliza algoritmos BFS para revelar todas as celulas vizinhas
        até a fronteira com númeoros ou flags.
        """
        queue = deque()
        queue.append(clickedCell)

        visited = set()

        while queue:
            cell = queue.pop()
            print(cell)

            if cell.adjacentMines == 0:
                neighbors = cell.getNeighbors(self.rows, self.cols)
                for neighbor in neighbors:
                    x, y = neighbor
                    if self.grid[x][y] not in visited:
                        queue.append(self.grid[x][y])
                    visited.add(self.grid[x][y])

        for i in visited:
            self.coveredField.add(i)

    def gameOver(self, cell):
        lostFont = pygame.font.SysFont('comicsans', 40)
        text = lostFont.render("Você perdeu! Jogue novamente.", 1, "black")
        
        self.screen.blit(cell.image, (cell.x * self.size, cell.y * self.size))    
        self.screen.blit(text, (self.rows*self.size / 2 - text.get_width() / 2, self.cols*self.size / 2 - text.get_height() / 2))
        
        pygame.display.update()

    def cellClicked(self, mouseX, mouseY, mouseButton):
        cell = self.grid[mouseX//self.size][mouseY//self.size]

        if cell not in self.coveredField:
            if mouseButton == MOUSEBUTTONRIGHT:
                if cell in self.flags:
                    self.flags.remove(cell)
                else:
                    self.flags.add(cell)
            elif mouseButton == MOUSEBUTTONLEFT:
                if cell not in self.flags:
                    self.coveredField.add(cell)
                    if cell.hasMine:
                        self.gameOver(cell)
                        pygame.time.delay(5000)
                    else:
                        self.uncoverCells(cell)

        self.draw()
