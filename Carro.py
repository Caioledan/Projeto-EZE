from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

v1 = [-1,0,0]
v2 = [1,0,0]
v3 = [0,2,0]
v4 = [-1,0,0.50]
v5 = [1,0,0.50]
v6 = [0,2,0.50]

vertices = [v1,v2,v3,v4,v5,v6]

class Carro:
    def __init__(self):
        global v1,v2,v3,v4,v5,v6

    def desenhar(self):
        global v1,v2,v3,v4,v5,v6
        #Desenhando ao redor do triângulo..
        glColor3f(0,0.5,0.8)
        glBegin(GL_TRIANGLES)
        for i in vertices:
            glVertex3fv(i)
        glEnd()

        #Desenhando as laterais do polígono.
        glColor3f(0,0,0.8)
        glBegin(GL_QUADS)

        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v5)
        glVertex3fv(v4)

        glVertex3fv(v1)
        glVertex3fv(v3)
        glVertex3fv(v6)
        glVertex3fv(v4)

        glVertex3fv(v2)
        glVertex3fv(v3)
        glVertex3fv(v6)
        glVertex3fv(v5)
        glEnd()

        #Desenhando as linhas das laterais por estilo.
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )#função pra desenhar só as bordas
        glColor3f(1,1,1)

        glBegin(GL_TRIANGLES)
        for i in vertices:
            glVertex3fv(i)
        glEnd()

        glBegin(GL_QUADS)
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v5)
        glVertex3fv(v4)

        glVertex3fv(v1)
        glVertex3fv(v3)
        glVertex3fv(v6)
        glVertex3fv(v4)

        glVertex3fv(v2)
        glVertex3fv(v3)
        glVertex3fv(v6)
        glVertex3fv(v5)

        glEnd()
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        glFlush()
