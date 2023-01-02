import random
import pygame
from collections import deque
from utils import setImages, IMGS 
from cell import Cell

MOUSEBUTTONLEFT = 1
MOUSEBUTTONRIGHT = 3

class Board():
    def __init__(self, screen, width, height, size):
        self.numMines = 5
        self.grid = []
        self.revealedCells = set()
        self.flags = set()
        self.mines = set()

        self.images = setImages(size, size)
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
    
    def buildMapRandom(self):
        while len(self.mines) < self.numMines:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.rows-1)
            if self.grid[row][col].hasMine:
                continue
            self.grid[row][col].hasMine = True
            self.mines.add((row, col))

    def adjacentMines(self, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < self.rows and j >= 0 and j < self.rows:
                    if self.grid[i][j].hasMine:
                        self.grid[x][y].adjacentMines += 1

        self.grid[x][y].image = self.images.get("grid" + str(self.grid[x][y].adjacentMines))

    def fillingBoard(self):
        for i in range(self.rows):
            for j in range(self.rows):
                if self.grid[i][j].hasMine:
                    self.grid[i][j].image = self.images.get("mine")
                else:
                    self.adjacentMines(i, j)
    
    def getNeighbors(self, cell):
        neighbors = set()
        x, y = cell.getPosition()
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and  i < self.rows and j >= 0 and j < self.cols:
                    if (i, j) != (x, y):
                        neighbors.add(self.grid[i][j])
        return neighbors
    
    def draw(self):
        for x in range(self.rows):
            for y in range(self.rows):
                cell = self.grid[x][y]
                if cell in self.flags:
                    self.screen.blit(self.images.get("flag"), (cell.x * self.size, cell.y * self.size))
                elif cell not in self.revealedCells:
                    
                    self.screen.blit(self.images.get("grid"), (cell.x * self.size, cell.y * self.size))
                else:
                    self.screen.blit(cell.image, (cell.x * self.size, cell.y * self.size))

        pygame.display.update()
        
        print(f"Abertos ({len(self.revealedCells)})")

    def reset(self):
        self.grid = []
        self.revealedCells = set()
        self.flags = set()
        self.mines = set()

        self.setupBoard()

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
            # print(cell)

            if cell.adjacentMines == 0:
                neighbors = self.getNeighbors(cell)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        visited.add(neighbor)

        for i in visited:
            self.revealedCells.add(i)

    def gameOver(self):
        lostFont = pygame.font.SysFont('comicsans', 40)
        text = lostFont.render("Você perdeu! Jogue novamente.", 1, "black")
        
        self.screen.blit(text, (self.rows*self.size / 2 - text.get_width() / 2, self.cols*self.size / 2 - text.get_height() / 2))
        
        pygame.display.update()

        pygame.time.delay(5000)
        # self.reset()

    def won(self):
        lostFont = pygame.font.SysFont('comicsans', 40)
        text = lostFont.render("Parabéns! Você Venceu!", 1, "black")

        self.screen.blit(text, (self.rows*self.size / 2 - text.get_width() / 2, self.cols*self.size / 2 - text.get_height() / 2))
        pygame.display.update()

        pygame.time.delay(5000)
        # self.reset()

    def checkResult(self):
        for row, col in self.mines:
            if  self.grid[row][col] in self.revealedCells:
                print(f"Mina na casa ({row, col})")
                self.gameOver()
        
        if len(self.revealedCells) == (self.rows * self.cols) - self.numMines:
            self.won()

    def  getPositionRevealedCells(self):
        positions = []
        for cell in self.revealedCells:
            pos =cell.getPosition()
            positions.append[pos]

        return positions


    def cellClicked(self, row, col, mouseButton=MOUSEBUTTONLEFT):
        cell = self.grid[row][col]

        if cell not in self.revealedCells:
            if mouseButton == MOUSEBUTTONRIGHT:
                if cell in self.flags:
                    self.flags.remove(cell)
                else:
                    self.flags.add(cell)
            elif mouseButton == MOUSEBUTTONLEFT:
                if cell not in self.flags:
                    self.revealedCells.add(cell)
                    if not cell.hasMine:
                        self.uncoverCells(cell)

        self.draw()
        self.checkResult()