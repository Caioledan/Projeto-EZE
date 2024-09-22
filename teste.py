import osmium as osm
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

rotation_x = 0
rotation_y = 0
zoom = 1  # Zoom inicial (mais perto do que antes)
move_x = 0  # Controle de movimentação no eixo X
move_y = 0  # Controle de movimentação no eixo Y
move_speed = 0.1  # Velocidade de movimento do mapa

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        super().__init__()
        
        self.nodes = {}
        self.ways = []

    def node(self, n):
        self.nodes[n.id] = (n.location.lat, n.location.lon)

    def way(self, w):
        if 'highway' in w.tags:
            self.ways.append([n.ref for n in w.nodes])

# Função para converter coordenadas lat/lon para coordenadas OpenGL
def latlon_to_opengl(lat, lon, bbox, z=0):
    min_lat, min_lon, max_lat, max_lon = bbox

    # Calcula o centro do mapa
    # center_lat = (min_lat + max_lat) / 2
    # center_lon = (min_lon + max_lon) / 2

    x = ((lat - min_lat) / (max_lat - min_lat)) * 2 - 1
    y = ((lon - min_lon) / (max_lon - min_lon)) * 2 - 1
    

    # # Aumenta o fator de escala
    # lat_range = max_lat - min_lat
    # lon_range = max_lon - min_lon
    # scale_factor = max(lat_range, lon_range) / 2  # Ajuste o fator de escala

    # Converte lat/lon para coordenadas 3D OpenGL [-1, 1]
    # x = (lon - center_lon) / scale_factor
    # y = (lat - center_lat) / scale_factor
    return x, y, z

# Função para desenhar ruas com profundidade (prismas)
def draw_map_with_depth(nodes, ways, bbox, street_width=0.0010, depth=0.001):
    glLineWidth(20)
    glColor3f(65.0/255.0, 85.0/255.0, 103.0/255.0)  # Cor branca para as ruas
    glBegin(GL_QUADS)  # Usamos quadrados em vez de linhas

    for way in ways:
        for i in range(len(way) - 1):
            # Pega os dois nós consecutivos que representam uma rua
            node1 = nodes[way[i]]
            node2 = nodes[way[i + 1]]

            # Converte as coordenadas lat/lon em coordenadas OpenGL
            x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0)
            x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)

            # Aumenta a escala das coordenadas
            # x1 *= scale_factor
            # y1 *= scale_factor
            # x2 *= scale_factor
            # y2 *= scale_factor

            # Vetor de direção da rua (vetor entre os dois nós)
            direction = np.array([x2 - x1, y2 - y1])
            direction = direction / np.linalg.norm(direction)  # Normaliza o vetor

            # Vetor perpendicular à rua (para criar a largura)
            perpendicular = np.array([-direction[1], direction[0]]) * street_width

            # Calcula os quatro vértices do prisma que formará a rua
            v1 = [x1 + perpendicular[0], y1 + perpendicular[1], z1]
            v2 = [x1 - perpendicular[0], y1 - perpendicular[1], z1]
            v3 = [x2 + perpendicular[0], y2 + perpendicular[1], z2]
            v4 = [x2 - perpendicular[0], y2 - perpendicular[1], z2]

            # Desenha as faces superior e inferior da rua (como um prisma)
            glVertex3f(v1[0], v1[1], z1 + depth)  # Face superior
            glVertex3f(v2[0], v2[1], z1 + depth)
            glVertex3f(v4[0], v4[1], z2 + depth)
            glVertex3f(v3[0], v3[1], z2 + depth)

            glVertex3f(v1[0], v1[1], z1)  # Face inferior
            glVertex3f(v2[0], v2[1], z1)
            glVertex3f(v4[0], v4[1], z2)
            glVertex3f(v3[0], v3[1], z2)

            # Desenha as laterais (paredes) da rua para dar profundidade
            glVertex3f(v1[0], v1[1], z1 + depth)
            glVertex3f(v1[0], v1[1], z1)
            glVertex3f(v3[0], v3[1], z2)
            glVertex3f(v3[0], v3[1], z2 + depth)

            glVertex3f(v2[0], v2[1], z1 + depth)
            glVertex3f(v2[0], v2[1], z1)
            glVertex3f(v4[0], v4[1], z2)
            glVertex3f(v4[0], v4[1], z2 + depth)
            
    glEnd()

# Função para ler o arquivo OSM e extrair as coordenadas e vias
def read_osm(filename):
    handler = OSMHandler()
    handler.apply_file(filename)

    # Encontrar os limites geográficos (bounding box)
    lats = [coord[0] for coord in handler.nodes.values()]
    lons = [coord[1] for coord in handler.nodes.values()]
    bbox = (min(lats), min(lons), max(lats), max(lons))

    return handler.nodes, handler.ways, bbox

# Função para configurar o modo de perspectiva 3D
def setup_3d_view():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 800 / 600, 0.1, 100.0)  # Ângulo de visão, proporção e profundidade ajustados
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, zoom, 0, 0, 0, 0, 1, 0)
    glEnable(GL_DEPTH_TEST)


# Função para desenhar casas (cubos/prismas) ao lado das ruas
def draw_buildings(nodes, ways, bbox, building_width=0.002, building_height=0.001):
    glColor3f(0.7, 0.7, 0.7)  # Cor cinza para os prédios
    glBegin(GL_QUADS)
    
    for way in ways:
        for i in range(len(way) - 1):
            # Pega os dois nós consecutivos que representam uma rua
            node1 = nodes[way[i]]
            node2 = nodes[way[i + 1]]

            # Converte as coordenadas lat/lon em coordenadas OpenGL
            x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0)
            x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)

            # Vetor de direção da rua (vetor entre os dois nós)
            direction = np.array([x2 - x1, y2 - y1])
            direction = direction / np.linalg.norm(direction)  # Normaliza o vetor

            # Vetor perpendicular à rua (para posicionar os edifícios ao lado das ruas)
            perpendicular = np.array([-direction[1], direction[0]]) * building_width

            # Calcula os quatro vértices do prédio ao lado da rua
            b1 = [x1 + perpendicular[0], y1 + perpendicular[1], z1]
            b2 = [x1 - perpendicular[0], y1 - perpendicular[1], z1]
            b3 = [x2 + perpendicular[0], y2 + perpendicular[1], z2]
            b4 = [x2 - perpendicular[0], y2 - perpendicular[1], z2]

            # Desenha o prédio como um prisma com altura variável
            for i in range(2):  # Desenha dois prédios (um de cada lado da rua)
                # Desloca o prédio para longe da rua no lado perpendicular
                offset = perpendicular * (i * 2 - 1)  # Alterna entre os dois lados

                # Vértices superiores do prédio
                v1 = [b1[0] + offset[0], b1[1] + offset[1], z1 + building_height]
                v2 = [b2[0] + offset[0], b2[1] + offset[1], z1 + building_height]
                v3 = [b4[0] + offset[0], b4[1] + offset[1], z2 + building_height]
                v4 = [b3[0] + offset[0], b3[1] + offset[1], z2 + building_height]

                # Face superior
                glVertex3f(v1[0], v1[1], v1[2])
                glVertex3f(v2[0], v2[1], v2[2])
                glVertex3f(v3[0], v3[1], v3[2])
                glVertex3f(v4[0], v4[1], v4[2])

                # Face inferior
                glVertex3f(b1[0] + offset[0], b1[1] + offset[1], z1)
                glVertex3f(b2[0] + offset[0], b2[1] + offset[1], z1)
                glVertex3f(b4[0] + offset[0], b4[1] + offset[1], z2)
                glVertex3f(b3[0] + offset[0], b3[1] + offset[1], z2)

                # Laterais do prédio
                glVertex3f(v1[0], v1[1], v1[2])
                glVertex3f(v1[0], v1[1], z1)
                glVertex3f(v4[0], v4[1], z2)
                glVertex3f(v4[0], v4[1], v4[2])

                glVertex3f(v2[0], v2[1], v2[2])
                glVertex3f(v2[0], v2[1], z1)
                glVertex3f(v3[0], v3[1], z2)
                glVertex3f(v3[0], v3[1], v3[2])

    glEnd()


# Função principal
def main():
    global rotation_x, rotation_y, zoom, move_x, move_y, move_speed
    # Inicializa pygame
    pygame.init()
    display = (1080, 920)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(39.0/255.0, 45.0/255.0, 57.0/255.0, 1.0)  # Cor de fundo azul claro (R, G, B, A)
    # Configura a visualização 3D

    # Lê o arquivo OSM
    filename = "limoeiro.osm"  # Substitua pelo caminho do arquivo .osm
    nodes, ways, bbox = read_osm(filename)

    # Variáveis de controle de rotação, zoom e posição do mapa
    rotation_x = 0
    rotation_y = 0
    zoom = 1  # Zoom inicial (mais perto do que antes)
    move_x = 0  # Controle de movimentação no eixo X
    move_y = 0  # Controle de movimentação no eixo Y
    move_speed = 0.1  # Velocidade de movimento do mapa

    # Loop principal do pygame
    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    

        setup_3d_view()

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controle de rotação, zoom e movimento com o teclado
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rotation_y -= 1
        if keys[K_RIGHT]:
            rotation_y += 1
        if keys[K_UP]:
            rotation_x -= 1
        if keys[K_DOWN]:
            rotation_x += 1
        if keys[K_EQUALS] or keys[K_PLUS]:  # Tecla '+' para aumentar o zoom
            print(zoom)
            zoom -= 0.1  # Aproxima a câmera
        if keys[K_MINUS]:  # Tecla '-' para diminuir o zoom
            print(zoom)
            zoom += 0.1  # Afasta a câmera

        # Movimentação do mapa com as teclas W, A, S, D
        if keys[K_w]:
            move_y -= move_speed  # Move o mapa para cima
        if keys[K_s]:
            move_y += move_speed  # Move o mapa para baixo
        if keys[K_a]:
            move_x -= move_speed  # Move o mapa para a esquerda
        if keys[K_d]:
            move_x += move_speed  # Move o mapa para a direita


        # Aplica rotação no mapa
        glRotatef(rotation_x, 1, 0, 0)  # Rotaciona em torno do eixo X
        glRotatef(rotation_y, 0, 1, 0)  # Rotaciona em torno do eixo Y

        # Aplica movimentação no mapa
        glTranslatef(move_x, move_y, 0)  # Move o mapa para cima/baixo e esquerda/direita

        # Desenha o mapa com profundidade
        draw_map_with_depth(nodes, ways, bbox)

        # Funcao para fazer a construcoes do mapa
        # draw_buildings(nodes, ways, bbox)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()