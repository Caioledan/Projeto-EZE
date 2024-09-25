from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glm
import numpy as np
from utils.OSMHandlerConvert import OSMHandler, latlon_to_opengl
from utils.desenhos import draw_buildings_as_cubes, draw_map_with_depth, draw_path, draw_pre_path
from utils.PathFinder import PathFinder
from utils.randomic import Randomic
from utils.Carro import *
from utils.pontosInteresse import pontos
from map_data import paths



#variáveis globais para armazenar a posição da câmera atual da camera e o seu alvo.
posCameraAtual = glm.vec3(0, 0, 0.02)
suavizacaoCamera = 0.1  #variavel para a suavização
vertice = 0
trajeto = []


posicao = glm.vec3(0,0,0) #posição do self.carro
direcao = glm.vec3(0,1,0) #vetor direção no eixo y
lateral = glm.vec3(1,0,0) #vetor lateral no eixo x

janelaLargura = 1920
janelaAltura = 1080

carro = Carro(posicao, direcao, lateral)

raio = 0.005
lados = 100

# Chamada para a textura
point1 = pontos(raio,lados)
point2 = pontos(raio,lados)
texId1 = 0
texId2 = 0

zoom = 1
class Utils():
    def __init__(self):
        # Variáveis globais
        #constantes
        self.rotation_x = 0
        self.rotation_y = 0
        self.move_x = 0
        self.move_y = 0
        self.move_speed = 0.1
        self.draw_min = False
        self.move = False
        self.nodes = None
        self.bbox = None
        self.path = None
        self.cam = False
        self.pre = False
        self.pre_true = False
        self.original_position = False


    def setup_3d_view(self):
        global zoom
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 800 / 600, 0.02, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, zoom, 0, 0, 0, 0, 1, 0)


    def setup_lighting(self):
        glEnable(GL_LIGHTING)  # Habilita o sistema de iluminação
        glEnable(GL_LIGHT0)    # Habilita uma luz (Luz 0)

        # Posiciona a luz ligeiramente à frente do carro, seguindo sua direção
        light_position = [
            carro.posicao.x + carro.direcao.x * 0.0001,  # Posição da luz à frente do carro na direção X
            carro.posicao.y + carro.direcao.y * 0.0001,  # Posição da luz à frente do carro na direção Y
            carro.posicao.z + 0.02,                   # Mantém a luz um pouco acima da posição do carro
            1.0  # Componente w = 1.0 significa que é uma luz posicional
        ]

        # Definindo a luz como uma luz direcional à frente do carro
        light_direction = [
            carro.direcao.x * 0.1,  # Direção da luz na direção X do carro
            carro.direcao.y * 0.1,  # Direção da luz na direção Y do carro
            -0.1,  # Direcionada ligeiramente para baixo
        ]

        # Configura os parâmetros de iluminação: ambiente, difusa, e especular
        light_ambient = [0.8, 0.8, 0.8, 1.0]   # Componente ambiente da luz
        light_diffuse = [1.0, 1.0, 1.0, 1.0]   # Componente difusa
        light_specular = [1.0, 1.0, 1.0, 1.0]  # Componente especular

        # Aplicar os parâmetros de iluminação ao GL_LIGHT0
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)  # Define a posição da luz
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction)  # Define a direção da luz
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 30.0)  # Ângulo do feixe de luz (em graus)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

        # Configura o modelo de iluminação (luz ambiente global)
        global_ambient = [0.9, 0.9, 0.9, 1.0]
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

        # Habilita o uso de materiais
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Especular
        glMateriali(GL_FRONT, GL_SHININESS, 64)  # Brilho especular

    def redimensionaJanela(self, w, h):
        global janelaLargura, janelaAltura
        janelaLargura = w
        janelaAltura = h
        
        # Evita divisão por zero se a altura for muito pequena
        if h == 0:
            h = 1
        
        # Ajusta a viewport ao novo tamanho da janela
        glViewport(0, 0, w, h)
        
        # Ajusta a projeção de perspectiva
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = w / h
        gluPerspective(45.0, aspect_ratio, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def read_osm(self, filename):
        handler = OSMHandler()
        handler.apply_file(filename)
        lats = [coord[0] for coord in handler.nodes.values()]
        lons = [coord[1] for coord in handler.nodes.values()]
        bbox = (min(lats), min(lons), max(lats), max(lons))
        return handler.nodes, handler.ways, handler.buildings, handler.graph, bbox

    def create_path(self, nodes, path, bbox, trajeto):
        for i in range(len(path) - 1):
            node1 = nodes[path[i]]
            node2 = nodes[path[i + 1]]
            x1, y1, z1 = latlon_to_opengl(node1[0], node1[1], bbox, z=0)
            x2, y2, z2 = latlon_to_opengl(node2[0], node2[1], bbox, z=0)
            trajeto.append(glm.vec3(x1, y1, z1))
            trajeto.append(glm.vec3(x2, y2, z2))


    def keyboard_callback(self, key, x, y):
        global trajeto, zoom
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
            zoom -= 0.1
        elif key == b'-':
            zoom += 0.1
        elif key == b' ':
            if not self.path:  # Só cria o caminho se ainda não existir
                random = Randomic()
                pathfinder = PathFinder(self.graph, self.nodes)
                n1, n2 = random.randomizer()
                start_node = int(n1)
                end_node = int(n2)
                self.path = pathfinder.find_shortest_path(start_node, end_node)
                self.create_path(self.nodes, self.path, self.bbox, trajeto)
                carro.setarPosicaoInicio(*trajeto[vertice])
                carro.calculaProxDirec(trajeto[vertice+1])
            self.draw_min = not self.draw_min  # Alterna entre desenhar ou não o caminho
        elif key == b'1':
            if not self.pre_true:
                trajeto = paths.routes["route1"]
                carro.setarPosicaoInicio(*trajeto[vertice])
                carro.calculaProxDirec(trajeto[vertice+1])
                self.pre_true = True
            self.pre = not self.pre
        elif key == b'2':
            if not self.pre_true:
                trajeto = paths.routes["route2"]
                carro.setarPosicaoInicio(*trajeto[vertice])
                carro.calculaProxDirec(trajeto[vertice+1])
                self.pre_true = True
            self.pre = not self.pre
        elif key == b'3':
            if not self.pre_true:
                trajeto = paths.routes["route3"]
                carro.setarPosicaoInicio(*trajeto[vertice])
                carro.calculaProxDirec(trajeto[vertice+1])
                self.pre_true = True
            self.pre = not self.pre
        elif key == b'4':
            if not self.pre_true:
                trajeto = paths.routes["route4"]
                carro.setarPosicaoInicio(*trajeto[vertice])
                carro.calculaProxDirec(trajeto[vertice+1])
                self.pre_true = True
            self.pre = not self.pre
        elif key == b'\r':
            self.move = not self.move
        elif key == b'c':
            self.cam = not self.cam
        elif key == b'r':
            self.original_position = not self.original_position


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
        global texId1, texId2

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if(self.cam):
            self.setup_lighting()
        
        else:
            self.setup_3d_view()
        
        if(not self.original_position):
            glRotatef(self.rotation_x, 1, 0, 0)
            glRotatef(self.rotation_y, 0, 1, 0)
            glTranslatef(self.move_x, self.move_y, 0)
        else:
            glRotatef(0, 1, 0, 0)
            glRotatef(0, 0, 1, 0)
            glTranslatef(0, 0, 0)

        # Desenha prédios e mapa
        draw_buildings_as_cubes(self.nodes, self.buiding, self.bbox)
        draw_map_with_depth(self.nodes, self.ways, self.bbox)

        # Desenha o caminho se a tecla espaço foi apertada
        if self.draw_min:
            glDisable(GL_DEPTH_TEST)
            draw_path(self.nodes, self.path, self.bbox)
            glEnable(GL_DEPTH_TEST)

        if self.pre:
            glDisable(GL_DEPTH_TEST)
            draw_pre_path(trajeto)
            glEnable(GL_DEPTH_TEST)

        # Desenha o carro apenas se o trajeto foi traçado
        if len(trajeto) > 1:  # Verifica se o trajeto foi gerado
            glLineWidth(0.01)
            glPushMatrix()
            glMultMatrixf(np.asarray(glm.transpose(M)))  # função que aplica uma matriz qualquer no objeto
            carro.desenhar()
            glPopMatrix()

        # Aplicando as texturas 
        if(len(trajeto)):
            loc = int((len(trajeto)/2.0))

            glBindTexture(GL_TEXTURE_2D, texId1)
            glPushMatrix()
            glTranslatef(trajeto[loc].x,trajeto[loc].y,trajeto[loc].z + 0.02)  # translação do círculo
            point1.desenhar()
            glPopMatrix()
            glBindTexture(GL_TEXTURE_2D, texId2)
            glPushMatrix()
            glTranslate(trajeto[int(loc * 1.5)].x, trajeto[int(loc * 1.5)].y, trajeto[int(loc * 1.5)].z + 0.02)
            point2.desenhar()
            glPopMatrix()
            glBindTexture(GL_TEXTURE_2D, 0)  # desassociar a textura
            
        glutSwapBuffers()


    def timer(self,v):
        global vertice, posCameraAtual, suavizacaoCamera,carro

        #a cada frame é necessário chamar essa função para 'agendar' a sua próxima execução.
        glutTimerFunc(int(1000/60), self.timer, 0)  
        

        if self.cam: # Se o carro começar a andar, atualiza a câmera para ele.
            #Atualizando a posição da câmera
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            posCameraDesejada = carro.posicao - carro.direcao * 0.1 + glm.vec3(0, 0, 0.05) #posição desejada da câmera, atrás do vetor direção self.carro.
            posCameraAtual = glm.lerp(posCameraAtual, posCameraDesejada, suavizacaoCamera)#faz uma transição suave entre a posição de camera        atual com a que deseja chegar.
            
            gluLookAt(posCameraAtual.x, posCameraAtual.y, posCameraAtual.z,  #posição suavizada da câmera
                        *carro.posicao,  # Ponto suavizado para o qual a câmera olha
                        0, 0, 1)  # Vetor 'up' (definindo o eixo Z como "para cima")
        

        if vertice < len(trajeto):
            if(glm.distance(carro.posicao,trajeto[vertice]) < 0.004): #Ao chegar no vértice, recalcula para o outro.
                if(trajeto[vertice] != trajeto[len(trajeto)-1]): #O self.carro só vai andar até ele chegar no último vértice
                    vertice = vertice + 1  #Incrementa para pegar o proximo vertice do trajeto
                    if self.move:
                        carro.calculaProxDirec(trajeto[vertice]) #Calculo a direção dele
                        carro.andar() #Coloco o self.carro para andar
                        carro.calcMatriz() #E calculo a matriz de transformação.
                else:
                    pass #Quando estiver no último vértice, o self.carro para.
            else:#Se não estiver perto do outro vértice, vai andando até chegar nele
                if self.move:
                    carro.andar() #Coloco o self.carro para andar
                    carro.calcMatriz() #E calculo a matriz de transformação.

        if len(trajeto) > 0:
            glPushMatrix()
            loc = int((len(trajeto)/2.0))
            if glm.distance(carro.posicao, trajeto[loc]) < 0.04:  # Verifica se o carro está próximo ao ponto
                point1.pulsar()
            glPopMatrix()
            if glm.distance(carro.posicao, trajeto[int(loc *1.5)]) < 0.04:
                point2.pulsar()

        glutPostRedisplay()


    def main(self):
        global trajeto, texId1, texId2, janelaLargura, janelaAltura
        # Inicializa GLUT
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(1080, 920)
        glutCreateWindow(b"PROJETO EZE")
        glClearColor(39.0 / 255.0, 45.0 / 255.0, 57.0 / 255.0, 1.0)
        #self.setup_3d_view()

        glEnable(GL_TEXTURE_2D)
        texId1 = point1.sortearTextura()
        texId2 = point2.sortearTextura()
        while(True):
            texId2 = point2.sortearTextura()
            if texId1 != texId2:
                break

        # Configuração do mapa
        filename = "data/map.osm"
        self.nodes, self.ways, self.buiding, self.graph, self.bbox = self.read_osm(filename)
        
        # Configurações do GLUT
        glutTimerFunc(int(1000/60), self.timer, 0)  
        glutDisplayFunc(self.display_callback)
        glutIdleFunc(self.display_callback)
        glutKeyboardFunc(self.keyboard_callback)
        glutSpecialFunc(self.special_callback)
        glutReshapeFunc(self.redimensionaJanela)

        # Loop principal
        glutMainLoop()
