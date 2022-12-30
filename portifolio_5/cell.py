import pygame

# Butões do mouse
MOUSEBUTTONLEFT = 1
MOUSEBUTTONRIGHT = 3

# Carregando os Sprites
cellImg = pygame.image.load("./sprites/Grid.png")
flagImg = pygame.image.load("./sprites/flag.png")
mineImg = pygame.image.load("./sprites/mine.png")
cellImgList = []
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

    def draw(self, screen):
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

        # self.draw()
        return self.hasMine