from queue import PriorityQueue

def aStarSolve(initialBoard):

    queue = PriorityQueue()
    queue.put(initialBoard.filaDePrioridade(0))

    i = 1
    passo = 0 
    while not queue.empty():
        board = queue.get()[2]
        print(f"Passo {passo}:\n{board}")

        if not board.objAlcancado():
            for vizinho in board.vizinhos():
                if vizinho != board.estadoAnterior:
                    queue.put(vizinho.filaDePrioridade(i))
                    i += 1
        else:
            return board.getEstadoAnterior()
        passo += 1

    return None
