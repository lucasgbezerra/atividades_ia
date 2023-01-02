import random
from sentence import Sentence
from itertools import combinations

class Solver():
    def __init__(self, rows, cols):
        self.cols = rows
        self.rows = cols
        self.revealed = set()
        self.mines = set()
        self.safes = set()

        # Base de conhecimento composta por sentenças
        self.knowledgeBase = []

        self.numRandomMoves = 0
        self.numSafeMoves = 0

    def markMine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledgeBase:
            sentence.removeMine(cell)

    def markSafe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledgeBase:
            sentence.removeSafe(cell)

    def addKnowledge(self, cell, cells):
        self.markSafe(cell)
        self.revealed.update(([c.getPosition() for c in cells]))

        for c in cells:
            if c.adjacentMines == 0:
                continue
            row, col = c.getPosition()
            neighbors = []
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    
                    if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
                        continue

                    if (i, j) in self.revealed:
                        continue
                    
                    neighbors.append((i,j))

            if len(neighbors) == 0:
                continue

            if len(neighbors) == c.adjacentMines:
                self.mines.update(neighbors)
            
            sentence = Sentence(neighbors, c.adjacentMines)
            if sentence in self.knowledgeBase: 
                return
            self.knowledgeBase.append(sentence)
            self.safes.update(sentence.knownSafes())
            self.mines.update(sentence.knownMines())

    def makeMove(self):

        safeMoves = self.safes.difference(self.revealed)

        if len(safeMoves) != 0:
            print("IA fazendo movimento seguro")
            safeMove = random.choice(list(safeMoves))
            self.numSafeMoves += 1
            # print("----- SAFE MOVES ----")
            # print(f"Moves: {len(self.revealed)} SAFES: {len(self.safes)}")
            # print(f"MOVES: {self.revealed}")
            # print(f"SAFES: {self.safes}")
            # print(f"SAFE MOVES: {safeMoves}")
            # print(f"Movimento seguro ({self.numSafeMoves}): {safeMove}")
            # print("----- SAFE MOVES ----")
            return (safeMove[0], safeMove[1])
        else:
            return self.makeRandomMove()
            

    def makeRandomMove(self):
        print("Realizando movimento aleatório!")
        randomMove = None

        while randomMove == None:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)

            if (row, col) in self.revealed:
                continue
            if (row, col) in self.mines:
                continue

            randomMove = (row, col)

        if randomMove != None:
            self.numRandomMoves += 1
            print(f"Random move ({self.numRandomMoves}): {randomMove}")
            self.revealed.add(randomMove)
            return randomMove
        else:
            return None

    