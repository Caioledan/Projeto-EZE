from queue import PriorityQueue

def lista_de_adjacencia(arquivo : str) -> dict:

    with open(arquivo, "r") as arquivo:
        lista = arquivo.readlines()

    listaDeAdjacencia = {}
    for linha in lista:
        dados = linha.split(',')

        if dados[0] not in listaDeAdjacencia:
            listaDeAdjacencia[dados[0]] = []
        if dados[1] not in listaDeAdjacencia:
            listaDeAdjacencia[dados[1]] = []

        if (dados[0] != dados[1]):
            listaDeAdjacencia[dados[0]].append((dados[1],dados[2]))
            listaDeAdjacencia[dados[1]].append((dados[0],dados[2]))
        else:
            listaDeAdjacencia[dados[1]].append((dados[0],dados[2]))

    for i in listaDeAdjacencia.keys():
        listaDeAdjacencia[i].sort()

    return listaDeAdjacencia

from queue import PriorityQueue

def Dijkstra(listaDeAdjacencia, s):
    dist = {}  
    pi = {}    
    Q = PriorityQueue()  
    
    
    for u in listaDeAdjacencia.keys():
        dist[u] = float('inf')  
        pi[u] = None             
    dist[s] = 0                  
    Q.put((0, s))                
    
   
    while not Q.empty():
        _, u = Q.get()  
        for v, w_uv in listaDeAdjacencia[u]:  
            w_uv = float(w_uv)  
            if dist[v] > dist[u] + w_uv:  
                dist[v] = dist[u] + w_uv  
                pi[v] = u                  
                Q.put((dist[v], v))        
                
    return dist, pi


listaDeAdjacencia = lista_de_adjacencia("data\\datavalorada.txt")

# Escolher o vértice de origem (s)
s = '-6.741179193301959'

# Executar o algoritmo de Dijkstra
distancias, predecessores = Dijkstra(listaDeAdjacencia, s)

# Exibir os resultados

for v, pred in predecessores.items():
    print("Predecessor de", v, ":", pred)
for v, dist in distancias.items():
    print("Para o vértice", v, ":", dist)






        