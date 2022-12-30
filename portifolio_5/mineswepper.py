import random
import pygame
import sys
from cell import Cell, cellImg, flagImg, mineImg, cellImgList

class Board():
    def __init__(self, screen, width, height, size):
        self.numMines = 40
        self.grid = []
        self.coveredField = []
        self.screen = screen
        self.rows = width // size
        self.cols = height // size
        self.size = size

    def setupBoard(self):
        self.buildGrid()
        self.buildMapRandom()
        self.fillingBoard()
        self.drawGrid()

    def buildGrid(self):
        for line in range(self.rows):
            self.grid.append([])
            for column in range(self.rows):
                self.grid[line].append(Cell(line * self.size,column * self.size))

    # 
    def buildMapRandom(self):
        for i in range(self.numMines):
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.rows-1)
            
            self.grid[x][y].hasMine = True


    # def adjacentMines(self):
    #     for i in range(self.rows):
    #         for j in range(self.rows):
    #              if self.grid[i][j].hasMine:
    #                 continue
    #         for x in range(i - 1, i + 2):
    #             for y in range(j - 1, j + 2):
    #                 if x < 0 or y < 0 or x >= self.rows or y >= self.rows:
    #                     continue
    #                 if self.grid[x][y].hasMine:
    #                     self.grid[i][j].adjacentMines += 1

    def adjacentMines(self, x, y):
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and  i < self.rows and j >= 0 and j < self.rows:
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

    def drawGrid(self):
        for i in range(self.rows):
            for j in range(self.rows):
                self.grid[i][j].draw(self.screen)
    
    def cellClicked(self, mouseX, mouseY, mouseButton):
        cell = self.grid[mouseX//self.size][mouseY//self.size]
        hasMine = cell.clicked(mouseButton)
        cell.draw(self.screen)
        if hasMine:
            print("Game Over")
        else:
            pass

