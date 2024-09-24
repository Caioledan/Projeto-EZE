from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glm
from utils.OSMHandlerConvert import OSMHandler, latlon_to_opengl
from utils.desenhos import draw_buildings_as_cubes, draw_map_with_depth, draw_path
from utils.PathFinder import PathFinder
from utils.randomicc import Randomic
from utils.Carro import *
import numpy as np



posicao = glm.vec3(0,0,0) #posição do carro
direcao = glm.vec3(0,1,0) #vetor direção no eixo y
lateral = glm.vec3(1,0,0) #vetor lateral no eixo x
carro = Carro(posicao, direcao, lateral)


trajeto = [glm.vec3(2,2,0),
           glm.vec3(4,2,0),
           glm.vec3(6,2,0),
           glm.vec3(7,3,0),
           glm.vec3(6,5,0),
           glm.vec3(5,6,0),
           glm.vec3(-5,10,0),
           glm.vec3(-50,11,0)] #percurso

class Utils():
    def __init__(self):
        # Variáveis globais
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = 1
        self.move_x = 0
        self.move_y = 0
        self.move_speed = 0.1
        #self.posicao = glm.vec3(0, 0, 0)  # Posição do carro
        #self.direcao = glm.vec3(0, 1, 0)  # Vetor direção no eixo y
        #self.lateral = glm.vec3(1, 0, 0)  # Vetor lateral no eixo x
        self.trajeto = []
        self.draw_min = False
        #self.carro = None
        self.nodes = None
        self.bbox = None
        self.path = None

    def setup_3d_view(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 800 / 600, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, self.zoom, 0, 0, 0, 0, 1, 0)
        glEnable(GL_DEPTH_TEST)

    def read_osm(self, filename):
        handler = OSMHandler()
        handler.apply_file(filename)
        lats = [coord[0] for coord in handler.nodes.values()]
        lons = [coord[1] for coord in handler.nodes.values()]
        bbox = (min(lats), min(lons), max(lats), max(lons))
        return handler.nodes, handler.ways, handler.buildings, handler.graph, bbox

    def create_path(self, nodes, path, bbox):
        for i in range(len(path) - 1):
            node1 = nodes[path[i]]
            node2 = nodes[path[i + 1]]
            x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0)
            x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)
            self.trajeto.append(glm.vec3(x1, y1, z1))
            self.trajeto.append(glm.vec3(x2, y2, z2))

    def keyboard_callback(self, key, x, y):
        # Controle de rotação, zoom e movimento
        if key == b'\x1b':  # Tecla ESC para sair
            glutLeaveMainLoop()
        elif key == b'w':
            self.move_y -= self.move_speed
        elif key == b's':
            self.move_y += self.move_speed
        elif key == b'a':
            self.move_x += self.move_speed
        elif key == b'd':
            self.move_x -= self.move_speed
        elif key == b'=':
            self.zoom -= 0.1
        elif key == b'-':
            self.zoom += 0.1
        elif key == b' ':
            self.draw_min = not self.draw_min

    def special_callback(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.rotation_y -= 1
        elif key == GLUT_KEY_RIGHT:
            self.rotation_y += 1
        elif key == GLUT_KEY_UP:
            self.rotation_x -= 1
        elif key == GLUT_KEY_DOWN:
            self.rotation_x += 1

    def display_callback(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_3d_view()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glTranslatef(self.move_x, self.move_y, 0)

        # Desenha prédios e mapa
        draw_buildings_as_cubes(self.nodes, self.buiding, self.bbox)
        draw_map_with_depth(self.nodes, self.ways, self.bbox)

        # Desenha o caminho se a tecla espaço foi apertada
        if self.draw_min:
            glDisable(GL_DEPTH_TEST)
            draw_path(self.nodes, self.path, self.bbox)
            glEnable(GL_DEPTH_TEST)

        # Desenha o carro
        glLineWidth(0.01)
        glPushMatrix()
        glScale(0.005, 0.005, 0.005)
        self.carro.desenhar()
        glPopMatrix()

        glutSwapBuffers()

    global carro
    vertice = 0 #Variável que vai dizer o índice do vertice na lista para o carro andar.
    carro.setarPosicaoInicio(*trajeto[vertice]) #Seto o carro com uma posição inicial
    carro.calculaProxDirec(trajeto[vertice+1]) #E faço ele ficar em direção ao vértice do trajeto.

    #variáveis globais para armazenar a posição da câmera atual da camera e o seu alvo.
    posCameraAtual = glm.vec3(0, 0, 5)
    suavizacaoCamera = 0.05  #variavel para a suavização
    def timer(self, v):
        global carro,vertice, posCameraAtual,suavizacaoCamera
        #a cada frame é necessário chamar essa função para 'agendar' a sua próxima execução
        glutTimerFunc(int(1000/60), self.timer, 0)  

        #Atualizando a posição da câmera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        posCameraDesejada = carro.posicao - carro.direcao + glm.vec3(0, 0, 0.75) #posição desejada da câmera, atrás do vetor direção carro.
        posCameraAtual = glm.lerp(posCameraAtual, posCameraDesejada, suavizacaoCamera)#faz uma transição suave entre a posição de camera atual com a que deseja chegar.

        gluLookAt(posCameraAtual.x, posCameraAtual.y, posCameraAtual.z,  #posição suavizada da câmera
                *carro.posicao,  # Ponto suavizado para o qual a câmera olha
                0, 0, 1)  # Vetor 'up' (definindo o eixo Z como "para cima")
        

        if vertice < len(self.trajeto):
            if(glm.distance(carro.posicao,self.trajeto[vertice]) < 0.1): #Ao chegar no vértice, recalcula para o outro.
                if(self.trajeto[vertice] != self.trajeto[len(self.trajeto)-1]): #O carro só vai andar até ele chegar no último vértice
                    vertice = vertice + 1  #Incrementa para pegar o proximo vertice do trajeto
                    carro.calculaProxDirec(self.trajeto[vertice]) #Calculo a direção dele
                    carro.andar() #Coloco o carro para andar
                    carro.calcMatriz() #E calculo a matriz de transformação.
                else:
                    pass #Quando estiver no último vértice, o carro para.
            else:#Se não estiver perto do outro vértice, vai andando até chegar nele.
                carro.andar() 
                carro.calcMatriz()

        glutPostRedisplay()

    def main(self):
        # Inicializa GLUT
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(1080, 920)
        glutCreateWindow(b"WAZE PROJECT")
        glClearColor(39.0 / 255.0, 45.0 / 255.0, 57.0 / 255.0, 1.0)

        # Configuração do mapa
        filename = "data/map.osm"
        self.nodes, self.ways, self.buiding, self.graph, self.bbox = self.read_osm(filename)
        random = Randomic()
        pathfinder = PathFinder(self.graph, self.nodes)
        n1, n2 = random.randomizer()
        start_node = int(n1)
        end_node = int(n2)
        self.path = pathfinder.find_shortest_path(start_node, end_node)

        # Carro
        #self.carro = Carro(self.posicao, self.direcao, self.lateral)
        self.create_path(self.nodes, self.path, self.bbox)
        #self.carro.setarPosicaoInicio(glm.vec3([ 0.293644, 0.320556, 0 ]))
        print(self.trajeto)
        #self.carro.calculaProxDirec(self.trajeto[1])

        # Configurações do GLUT
        glutDisplayFunc(self.display_callback)
        glutTimerFunc(int(1000/60), self.timer, 0) # função 'timer' será chamada daqui a 1000/FPS milissegundos#]        glutIdleFunc(self.display_callback)
        glutKeyboardFunc(self.keyboard_callback)
        glutSpecialFunc(self.special_callback)

        # Loop principal
        glutMainLoop()