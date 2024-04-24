
def remover_linhas_repetidas(arquivo_origem, arquivo_destino):

    
    with open(arquivo_origem, "r+") as origem, open(arquivo_destino, 'w+') as destino:
        for linha in origem:
            linhas = linha.strip().split(',')

            p1 = float(linhas[0])
            p2 = float(linhas[1])

            valor = abs(p1 - p2)

            destino.write(linhas[0] + ',' + linhas[1] + ',' +  str(valor) + '\n')
        



    # origem.close()
    # destino.close()
remover_linhas_repetidas("Trabalho\data.txt", "Trabalho\datatratada.txt")
