def dls(src,target,maxDepth):
    if src == target : return True
    if maxDepth <= 0 : return False

    for i in graph[src]:
        if(dls(i,target,maxDepth-1)):
            return True
    return False

def iddfs(src, target, maxDepth):
    for i in range(maxDepth):
        if (dls(src, target, i)):
            return True
    return False

graph = {
    0 : [1, 2],
    1 : [0, 3, 4],
    2 : [0, 5, 6],
    3 : [1],
    4 : [1],
    5 : [2],
    6 : [2]
}

target = 6; maxDepth = 3; src = 0

if iddfs(src, target, maxDepth) == True:
	print (f"O alvo é alcançado com a profundidade máxima {maxDepth}")
else :
	print (f"O alvo NÃO é alcançado com a profundidade máxima {maxDepth}")