# Algoritmo para reestruturar meu sistema de arquivos para Geogebra

def openData():
    file_writed = open("./data/data_tratada.txt", "+w")

    with open("./data/data.txt", "r") as f:
        for i in f:
            if not "--" in i.strip():
                file_writed.write(i)
            
            else:
                lat, long = i.split("--")
                file_writed.write("{}\n{}".format(lat, long))
            
        file_writed.close()
        f.close()

openData()