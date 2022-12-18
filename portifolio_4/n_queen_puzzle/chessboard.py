import pygame
from pygame import Color
from time import sleep

def loadImage(imgSize):
    img = pygame.image.load("red_queen.png")
    img = pygame.transform.scale(img, (imgSize, imgSize))
    return img

def drawChessBoard(surface, size, num_queens):

    rectSize = size/num_queens

    currentColor = changeColor()
    posX = posY = 0

    for x in range(num_queens):
        posX = x * rectSize
        for y in range(num_queens):
            posY = y * rectSize
            createRects(int(posX), int(posY), currentColor, rectSize, surface)
            currentColor = changeColor(currentColor)
        currentColor = changeColor(currentColor)
    pygame.display.update()




def drawSolution(surface, size, solution):
    queen = loadImage(size/len(solution))

    for posQueen in solution:
        posX = posQueen[0] * size/len(solution)
        posY = posQueen[1] * size/len(solution)
        surface.blit(queen, (posX, posY))
        pygame.display.update()
        sleep(0.1)

def changeColor(currentColor=None):
    white = Color(255, 255, 255)
    black = Color(0, 0, 0)
    
    if currentColor == white:
        return black
    else:
        return white

def createRects(posX, posY, color, rectSize, surface):
    rects = pygame.Rect(posX, posY, rectSize, rectSize)
    pygame.draw.rect(surface, color, rects)

