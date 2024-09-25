from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from utils.OSMHandlerConvert import latlon_to_opengl


# Função para desenhar ruas com profundidade (prismas)
def draw_map_with_depth(nodes, ways, bbox, street_width=0.001, depth=0.001):
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


# Função para desenhar o caminho em ciano
def draw_path(nodes, path, bbox): # O código recebe a lista de vértices do mapa, as IDs de vértices utilizadas no caminho e as coordenadas de mapa bbox
    glColor3f(40.0/255.0, 224.0/255.0, 254.0/255.0)  # Cor ciano para o caminho
    glLineWidth(5)  # Largura da linha para destacar o caminho
    glBegin(GL_LINES)


    for i in range(len(path) - 1): # Para cada ID de vértice no caminho ele irá:
        node1 = nodes[path[i]] # Receber em uma variável o vértice ligado ao ID no path
        node2 = nodes[path[i + 1]] # Faz o mesmo porém para verificar o próximo vértice

        x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0) # Faz a normalização das coordenadas do osm para as coordenadas do OpenGl
        x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)

        # Desenha uma linha entre os dois nós
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)

    glEnd()

# Função para desenhar um caminho pre-setado em ciano
def draw_pre_path(trajeto):
    glColor3f(40.0/255.0, 224.0/255.0, 254.0/255.0)
    glLineWidth(5)
    glBegin(GL_LINES)

    # Utiliza a mesma lógica de draw_path porém com coordenadas de vértices ao invés de IDs de vértices
    for i in trajeto:
        glVertex3f(*i)

    glEnd()


def draw_buildings_as_cubes(nodes, buildings, bbox, building_width=0.0001, building_height=0.003):
    glColor3f(0.7, 0.7, 0.7)  # Cor cinza para os prédios
    glBegin(GL_QUADS)  # Usamos quadrados para desenhar as faces

    for building in buildings:
        if len(building) < 2:
            continue

        vertices = []
        for node_id in building:
            node = nodes.get(node_id)
            if node:
                x, y, z = latlon_to_opengl(node[0], node[1], bbox, z=0)
                vertices.append([x, y, z])

        # Se não houver vértices suficientes para desenhar o prédio, continue
        if len(vertices) < 3:
            continue

        # Desenhar as faces do prédio como cubo
        for i in range(len(vertices)):
            # Para cada vértice i e o próximo vértice next_i (para fechar o polígono), desenha-se a base do cubo.
            # A base é desenhada com os quatro vértices ao redor de cada ponto do prédio, ajustando as coordenadas em relação à largura do prédio (building_width).

            next_i = (i + 1) % len(vertices)

            # Face inferior (base do cubo)
            glVertex3f(vertices[i][0] - building_width/2, vertices[i][1] - building_width/2, 0)
            glVertex3f(vertices[next_i][0] - building_width/2, vertices[next_i][1] - building_width/2, 0)
            glVertex3f(vertices[next_i][0] + building_width/2, vertices[next_i][1] + building_width/2, 0)
            glVertex3f(vertices[i][0] + building_width/2, vertices[i][1] + building_width/2, 0)

            # Face superior (teto do cubo)
            glVertex3f(vertices[i][0] - building_width/2, vertices[i][1] - building_width/2, building_height)
            glVertex3f(vertices[next_i][0] - building_width/2, vertices[next_i][1] - building_width/2, building_height)
            glVertex3f(vertices[next_i][0] + building_width/2, vertices[next_i][1] + building_width/2, building_height)
            glVertex3f(vertices[i][0] + building_width/2, vertices[i][1] + building_width/2, building_height)

            # Desenhar as faces laterais (laterais do cubo)
            # Lado 1
            # Para cada par de vértices, desenha-se também as laterais, ligando a base ao teto e seus casos analogos
            glVertex3f(vertices[i][0] - building_width/2, vertices[i][1] - building_width/2, 0)
            glVertex3f(vertices[next_i][0] - building_width/2, vertices[next_i][1] - building_width/2, 0)
            glVertex3f(vertices[next_i][0] - building_width/2, vertices[next_i][1] - building_width/2, building_height)
            glVertex3f(vertices[i][0] - building_width/2, vertices[i][1] - building_width/2, building_height)

            # Lado 2
            glVertex3f(vertices[i][0] + building_width/2, vertices[i][1] - building_width/2, 0)
            glVertex3f(vertices[next_i][0] + building_width/2, vertices[next_i][1] - building_width/2, 0)
            glVertex3f(vertices[next_i][0] + building_width/2, vertices[next_i][1] - building_width/2, building_height)
            glVertex3f(vertices[i][0] + building_width/2, vertices[i][1] - building_width/2, building_height)

            # Lado 3
            glVertex3f(vertices[i][0] + building_width/2, vertices[i][1] + building_width/2, 0)
            glVertex3f(vertices[next_i][0] + building_width/2, vertices[next_i][1] + building_width/2, 0)
            glVertex3f(vertices[next_i][0] + building_width/2, vertices[next_i][1] + building_width/2, building_height)
            glVertex3f(vertices[i][0] + building_width/2, vertices[i][1] + building_width/2, building_height)

            # Lado 4
            glVertex3f(vertices[i][0] - building_width/2, vertices[i][1] + building_width/2, 0)
            glVertex3f(vertices[next_i][0] - building_width/2, vertices[next_i][1] + building_width/2, 0)
            glVertex3f(vertices[next_i][0] - building_width/2, vertices[next_i][1] + building_width/2, building_height)
            glVertex3f(vertices[i][0] - building_width/2, vertices[i][1] + building_width/2, building_height)

    glEnd()