import pygame
from re import compile
IMGS = {}
def resizeImage(image, size):
    return pygame.transform.scale(image, size)

# Carregando os Sprites
# Lista de sprites 0-8: números, 9: vazia, 10: flag, 11: mina
def setImages(width , height):
    images = {}
    paths = []
    for i in range(0,9):
        paths.append("./sprites/grid" + str(i) + ".png")
    paths.append("./sprites/flag.png")
    paths.append("./sprites/mine.png")
    paths.append("./sprites/grid.png")  

    pattern = compile(r"/([^/]*)\.png")
    for p in paths :
        image = pygame.image.load(p)
        image = resizeImage(image, (width, height))
        images[pattern.search(p).group(1)] = image

    return images
