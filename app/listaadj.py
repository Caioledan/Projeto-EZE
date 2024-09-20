class ListaAdj():
    def __init__(self) -> None:
        pass

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

            if dados[0] != dados[1]:
                listaDeAdjacencia[dados[0]].append((dados[1], float(dados[2])))
                listaDeAdjacencia[dados[1]].append((dados[0], float(dados[2])))
            else:
                listaDeAdjacencia[dados[1]].append((dados[0], float(dados[2])))

        for i in listaDeAdjacencia.keys():
            listaDeAdjacencia[i].sort()
        
        return listaDeAdjacencia