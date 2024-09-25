import osmium as osm

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.ways = []
        self.graph = {}
        self.buildings = []  # Lista para armazenar os prédios

    def node(self, n):
        self.nodes[n.id] = (n.location.lat, n.location.lon)

    def way(self, w):
        if 'highway' in w.tags:
            node_refs = [n.ref for n in w.nodes]
            self.ways.append(node_refs)
            # Cria um grafo conectando os nós adjacentes para usar no caminho mais curto
            for i in range(len(node_refs) - 1):
                self._add_edge(node_refs[i], node_refs[i + 1])

        if 'building' in w.tags:
            self.buildings.append([n.ref for n in w.nodes])  # Adiciona prédios à lista

    def _add_edge(self, node1, node2):
        if node1 not in self.graph:
            self.graph[node1] = []
        if node2 not in self.graph:
            self.graph[node2] = []
        self.graph[node1].append(node2)
        self.graph[node2].append(node1)


# Função para converter coordenadas lat/lon para coordenadas OpenGL
def latlon_to_opengl(lat, lon, bbox, z=0):
   
    min_lat, min_lon, max_lat, max_lon = bbox
    
    scale_factor = 0.5  # Ajuste esse valor para aumentar/reduzir o espaçamento
    x = ((lat - min_lat) / (max_lat - min_lat)) * 2 - 1
    y = ((lon - min_lon) / (max_lon - min_lon)) * 2 - 1
    
    # Aplique o fator de escala
    #x *= scale_factor
    #y *= scale_factor

    return x, y, z