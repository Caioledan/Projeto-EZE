import heapq
import numpy as np

class PathFinder:
    def __init__(self, graph, nodes):
        self.graph = graph  # Armazena o grafo
        self.nodes = nodes  # Armazena as coordenadas dos nós

    def find_shortest_path(self, start, end): #Função que verifica o caminho mínimo entre o vértice de início e o vértice de fim
        queue = [(0, start, [])]  #Uma lista é criada como uma fila. Ela guardará tuplas, sendo essas (O custo do caminho, O nó atual, Lista com o caminho)
        visited = set() #Para fins de evitar um vértice já passado, os vértices visitados foram armazenados de forma única.

        while queue:
            cost, node, path = heapq.heappop(queue) #Extrai o vértice com menor custo

            if node in visited: #Se o vértice já foi visitado, ele é ignorado.
                continue

            path = path + [node] #Adiciona o vértice no caminho.

            if node == end: #Caso tenha chegado ao fim, retorna o caminho.
                return path
            
            visited.add(node) #Marca o vértice como visitado, para não ser chamado novamente

            for neighbor in self.graph.get(node, []): # Verifica os vértices vizinhos do atual
                if neighbor not in visited:  # Verifica se já foi visitado
                    edge_cost = self.distance(self.nodes[node], self.nodes[neighbor]) # Se não foi visitado, calcula-se o custo até ele.
                    heapq.heappush(queue, (cost + edge_cost, neighbor, path)) # Adiciona ele na fila de vértices para calcular o caminho mínimo.

        return []

    def distance(self, node1, node2): # Função que calcula a distância (Custo) de um vértice até outro.
        lat1, lon1 = node1
        lat2, lon2 = node2
        return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) # Faz a normalização e retorna
