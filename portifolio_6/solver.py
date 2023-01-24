import random
from sentence import Sentence
from itertools import combinations

# MOVES = [(2,2), (2, 4), (3, 4), (4, 4), (4, 0), (2, 0)]
class Solver():
    def __init__(self, rows, cols, num_mines):
        self.cols = cols
        self.rows = rows
        self.revealed = set()
        self.mines = set()
        self.safes = set()
        self.numMines = num_mines
        # Base de conhecimento composta por sentenças
        self.knowledgeBase = []
        
        self.generalProb = num_mines/(rows*cols)
        self.probs = self.initProbs()

        self.numProbMoves = 0
        self.numRandomMoves = 0
        self.numSafeMoves = 0

    def reset(self):
        self.revealed.clear()
        self.mines.clear()
        self.safes.clear()
        self.knowledgeBase = []
        self.numProbMoves = 0
        self.numSafeMoves = 0
        self.numRandomMoves = 0

        self.generalProb = self.numMines/(self.rows*self.cols)
        self.probs = self.initProbs()

    def initProbs(self):
        probs = []
        for i in range(self.rows):
            probs.append([self.generalProb]*self.cols)
        return probs
    
    def markMine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledgeBase:
            sentence.removeMine(cell)

    def markSafe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledgeBase:
            sentence.removeSafe(cell)

    def addKnowledge(self, cell, cells):
        self.revealed.update(([c.getPosition() for c in cells]))
        self.markSafe(cell)
        # print(f"Base: {len(self.knowledgeBase)}")

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
            
            self.createSentence(neighbors, c.adjacentMines)
        
        self.inference()
        self.cleanKnowledge()

    def cleanKnowledge(self):
        for s in self.knowledgeBase:
            while self.knowledgeBase.count(s) > 1:
                self.knowledgeBase.remove(s)

        for s in self.knowledgeBase:
            if len(s.cells) == 0:
                self.knowledgeBase.remove(s)
                    
    def updateKnowlegde(self):
        for sentence in self.knowledgeBase:      
            self.safes.update(sentence.knownSafes())
            self.mines.update(sentence.knownMines())

            for cell in self.safes:
                self.markSafe(cell)
            for cell in self.mines:
                self.markMine(cell)

            if len(sentence.cells) == 0:
                self.knowledgeBase.remove(sentence)
    
    def createSentence(self, neighbors, numMines):
        sentence = Sentence(sorted(neighbors), numMines)
        if sentence in self.knowledgeBase:
            return
                
        self.knowledgeBase.append(sentence)
        self.safes.update(sentence.knownSafes())
        self.mines.update(sentence.knownMines())

        self.updateKnowlegde()

    def inference(self):
        inferences = []
        for sentence, sentence1 in combinations(self.knowledgeBase, 2):
            if sentence == sentence1:
                continue
            
            if sentence.cells.issubset(sentence1.cells):
                cells = sentence1.cells - sentence.cells
                numMines = sentence1.numMines - sentence.numMines
                inferences.append((cells, numMines))

            if sentence1.cells.issubset(sentence.cells):
                cells = sentence.cells - sentence1.cells
                numMines = sentence.numMines - sentence1.numMines
                inferences.append((cells, numMines))

        if len(inferences) > 0:
            for c, m in inferences:
                self.createSentence(c,m)

    def makeMove(self):
        safemoves = self.safes - self.revealed
        if len(safemoves) != 0:
            self.numSafeMoves += 1
            safeMove = random.choice(list(safemoves))
            print(f"IA fazendo movimento seguro ({self.numSafeMoves}: {safeMove})")

            return (safeMove[0], safeMove[1])
        else:
            return None
        # move  = None
        # if len(MOVES) > 0:
        #     move = MOVES.pop(0)
        # return move

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
            print(f"Random move ({self.numProbMoves}): {randomMove}")
            self.revealed.add(randomMove)
            return randomMove
        else:
            return None
        # move  = None
        # if len(MOVES) > 0:
        #     move = MOVES.pop(0)
        # return move

    def  probBasedMove(self, numMines, numCells, board):

        print(f"REVELADOS: {self.revealed}")
        print(f"MINAS: {self.mines}")
        print(f"SAFES: {self.safes}")
        unknownNeighbors = set()

        if len(self.revealed) == 0:
            return self.makeRandomMove()

        for cell in self.revealed:
            unknownNeighbors.clear()
            self.probs[cell[0]][cell[1]] = 0

            if cell in self.mines:
                continue

            adMines = board.grid[cell[0]][cell[1]].adjacentMines
            if adMines == 0:
                continue

            neighbors = board.getUnrevealedNeighborsPosition((cell[0], cell[1]))
            if len(neighbors) == 0:
                continue
            
            for neigh in neighbors:
                if neigh in self.mines:
                    adMines -= 1
                else:
                    unknownNeighbors.add(neigh)

            if len(unknownNeighbors) == 0:
                continue
            prob = adMines/len(unknownNeighbors)
            print(f"Base prob: {prob}")
            print(f"CELL: {cell[0], cell[1]}")
            
            for (x, y) in unknownNeighbors:
                print(f"N-CELL: {x, y} => PROB {self.probs[x][y]}")
                if self.probs[x][y] == 1 or self.probs[x][y] == 0:
                    continue
                if prob == 0 or prob == 1:
                    self.probs[x][y] = prob
                else:
                    self.probs[x][y] = (self.probs[x][y] + prob)/2

                print(f"N-CELL: {x, y} => PROB {self.probs[x][y]}")
        self.numProbMoves += 1
        return self.recalcProbs((numMines - len(self.mines) ),(numCells - len(self.revealed)+len(self.mines)))

    def recalcProbs(self, mines, cellsUnrevealed):
        if cellsUnrevealed == 0:
            return None
        prob = self.generalProb
        self.generalProb = mines/cellsUnrevealed
        bestProb = 1
        bestMoves = []

        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) in self.mines:
                    self.probs[i][j] = 1
                elif (i, j) in self.revealed:
                    self.probs[i][j] = 0
                elif self.probs[i][j] == prob:
                        self.probs[i][j] = self.generalProb
                if self.probs[i][j] <= bestProb and (i, j) not in self.revealed:
                    if self.probs[i][j] < bestProb:
                        bestProb = self.probs[i][j]
                        bestMoves.clear()
                        bestMoves.append((i, j))
                    else:
                        bestMoves.append((i, j))


        for i in range(self.rows):
            print(f"{i} -> {self.probs[i]}")
        
        print(f"MOVES= {bestMoves}")
        bestMove  = random.choice(bestMoves)
        print(f"MOVE: {bestMove} PROB: {bestProb*100:.2f}%")
        self.revealed.add(bestMove)
        return bestMove
                