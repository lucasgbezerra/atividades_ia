import random
from time import perf_counter
import pygame
from collections import deque
from utils import setImages 
from cell import Cell

MOUSEBUTTONLEFT = 1
MOUSEBUTTONRIGHT = 3

class Board():
    def __init__(self, screen, clock, rows, cols, size, numMines):
        self.numMines = numMines
        self.grid = []
        self.revealedCells = set()
        self.flags = set()
        self.mines = set()

        self.images = setImages(size, size)
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.size = size

    def setupBoard(self):
        self.buildGrid()
        self.buildMapRandom()
        self.fillingBoard()
        # self.draw()

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
        # for row, col in self.mines:
        #     self.grid[row][col].hasMine = True

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
    
    def addFlags(self, newFlags):
        for row, col in newFlags:
            cell = self.grid[row][col]
            if cell not in self.flags:
                self.flags.add(cell)
    
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

        # pygame.display.flip()
        pygame.display.update(0,0,self.rows*self.size, self.cols*self.size)
        

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
        font = pygame.font.SysFont('comicsans', 40)
        resetFont = pygame.font.SysFont('comicsans', 30)

        text = font.render("Você perdeu! Jogue novamente.", 1, "black")
        text2 = resetFont.render("Pressione a barra de espaço para reiniciar", 1, "black")
        
        self.screen.blit(text, (self.rows*self.size / 2 - text.get_width() / 2, self.cols*self.size / 2 - text.get_height() / 2))
        self.screen.blit(text2, (self.rows*self.size / 2 - text2.get_width() / 2, (self.cols*self.size / 2 - text2.get_height() / 2) + 30))
        
        pygame.display.update()

    def won(self):
        font = pygame.font.SysFont('comicsans', 40)
        resetFont = pygame.font.SysFont('comicsans', 30)
        text = font.render("Parabéns! Você Venceu!", 1, "black")
        text2 = resetFont.render("Pressione a barra de espaço para reiniciar", 1, "black")


        self.screen.blit(text, (self.rows*self.size / 2 - text.get_width() / 2, self.cols*self.size / 2 - text.get_height() / 2))
        self.screen.blit(text2, (self.rows*self.size / 2 - text2.get_width() / 2, (self.cols*self.size / 2 - text2.get_height() / 2) + 30))

        pygame.display.update()

        

    def checkResult(self):
        for row, col in self.mines:
            if  self.grid[row][col] in self.revealedCells:
                print(f"Mina na casa ({row, col})")
                self.gameOver()
                return 2
        
        if len(self.revealedCells) == (self.rows * self.cols) - self.numMines:
            self.won()
            return 2

        return 1

    def  getPositionRevealedCells(self):
        positions = []
        for cell in self.revealedCells:
            pos = cell.getPosition()
            positions.append(pos)
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
        
        print(f"Abertos ({len(self.revealedCells)})")

    def infos(self, time, player):
        # print(f"Tempo: {time:.0f} s")
        font = pygame.font.SysFont('comicsans', 30)
        timeText = font.render(f"Tempo: {time:.0f} s", 1, "white")
        if player:
            playerText = font.render(f"Player: IA", 1, "white")
        else:
            playerText = font.render(f"Player: Usuário", 1, "white")

        flagsText = font.render(f"Flags: {len(self.flags)}", 1, "white")
        width, height = self.screen.get_size()


        self.screen.fill((0,0,0))
        self.screen.blit(timeText, (20, self.cols*self.size + 10))
        self.screen.blit(playerText, (width / 2 - playerText.get_width() / 2, self.cols*self.size + 10))
        self.screen.blit(flagsText, (self.rows*self.size - 100, self.cols*self.size + 10))

        pygame.display.update((0, self.cols*self.size, width,  height - self.cols*self.size))
