from OpenGL.GL import *
from OpenGL.GLUT import *
import glm

coords = ()
janela_largura = 400
janela_altura = 400

def configuracoes_iniciais():
    glClearColor(1, 1, 1, 1)


def desenha():
    glClear(GL_COLOR_BUFFER_BIT)

  

def capturaCoordenada(button, state, x, y):
    global coords

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        novo_ponto = glm.vec2(0)
        novo_ponto.x = 2*x/janela_largura
        novo_ponto.y = 1-2*y/janela_altura
        coords = (novo_ponto.x, novo_ponto.y)

    print("As coordenadas respectivadas dos pontos X e Y é {}".format(coords))

    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(janela_largura, janela_altura)
glutCreateWindow("Projeto EZE")
configuracoes_iniciais()
glutDisplayFunc(desenha)
glutMouseFunc(capturaCoordenada)
glutMainLoop()
