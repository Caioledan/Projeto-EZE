def lista_de_adjacencia(arquivo : str) -> dict:

    with open(arquivo, "r") as arquivo:
        lista = arquivo.readlines()

    listaDeAdjacencia = {}
    for linha in lista:
        dados = linha.split(',')

        if float(dados[0]) not in listaDeAdjacencia:
            listaDeAdjacencia[dados[0]] = []
        
        if float(dados[1]) not in listaDeAdjacencia:
            listaDeAdjacencia[dados[1]] = []

        # Adicionando a aresta
        if (float(dados[0]) != float(dados[1])): 
            listaDeAdjacencia[dados[0]].append((dados[1], (dados[2])))
            listaDeAdjacencia[dados[1]].append((dados[0], (dados[2])))
        else: # Caso tenha laço
            listaDeAdjacencia[dados[1]].append((dados[0], (dados[2])))

    for i in listaDeAdjacencia.keys():
        listaDeAdjacencia[i].sort()

    # return listaDeAdjacencia
    arq = open("data\\teste.txt","w+")

    # arq.write(str(listaDeAdjacencia))
    for chave,valor in listaDeAdjacencia.items():
        print(chave, ":", valor)
        arq.write(str(chave))
        arq.write(':')
        arq.write(str(valor))
        arq.write('\n')

lista_de_adjacencia("data\\datavalorada.txt")

        