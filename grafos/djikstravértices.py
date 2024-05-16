import heapq

def dijkstra(grafo, origem):
    # Inicializa as distâncias e o predecessor de cada nó
    dist = {vertice: float('infinity') for vertice in grafo}
    dist[origem] = 0
    anterior = {vertice: None for vertice in grafo}
    
    # Inicializa a fila de prioridade
    fila = []
    heapq.heappush(fila, (0, origem))
    
    while fila:
        dist_atual, vert_atual = heapq.heappop(fila)
        
        if dist_atual > dist[vert_atual]:
            continue
        
        for vizinho, peso in grafo[vert_atual]:
            distance = dist_atual + float(peso)
            
            if distance < dist[vizinho]:
                dist[vizinho] = distance
                anterior[vizinho] = vert_atual
                heapq.heappush(fila, (distance, vizinho))
    
    return dist, anterior

def lista_de_adjacencia(arquivo : str) -> dict:
    with open(arquivo, "r") as arquivo:
        lista = arquivo.readlines()

    listaDeAdjacencia = {}
    for linha in lista:
        dados = linha.strip().split('--')

        if dados[0] not in listaDeAdjacencia:
            listaDeAdjacencia[dados[0]] = []
        
        if dados[1] not in listaDeAdjacencia:
            listaDeAdjacencia[dados[1]] = []

        # Adicionando a aresta
        if dados[0] != dados[1]:
            listaDeAdjacencia[dados[0]].append((dados[1], float(dados[2])))
            listaDeAdjacencia[dados[1]].append((dados[0], float(dados[2])))
        else: # Caso tenha laço
            listaDeAdjacencia[dados[1]].append((dados[0], float(dados[2])))

    for i in listaDeAdjacencia.keys():
        listaDeAdjacencia[i].sort()

    
    return listaDeAdjacencia

# Exemplo de uso
arquivo = "data\\datavalorada.txt"
grafo = lista_de_adjacencia(arquivo)
vert_origem = '12.980939744070279,19.83807640240745'  # Substitua pelo vértice de início desejado
dist, anterior = dijkstra(grafo, vert_origem)

# Exibindo as distâncias e caminhos mais curtos
print("Distâncias:", dist)
print("Caminhos mais curtos:", anterior)
