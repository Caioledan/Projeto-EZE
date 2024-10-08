import random

class Randomic:
    def __init__(self):
        self.n1 = random.randint(1, 1683)  # O intervalo deve ser de 0 a 1683 para acessar corretamente a lista
        self.n2 = random.randint(1, 1683)

    def randomizer(self):
        with open("map_data/treated_map.txt", 'r') as r:  # O arquivo lido é um arquivo com todos os IDs dos vértices do mapa
            linhas = r.readlines()

        # Verifica se os números aleatórios estão dentro do intervalo de linhas disponíveis
        if self.n1 < len(linhas) and self.n2 < len(linhas):
            return linhas[self.n1].strip(), linhas[self.n2].strip() # Então retorna os IDs de dois nós aleatórios

