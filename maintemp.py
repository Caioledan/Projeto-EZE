from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glm
from Carro import *
import numpy as np
from pontosInteresse import *
from pontosInteresse import *

posicao = glm.vec3(0,0,0) #posição do carro
direcao = glm.vec3(0,1,0) #vetor direção no eixo y
lateral = glm.vec3(1,0,0) #vetor lateral no eixo x





trajeto = [glm.vec3(2,2,0),
           glm.vec3(4,2,0),
           glm.vec3(6,2,0),
           glm.vec3(7,3,0),
           glm.vec3(6,5,0),
           glm.vec3(5,6,0),
           glm.vec3(-5,10,0),
           glm.vec3(-50,11,0)] #percurso


carro = Carro(posicao,direcao,lateral)
ponto = pontos()
texId = 0

def desenhapercurso():
    global trajeto
    glLineWidth(5)
    glColor3f(1,0.5,0)
    glBegin(GL_LINE_STRIP)
    for i in trajeto:
        glVertex3f(*i)
    glEnd()
   

def desenhaLinhasXeYeZ():
    glColor3f(1,0,0)
    glBegin(GL_LINES)
    #Desenhnado o eixo X
    glVertex3f(-50,0,0)
    glVertex3f(50,0,0)
    #Desenhando o eixo Y
    glColor3f(0,1,0)
    glVertex3f(0,50,0)
    glVertex3f(0,-50,0)
    #Desenhando o eixo Z
    glColor3f(0,0,1)
    glVertex3f(0,0,50)
    glVertex3f(0,0,-50)

    glEnd()

def inicio():
    global texId
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-5,5,-5,5,-5,100) #Largura da projeção
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(carro.posicao.x,carro.posicao.y-1,1,2,2,0,0,0,1)
    glEnable(GL_TEXTURE_2D)
    texId = ponto.sortearTextura()
    

    glClearColor(0.5,0.5,0.5,0.5)#Cor do fundo
    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade



vertice = 0 #Variável que vai dizer o índice do vertice na lista para o carro andar.
carro.setarPosicaoInicio(*trajeto[vertice]) #Seto o carro com uma posição inicial
carro.calculaProxDirec(trajeto[vertice+1]) #E faço ele ficar em direção ao vértice do trajeto.

#variáveis globais para armazenar a posição da câmera atual da camera e o seu alvo.
posCameraAtual = glm.vec3(0, 0, 5)
suavizacaoCamera = 0.05  #variavel para a suavização

def timer(v):
    global carro,vertice, posCameraAtual,suavizacaoCamera
    #a cada frame é necessário chamar essa função para 'agendar' a sua próxima execução
    glutTimerFunc(int(1000/60), timer, 0)  

    #Atualizando a posição da câmera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    posCameraDesejada = carro.posicao - carro.direcao + glm.vec3(0, 0, 0.75) #posição desejada da câmera, atrás do vetor direção carro.
    posCameraAtual = glm.lerp(posCameraAtual, posCameraDesejada, suavizacaoCamera)#faz uma transição suave entre a posição de camera atual com a que deseja chegar.

    gluLookAt(posCameraAtual.x, posCameraAtual.y, posCameraAtual.z,  #posição suavizada da câmera
              *carro.posicao,  # Ponto suavizado para o qual a câmera olha
              0, 0, 1)  # Vetor 'up' (definindo o eixo Z como "para cima")
    

    if vertice < len(trajeto):
        if(glm.distance(carro.posicao,trajeto[vertice]) < 0.1): #Ao chegar no vértice, recalcula para o outro.
            if(trajeto[vertice] != trajeto[len(trajeto)-1]): #O carro só vai andar até ele chegar no último vértice
                vertice = vertice + 1  #Incrementa para pegar o proximo vertice do trajeto
                carro.calculaProxDirec(trajeto[vertice]) #Calculo a direção dele
                carro.andar() #Coloco o carro para andar
                carro.calcMatriz() #E calculo a matriz de transformação.
            else:
                pass #Quando estiver no último vértice, o carro para.
        else:#Se não estiver perto do outro vértice, vai andando até chegar nele.
            carro.andar() 
            carro.calcMatriz()

    glutPostRedisplay()



def desenhar():
    global texId
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o conteÃºdo do frame buffer aplicando a cor usada em glClearColor em toda a imagem
    
    desenhaLinhasXeYeZ()

    glPushMatrix()
    glMultMatrixf(np.asarray(glm.transpose(M))) # função que aplica uma matriz qualquer no objeto
    carro.desenhar()
    glPopMatrix()

    desenhapercurso()


    glBindTexture(GL_TEXTURE_2D, texId)  # vinculando a textura
    glPushMatrix()
    glTranslatef(trajeto[3].x,trajeto[3].y,trajeto[3].z+1)  # translação do círculo
    ponto.desenhar()  # desenhando o círculo
    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)  # desassociar a textura
  
    glutSwapBuffers()

glutInit()
glutInitWindowSize(500,500)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowPosition(0,0)
glutCreateWindow("Prototipo de automovel")
inicio()
glutTimerFunc(int(1000/60), timer, 0) # função 'timer' será chamada daqui a 1000/FPS milissegundos
glutDisplayFunc(desenhar)
glutMainLoop()