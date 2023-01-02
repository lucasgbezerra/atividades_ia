class Sentence():
    def __init__(self, cells, numMines):
        self.cells = set(cells)
        self.numMines = numMines

    def __eq__(self, other):
        return self.cells == other.cells and self.numMines == other.numMines

    def __str__(self):
        return f"{self.cells} = {self.numMines}"

    def knownMines(self):
        mines = set()

        if len(self.cells) == self.numMines: 
            for cell in self.cells: 
                mines.add(cell)

            for cell in mines:
                self.removeMine(cell)

        return mines

    def knownSafes(self):
        safes = set()

        if self.numMines == 0:
            for cell in self.cells: 
                safes.add(cell)
        
            for cell in safes:
                self.removeSafe(cell)

        return safes

    def removeMine(self, cell):
        if (cell) in self.cells:
            self.cells.remove(cell)
            self.numMines -= 1

    def removeSafe(self, cell):
        if (cell) in self.cells:
            self.cells.remove(cell)
