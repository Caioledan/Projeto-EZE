from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2,2,-2,2,-2,2) #Largura da projeção
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0.5,0.5,0.5,0,0,0,0,0,1)

    glClearColor(0.5,0.5,0.5,0.5)#Cor do fundo
    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade

def desenhar():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o conteÃºdo do frame buffer aplicando a cor usada em glClearColor em toda a imagem
    
    desenhaLinhasXeYeZ()

    #Desenhando ao redor do triângulo..
    glColor3f(0,0.5,0.8)
    glBegin(GL_TRIANGLES)

    glVertex3f(-0.5,0,0)
    glVertex3f(0.5,0,0)
    glVertex3f(0,1,0)

    glVertex3f(-0.5,0,0.25)
    glVertex3f(0.5,0,0.25)
    glVertex3f(0,1,0.25)

    glEnd()

    #Desenhando as laterais do polígono.
    glColor3f(0,0,0.8)
    glBegin(GL_QUADS)

    glVertex3f(0.5,0,0)
    glVertex3f(0.5,0,0.24)
    glVertex3f(0,1,0.24)
    glVertex3f(0,1,0)

    glVertex3f(0.5,0,0)
    glVertex3f(-0.5,0,0)
    glVertex3f(-0.5,0,0.24)
    glVertex3f(0.5,0,0.24)

    glVertex3f(-0.5,0,0)
    glVertex3f(-0.5,0,0.24)
    glVertex3f(0,1,0.24)
    glVertex3f(0,1,0)

    glEnd()


    #Desenhando as linhas das laterais por estilo.
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )#função pra desenhar só as bordas
    glColor3f(1,1,1)

    glBegin(GL_TRIANGLES)
    glVertex3f(-0.5,0,0)
    glVertex3f(0.5,0,0)
    glVertex3f(0,1,0)

    glVertex3f(-0.5,0,0.25)
    glVertex3f(0.5,0,0.25)
    glVertex3f(0,1,0.25)
    glEnd()

    glBegin(GL_QUADS)
    glVertex3f(0.5,0,0)
    glVertex3f(0.5,0,0.24)
    glVertex3f(0,1,0.24)
    glVertex3f(0,1,0)

    glVertex3f(0.5,0,0)
    glVertex3f(-0.5,0,0)
    glVertex3f(-0.5,0,0.24)
    glVertex3f(0.5,0,0.24)

    glVertex3f(-0.5,0,0)
    glVertex3f(-0.5,0,0.24)
    glVertex3f(0,1,0.24)
    glVertex3f(0,1,0)
    glEnd()
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glFlush()

   

glutInit()
glutInitWindowSize(500,500)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowPosition(0,0)
glutCreateWindow("Prototipo de automovel")
inicio()
glutDisplayFunc(desenhar)
glutMainLoop()