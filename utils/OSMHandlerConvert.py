import osmium as osm

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        super().__init__()
        
        self.nodes = {}
        self.ways = []
        self.buildings = []  # Lista para armazenar os prédios

    def node(self, n):
        self.nodes[n.id] = (n.location.lat, n.location.lon)

    def way(self, w):
        if 'highway' in w.tags:
            self.ways.append([n.ref for n in w.nodes])

        if 'building' in w.tags:
            self.buildings.append([n.ref for n in w.nodes])  # Adiciona prédios à lista


# Função para converter coordenadas lat/lon para coordenadas OpenGL
def latlon_to_opengl(lat, lon, bbox, z=0):
   
    min_lat, min_lon, max_lat, max_lon = bbox
    
    scale_factor = 0.5  # Ajuste esse valor para aumentar/reduzir o espaçamento
    x = ((lat - min_lat) / (max_lat - min_lat)) * 2 - 1
    y = ((lon - min_lon) / (max_lon - min_lon)) * 2 - 1
    
    # Aplique o fator de escala
    x *= scale_factor
    y *= scale_factor

    return x, y, z