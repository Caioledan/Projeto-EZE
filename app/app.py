from OpenGL.GL import *
from OpenGL.GLUT import *

class Main: 
    def __init__(self):
        self.zoom_factor = 30.0
        self.mouse_x = 0
        self.mouse_y = 0
        self.window_width = 1024
        self.window_height = 1024


    def loadData(self): 
        l = list()

        with open("./data/data_tratada.txt") as f:
            for i in f:
                line = i.strip()
                separator = line.split(",")
                l.append(tuple(separator))

        return l


    def configuracoesIniciais(self):
        glClearColor(0.1529, 0.1765, 0.2235, 1.0)    # Qual a cor o framebuffer será limpo
        glLineWidth(4)     # Define a largura da linha no opengl 



    def desenha(self):   
        pontos = self.loadData()

        glClear(GL_COLOR_BUFFER_BIT)    # Limpar o framebuffer
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Fazer o movimento da tela em relação ao centro da janela
        mouse_offset_x = self.mouse_x - self.window_width / 2
        mouse_offset_y = self.mouse_y - self.window_height / 2

        # Normaliza o vetor de deslocamento para ajustar o zoom
        norm = (mouse_offset_x ** 2 + mouse_offset_y ** 2) ** 0.5
        if norm != 0:
            mouse_offset_x /= norm
            mouse_offset_y /= norm

        # Define o fator de zoom baseado na posição do mouse
        zoom_factor = 2.0  # Valor arbitrário, ajuste conforme necessário
        zoomed_mouse_offset_x = mouse_offset_x * zoom_factor
        zoomed_mouse_offset_y = mouse_offset_y * zoom_factor

        # Alterar o zoom da tela do opengl
        # Ajustar o tamanho da janela de visualização com base no fator de zoom
        window_width_zoomed = self.window_width / self.zoom_factor
        window_height_zoomed = self.window_height / self.zoom_factor
        glOrtho(-window_width_zoomed/2, window_width_zoomed/2, -window_height_zoomed/2, window_height_zoomed/2, -10, 10)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glBegin(GL_LINES)
        glColor3f(62/255.0, 86/255.0, 110/255.0)
        
        for ponto in pontos:
            x, y = ponto

            # Aplica o zoom para a direção do mouse
            x_zoomed = float(x) + zoomed_mouse_offset_x
            y_zoomed = float(y) + zoomed_mouse_offset_y
            glVertex3f(x_zoomed, y_zoomed, 0)
    
        glEnd()
        glFlush()


    def mouse_motion(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        glutPostRedisplay()


    def mouse_wheel(self, wheel, direction, x, y):
        # Atualiza o fator de zoom com base na direção da roda do mouse
        if direction > 0:
            self.zoom_factor *= 1.1  # Aumenta o zoom
        else:
            self.zoom_factor /= 1.1  # Diminui o zoom
        
        glutPostRedisplay()


    def init(self):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(1024, 1024)
        glutCreateWindow("Projeto EZE")
        self.configuracoesIniciais()
        glutDisplayFunc(self.desenha)
        glutMotionFunc(self.mouse_motion)
        glutMouseWheelFunc(self.mouse_wheel)
        glOrtho(-26, 26, -32, 32, -10, 10)
        glutMainLoop()


app = Main()

if __name__ == "__main__":
    app.init()
