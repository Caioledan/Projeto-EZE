import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from utils.OSMHandlerConvert import OSMHandler
from utils.desenhos import draw_buildings_as_cubes, draw_map_with_depth

zoom = 1  # Zoom inicial (mais perto do que antes)

class Utils(): 
    def __init__(self):

        # Variaveis globais
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = 1  # Zoom inicial (mais perto do que antes)
        self.move_x = 0  # Controle de movimentação no eixo X
        self.move_y = 0  # Controle de movimentação no eixo Y
        self.move_speed = 0.1  # Velocidade de movimento do mapa


    # Função para configurar o modo de perspectiva 3D
    def setup_3d_view(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 800 / 600, 0.1, 100.0)  # Ângulo de visão, proporção e profundidade ajustados
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, zoom, 0, 0, 0, 0, 1, 0)
        glEnable(GL_DEPTH_TEST)

    def read_osm(self, filename):
        handler = OSMHandler()
        handler.apply_file(filename)

        # Encontrar os limites geográficos (bounding box)
        lats = [coord[0] for coord in handler.nodes.values()]
        lons = [coord[1] for coord in handler.nodes.values()]
        bbox = (min(lats), min(lons), max(lats), max(lons))

        return handler.nodes, handler.ways, handler.buildings, bbox

    # Função principal
    def main(self):
        global rotation_x, rotation_y, zoom, move_x, move_y, move_speed
        # Inicializa pygame
        pygame.init()
        display = (1080, 920)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        glClearColor(39.0/255.0, 45.0/255.0, 57.0/255.0, 1.0)  # Cor de fundo azul claro (R, G, B, A)
        # Configura a visualização 3D

        # Lê o arquivo OSM
        filename = "./data/edificios.osm"  # Substitua pelo caminho do arquivo .osm
        nodes, ways, buiding, bbox = self.read_osm(filename)

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

            self.setup_3d_view()

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
                print("Zoom: ", zoom)
                zoom -= 0.1  # Aproxima a câmera
            if keys[K_MINUS]:  # Tecla '-' para diminuir o zoom
                print("Zoom: ", zoom)
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
            
            draw_buildings_as_cubes(nodes, buiding, bbox)
            # Desenha o mapa com profundidade
            draw_map_with_depth(nodes, ways, bbox)


            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()