import random
import pygame
import sys

pygame.init()

WIDTH = 512
HEIGHT = 512

MOUSEBUTTONLEFT = 1
MOUSEBUTTONRIGHT = 3

cellSize = 32
numCellsLine = WIDTH // cellSize
numCellsColumn = HEIGHT // cellSize
# Legendas
# ['-1', 'F','0', '1', '2', '3', '4', '5', '6', '7', '8']

# Constants to define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (192, 192, 192)
# Load Sprites
cellImgList = []


cellImg = pygame.image.load("./sprites/Grid.png")
flagImg = pygame.image.load("./sprites/flag.png")
mineImg = pygame.image.load("./sprites/mine.png")
for i in range(0,9):
    if i == 0:
        cellImgList.append(pygame.image.load("./sprites/empty.png"))
    else:
        cellImgList.append(pygame.image.load("./sprites/grid" + str(i) + ".png"))


class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasMine = False
        self.reveal = False
        self.adjacentMines = 0
        self.image = cellImg
        self.marked = False

    def draw(self):
        if self.reveal:
            if self.hasMine:
                self.image = mineImg
            else:
                self.image = cellImgList[self.adjacentMines]
        elif self.marked:
            self.image = flagImg
        else:
            self.image = cellImg

        screen.blit(self.image, (self.x, self.y))


    def clicked(self, mouseButton):
        if mouseButton == MOUSEBUTTONLEFT:
            self.reveal = True
        elif mouseButton == MOUSEBUTTONRIGHT:
            self.marked = True

        self.draw()
        return self.hasMine

class Board():
    def __init__(self):
        self.numMines = 40
        self.grid = []
        self.coveredField = []

    def setupBoard(self):
        self.buildGrid()
        self.buildMapRandom()
        self.fillingBoard()
        self.drawGrid()

    def buildGrid(self):
        for line in range(numCellsLine):
            self.grid.append([])
            for column in range(numCellsColumn):
                self.grid[line].append(Cell(line * cellSize,column * cellSize))

    # 
    def buildMapRandom(self):
        for i in range(self.numMines):
            x = random.randint(0, numCellsLine-1)
            y = random.randint(0, numCellsColumn-1)
            
            self.grid[x][y].hasMine = True


    # def adjacentMines(self):
    #     for i in range(numCellsLine):
    #         for j in range(numCellsColumn):
    #              if self.grid[i][j].hasMine:
    #                 continue
    #         for x in range(i - 1, i + 2):
    #             for y in range(j - 1, j + 2):
    #                 if x < 0 or y < 0 or x >= numCellsLine or y >= numCellsColumn:
    #                     continue
    #                 if self.grid[x][y].hasMine:
    #                     self.grid[i][j].adjacentMines += 1

    def adjacentMines(self, x, y):
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and  i < numCellsLine and j >= 0 and j < numCellsColumn:
                    if self.grid[i][j].hasMine:
                        self.grid[x][y].adjacentMines += 1

        self.grid[x][y].image = cellImgList[self.grid[x][y].adjacentMines]
        

    def fillingBoard(self):
        for i in range(numCellsLine):
            for j in range(numCellsColumn):
                if self.grid[i][j].hasMine:
                    self.grid[i][j].image = mineImg
                else:
                    self.adjacentMines(i, j)

    def drawGrid(self):
        for i in range(numCellsLine):
            for j in range(numCellsColumn):
                self.grid[i][j].draw()
    
    def cellClicked(self, mouseX, mouseY, mouseButton):
        hasMine = self.grid[mouseX//cellSize][mouseY//cellSize].clicked(mouseButton)
        if hasMine:
            print("Game Over")
        else:
            pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')
FPSCLOCK = pygame.time.Clock()
screen.fill(BG_COLOR)

# stores XY of mouse events
mouseX = 0
mouseY = 0
mouseButton = None

board = Board()

board.setupBoard()

def terminate():
    pygame.quit()
    sys.exit()

while True:
    
    # event handling loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            mouseButton = event.button
            print(mouseX, mouseY, mouseButton)
            board.cellClicked(mouseX, mouseY, mouseButton)


    pygame.display.update()