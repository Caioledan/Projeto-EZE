import heapq
class Djikstra():
    def __init__(self) -> None:
        pass

    
    from listaadj import ListaAdj

    def dijkstra(grafo, origem):
        dist = {vertice: float('infinity') for vertice in grafo}
        dist[origem] = 0
        anterior = {vertice: None for vertice in grafo}

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

    def reconstruct_caminho(anterior, origem, destino):
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anterior[atual]
        caminho.reverse()  #reverte o caminho para obtermos o caminho mínimo
        if caminho[0] == origem:
            return caminho
        else:
            return []


    # Exemplo de uso
    arquivo = "data\\datavalorada.txt"
    grafo = ListaAdj.lista_de_adjacencia(arquivo)
    vert_origem = '15.767335190764022,9.588007918107184'  # Substitua pelo vértice de início desejado
    vert_destino = '12.980939744070279,19.83807640240745'    # Substitua pelo vértice de destino desejado

    dist, anterior = dijkstra(grafo, vert_origem)
    # print(reconstruct_caminho(anterior, vert_origem, vert_destino))

    caminho = reconstruct_caminho(anterior, vert_origem, vert_destino)

    # for i in range(len(caminho) - 1):

    #         anterior = caminho[i]
    #         proximo = caminho[i+1]
    #         print(anterior)
    #         print(proximo)


    # print(f"Distância mínima de {vert_origem} até {vert_destino}: {dist[vert_destino]}")
    # print(f"Caminho mais curto de {vert_origem} até {vert_destino}: {shortest_caminho}")
