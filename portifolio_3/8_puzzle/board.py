class Board():
    def __init__(self, estadoInicial=None, estadoAnterior=None, moves=0) -> None:
        self.board = estadoInicial
        self.estadoAnterior = estadoAnterior
        self.moves = moves

    def __str__(self):
        string = ''
        string = string + '+---+---+---+\n'
        for i in range(3):
            for j in range(3):
                tile = self.board[i * 3 + j]
                string = string + '| {} '.format(' ' if tile == 0 else tile)
            string = string + '|\n'
            string = string + '+---+---+---+\n'
        return string

    def __eq__(self, other):
        if other is None:
            return False
        return self.board == other.board

    def objAlcancado(self):
        for i in range(0,9):
            if i != 8 and self.board[i] != i + 1:
                return False

        return True

    def movimentaVazio(self, lado):

        vazio = self.encontraVazio()

        if lado == 'U' and vazio / 3 != 0:
            col = (vazio % 3)
            row = int(vazio / 3) - 1
            self.troca(vazio, row * 3 + col)

        if lado == 'R' and vazio % 3 != 2:
            col = (vazio % 3) +1
            row = int(vazio / 3)
            self.troca(vazio, row * 3 + col)

        if lado == 'D' and vazio / 3 != 2:
            col = (vazio % 3)
            row = int(vazio / 3) + 1
            self.troca(vazio, row * 3 + col)

        if lado == 'L' and vazio / 3 != 0:
            col = (vazio % 3) - 1
            row = int(vazio / 3)
            self.troca(vazio, row * 3 + col)
        
    def encontraVazio(self):
        for i in range(0, 9):
            if self.board[i] == 0:
                return i

    def clone(self):
        return Board(self.board.copy(), self, self.moves + 1)


    def troca(self, origem, alvo):
        self.board[origem], self.board[alvo] = self.board[alvo], self.board[origem]

    def vizinhos(self):

        posVazio = self.encontraVazio()

        vizinhos = []

        if int(posVazio / 3) != 0:
            novoBoard = self.clone()
            novoBoard.movimentaVazio('U')
            vizinhos.append(novoBoard)

        if posVazio % 3 != 2:
            novoBoard = self.clone()
            novoBoard.movimentaVazio('R')
            vizinhos.append(novoBoard)


        if int(posVazio / 3) != 2:
            novoBoard = self.clone()
            novoBoard.movimentaVazio('D')
            vizinhos.append(novoBoard)

        if posVazio % 3 != 0:
            novoBoard = self.clone()
            novoBoard.movimentaVazio('L')
            vizinhos.append(novoBoard)

        return vizinhos


    def manhattanDistance(self):
        manhattan = 0
        for i in range(0,9):
            if self.board[i] != i + 1 and self.board[i] != 0:
                if self.board[i] == 0:
                    posCorreta = 8
                else:
                    posCorreta = self.board[i] - 1

                sRow = int(i / 3)
                sCol = i % 3
                tRow = int(posCorreta / 3)
                tCol = posCorreta % 3

                manhattan += abs(sRow - tRow) + abs(sCol - tCol)

        return manhattan

    def filaDePrioridade(self, count):
        return (self.moves + self.manhattanDistance(), count, self)

    def getEstadoAnterior(self):
  
        estados = [self]
        anterior = self.estadoAnterior
        while anterior is not None:
            estados.append(anterior)
            anterior = anterior.estadoAnterior

        return estados.reverse()