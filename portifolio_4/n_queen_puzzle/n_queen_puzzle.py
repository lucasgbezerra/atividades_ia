def isSafe(board, row, col, num_queens):
 
    for i in range(col):
        if board[row][i] == 1:
            return False
 
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] == 1:
            return False
 
    for i, j in zip(range(row, num_queens, 1),
                    range(col, -1, -1)):
        if board[i][j] == 1:
            return False
 
    return True

def solverNQueen(board, col, num_queens, solution):
     
    if (col >= num_queens):
        return True
         
    for i in range(num_queens):
        
        if isSafe(board, i, col, num_queens):
                  
            # Posiciona rainha e adiciona a solução
            board[i][col] =  1
            solution.append([i, col])
             
            if solverNQueen(board, col + 1, num_queens,solution):
                return True
                 
            # Backtrack caso o local escolhido não leve a solução
            board[i][col] = 0
            solution.pop(-1)

    return False
