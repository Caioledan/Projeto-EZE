from OpenGL.GL import *
from PIL import Image  
from math import pi,cos,sin
from random import randint

#caminhos para as texturas
textura1 = "utils/textures/acidente.png"
textura2 = "utils/textures/radar.png"
textura3 = "utils/textures/policia.png"
textura4 = "utils/textures/buraco.png"


class pontos:
    def __init__(self,raio,lados):
        self.raio = raio #raio em que o circulo da figura será desenhado.
        self.lados = lados #a qtd de lados da figura
        self.angulo = 0
        self.desloc = 0
        self.expandindo = True #variável para ajudar no pulsar




    # Função responsável por carregar uma textura a partir do nome do arquivo
    def carregaTextura(self,filename):
        # carregamento da textura feita pelo módulo PIL
        img = Image.open(filename)                  # abrindo o arquivo da textura
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # espelhando verticalmente a textura (normalmente, a coordenada y das imagens cresce de cima para baixo)
        imgData = img.convert("RGBA").tobytes()     # convertendo a imagem carregada em bytes que serão lidos pelo OpenGL

        # criando o objeto textura dentro da máquina OpenGL
        texId = glGenTextures(1) # criando um objeto textura
        glBindTexture(GL_TEXTURE_2D, texId) # tornando o objeto textura recém criado ativo
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)# suavização quando um texel ocupa vários pixels
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)# suavização quanto vários texels ocupam um único pixel
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)                                              # definindo que a cor da textura substituirá a cor do polígono

        glTexImage2D(GL_TEXTURE_2D, 
                    0, 
                    GL_RGBA,  
                    img.width, 
                    img.height, 
                    0, 
                    GL_RGBA, 
                    GL_UNSIGNED_BYTE, 
                    imgData)  # enviando os dados lidos pelo módulo PIL para a OpenGL
        glBindTexture(GL_TEXTURE_2D, 0) # tornando o objeto textura inativo por enquanto
        return texId #identificador da textura recém-criada

    def pulsar(self):
        if self.expandindo:#expandindo foi criado para saber a hora de aumentar o raio do circulo ou diminuir.
            self.raio += 0.001  #se for true, o raio aumenta a cada desenho.
            if self.raio >= 0.008:  #limite superior do raio
                self.expandindo = False  #depois que chegar no limite, vira false para começar a decrementar
        else:  #se o ponto está em fase de contração
            self.raio -= 0.001  #diminui o raio a cada frame
            if self.raio <= 0.005:  #se passar do valor minimo do raio, coloco true para aumentar de novo.
                self.expandindo = True

    def sortearTextura(self): #Função para sortear as texturas aleatoriamente pelo mapa.
        numero = randint(1,4)
        if numero == 1: return self.carregaTextura(textura1)
        if numero == 2: return self.carregaTextura(textura2)
        if numero == 3: return self.carregaTextura(textura3)
        if numero == 4: return self.carregaTextura(textura4)

    

    def desenhar(self):
        glPushMatrix()

        self.angulo += 5 # Fator que definirá a velocidade de rotação
        self.desloc = 0.003 * sin(self.angulo * pi/180) # Usando o fator 0.003 multiplicando a função seno, o movimento vertical se torna suave no eixo z
        glTranslate(0,0,self.desloc) # Função que faz o ícone ter um movimento suave para cima e para baixo

        glRotate(self.angulo, 0, 0, 1) # Função que faz o ícone rotacionar em torno de si mesmo, no eixo z

        glBegin(GL_TRIANGLE_FAN)
        glTexCoord2f(0.5, 0.5)  #Começo colocando o meio da coordenada de textura da imagem no meio da figura do circulo.
        glVertex3f(0,0, 0)  
        for i in range(self.lados + 1):
            angle = 2.0 * pi * i /self.lados
            x = self.raio * cos(angle)
            z = self.raio * sin(angle)
            glTexCoord2f(0.5 + (x / (2 * self.raio)), 0.5 + (z / (2 * self.raio))) #Converte a coordenada do circulo para a de textura primeiramente.
            glVertex3f(x, 0,z)
        glEnd()
        glPopMatrix()

