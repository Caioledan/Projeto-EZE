
def valorar(arquivo_origem, arquivo_destino):

    
    with open(arquivo_origem, "r+") as origem, open(arquivo_destino, 'w+') as destino:
        for linha in origem:
            linhas = linha.strip().split('--')
            ponto1 = linhas[0].strip().split(',')
            ponto2 = linhas[1].strip().split(',')
            
            p1x = float(ponto1[0])
            p1y = float(ponto1[1])
            p2x = float(ponto2[0])
            p2y = float(ponto2[1])

            valor = abs((((p2x - p1x)**2) + ((p2y - p1y)**2))**(1/2))

            destino.write(str(p1x) + "," + str(p1y) + '--' + str(p2x) + ',' + str(p2y) + '--' + str(valor) + '--\n')
        



    # origem.close()
    # destino.close()
valorar("data\dados.txt", "data\datavalorada.txt")
