from OpenGL.GL import *
from OpenGL.GLUT import *
from djikstrasetados import Djikstra
from listaadj import ListaAdj


def inicio():
    glClearColor(1,1,1,1)
    glLineWidth(3)

def desenha():
    

    origem = '15.767335190764022,9.588007918107184'
    destino = '12.980939744070279,19.83807640240745'

    arquivo = "data\\datavalorada.txt"
    grafo = ListaAdj.lista_de_adjacencia(arquivo)

    _,anterior = Djikstra.dijkstra(grafo,origem)
    caminho = Djikstra.reconstruct_caminho(anterior,origem,destino)


    glBegin(GL_LINES)
    glColor(133/255.0, 118/255.0, 255/255.0)
    for i in range(len(caminho) - 1):
        anterior = (float(caminho[i][0]),float(caminho[i][1]))
        proximo = (float(caminho[i+1][0]),float(caminho[i+1][1]))
        glVertex(anterior)
        glVertex(proximo)
        print(i)
            



    glEnd()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(1024,1024)
glutCreateWindow("Teste")
inicio()
glutDisplayFunc(desenha)
glOrtho(-26,26,-32,32,-10,10)
glutMainLoop()