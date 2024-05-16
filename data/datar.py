def valorar(arquivo_origem, arquivo_destino):

    
    with open(arquivo_origem, "r+") as origem, open(arquivo_destino, 'w+') as destino:
        i = 1
        for linha in origem:
            linhas = linha

            destino.write(str(i) + "--" + linhas)
            i += 1



valorar("data\dados.txt", "data\datavalorada.txt")
