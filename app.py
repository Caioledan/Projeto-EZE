import osmium as osm
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PathFinder import *
from randomico import Randomic


# Classe para lidar com o OSM e extrair informações
class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.ways = []
        self.graph = {}

    def node(self, n):
        self.nodes[n.id] = (n.location.lat, n.location.lon)

    def way(self, w):
        if 'highway' in w.tags:
            node_refs = [n.ref for n in w.nodes]
            self.ways.append(node_refs)
            # Cria um grafo conectando os nós adjacentes para usar no caminho mais curto
            for i in range(len(node_refs) - 1):
                self._add_edge(node_refs[i], node_refs[i + 1])

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
    x = ((lat - min_lat) / (max_lat - min_lat)) * 2 - 1
    y = ((lon - min_lon) / (max_lon - min_lon)) * 2 - 1
    return x, y, z

# Função para desenhar ruas com profundidade (prismas)
def draw_map_with_depth(nodes, ways, bbox, street_width=0.0010, depth=0.0001):
    glColor3f(65.0/255.0, 85.0/255.0, 103.0/255.0)  # Cor padrão para as ruas
    glBegin(GL_QUADS)

    for way in ways:
        for i in range(len(way) - 1):
            node1 = nodes[way[i]]
            node2 = nodes[way[i + 1]]
            x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0)
            x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)
            direction = np.array([x2 - x1, y2 - y1])
            direction = direction / np.linalg.norm(direction)
            perpendicular = np.array([-direction[1], direction[0]]) * street_width
            v1 = [x1 + perpendicular[0], y1 + perpendicular[1], z1]
            v2 = [x1 - perpendicular[0], y1 - perpendicular[1], z1]
            v3 = [x2 + perpendicular[0], y2 + perpendicular[1], z2]
            v4 = [x2 - perpendicular[0], y2 - perpendicular[1], z2]
            glVertex3f(v1[0], v1[1], z1 + depth)
            glVertex3f(v2[0], v2[1], z1 + depth)
            glVertex3f(v4[0], v4[1], z2 + depth)
            glVertex3f(v3[0], v3[1], z2 + depth)
            glVertex3f(v1[0], v1[1], z1)
            glVertex3f(v2[0], v2[1], z1)
            glVertex3f(v4[0], v4[1], z2)
            glVertex3f(v3[0], v3[1], z2)
    glEnd()

# Função para desenhar o caminho em rosa
def draw_path(nodes, path, bbox, street_width=0.0010, depth=0.0001):
    glColor3f(1.0, 0.0, 1.0)  # Cor rosa
    glBegin(GL_QUADS)

    for i in range(len(path) - 1):
        node1 = nodes[path[i]]
        node2 = nodes[path[i + 1]]
        x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0)
        x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)
        direction = np.array([x2 - x1, y2 - y1])
        direction = direction / np.linalg.norm(direction)
        perpendicular = np.array([-direction[1], direction[0]]) * street_width
        v1 = [x1 + perpendicular[0], y1 + perpendicular[1], z1]
        v2 = [x1 - perpendicular[0], y1 - perpendicular[1], z1]
        v3 = [x2 + perpendicular[0], y2 + perpendicular[1], z2]
        v4 = [x2 - perpendicular[0], y2 - perpendicular[1], z2]
        glVertex3f(v1[0], v1[1], z1 + depth)
        glVertex3f(v2[0], v2[1], z1 + depth)
        glVertex3f(v4[0], v4[1], z2 + depth)
        glVertex3f(v3[0], v3[1], z2 + depth)
        glVertex3f(v1[0], v1[1], z1)
        glVertex3f(v2[0], v2[1], z1)
        glVertex3f(v4[0], v4[1], z2)
        glVertex3f(v3[0], v3[1], z2)
    glEnd()



# Função para ler o arquivo OSM e extrair as coordenadas e vias
def read_osm(filename):
    handler = OSMHandler()
    handler.apply_file(filename)
    lats = [coord[0] for coord in handler.nodes.values()]
    lons = [coord[1] for coord in handler.nodes.values()]
    bbox = (min(lats), min(lons), max(lats), max(lons))
    return handler.nodes, handler.ways, handler.graph, bbox

def setup_3d_view():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (1080 / 920), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Função principal
def main():
    global rotation_x, rotation_y, zoom, move_x, move_y, move_speed

    pygame.init()

    display = (1080, 920)

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(39.0/255.0, 45.0/255.0, 57.0/255.0, 1.0)

    filename = "map.osm"
    nodes, ways, graph, bbox = read_osm(filename)

    random = Randomic()

    pathfinder = PathFinder(graph, nodes)
    n1, n2 = random.randomizer()
    print(n1 + "\n" + n2)
    start_node = int(n1)
    end_node = int(n2)

    # print(start_node + "\n" + end_node)


    path = pathfinder.find_shortest_path(start_node, end_node)

    rotation_x = 0
    rotation_y = 0
    zoom = 1
    move_x = 0
    move_y = 0
    move_speed = 0.005

    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        setup_3d_view()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rotation_y -= 1
        if keys[K_RIGHT]:
            rotation_y += 1
        if keys[K_UP]:
            rotation_x -= 1
        if keys[K_DOWN]:
            rotation_x += 1
        if keys[K_EQUALS] or keys[K_PLUS]:
            zoom -= 0.1
        if keys[K_MINUS]:
            zoom += 0.1
        if keys[K_w]:
            move_y -= move_speed
        if keys[K_s]:
            move_y += move_speed
        if keys[K_a]:
            move_x += move_speed
        if keys[K_d]:
            move_x -= move_speed

        glPushMatrix()
        glTranslatef(move_x, move_y, -zoom)
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)

        draw_map_with_depth(nodes, ways, bbox)
        draw_path(nodes, path, bbox)

        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
