class KnapsackPackage(): 
    def __init__(self, peso, valor): 
        self.peso = peso 
        self.valor = valor 
        self.custo = valor / peso
 
    def __lt__(self, other): 
        return self.custo < other.custo
 
def knapsackGreedy(pesos, valores, pesoMax, numElem):
    mochila = []
    for i in range(numElem): 
        mochila.append(KnapsackPackage(pesos[i], valores[i]))
    mochila.sort(reverse = True)
    pesoRestante = pesoMax
    result = 0
    i = 0
    
    while (i < numElem):
        if (mochila[i].peso <= pesoRestante):
            pesoRestante -= mochila[i].peso
            result += mochila[i].valor
            print("Mochila ", i, " - Peso ", mochila[i].peso, " - Valor ", mochila[i].valor)
        if (mochila[i].peso > pesoRestante):
            i += 1

    print("Valor Máximo:\t", result)
 
pesos = [15, 10, 2, 4] 
valores = [30, 25, 2, 6] 
pesoLimite = 37
numElementos = 4
knapsackGreedy(pesos, valores, pesoLimite, numElementos)