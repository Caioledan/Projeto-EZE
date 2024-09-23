import osmium as osm

# Classe para lidar com o OSM e extrair informações
class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.highway_nodes = set()  # Usamos um set para evitar duplicatas

    def node(self, n):
        # Não fazemos nada com os nodes aqui
        pass

    def way(self, w):
        if 'highway' in w.tags:
            # Adiciona os IDs dos nós ao conjunto se a way é do tipo highway
            for n in w.nodes:
                self.highway_nodes.add(n.ref)

    def save_highway_node_ids(self, filename):
        with open(filename, 'w') as f:
            for node_id in self.highway_nodes:
                f.write(f"{node_id}\n")

# Usar o handler para processar o arquivo OSM
handler = OSMHandler()
handler.apply_file('data/map.osm')  # Substitua pelo nome do seu arquivo

# Salva os IDs dos nós em um arquivo
handler.save_highway_node_ids('map/treated_map.txt')
