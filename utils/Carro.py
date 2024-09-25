from OpenGL.GL import *
import glm

#vertices do carro
v1 = [-0.006,-0.006,0]
v2 = [0.006,-0.006,0]
v3 = [0,0.006,0]
v4 = [-0.006,-0.006,0.004]
v5 = [0.006,-0.006,0.004]
v6 = [0,0.006,0.004]
M = glm.mat4(1) #matriz indentidade
velocidade = 0.001 #velocidade do carro para locomoção
trajeto = [v1,v2,v3,v4,v5,v6]#lista de vértices para desenhar os triangulos da figura.

class Carro:
    def __init__(self, posicao, direcao,lateral):
        self.posicao = posicao
        self.direcao = direcao
        self.lateral = lateral
        self.velocidade = velocidade


    def setarPosicaoInicio(self, x,y,z): #função para setar a posição de inicio do carro
        self.posicao.x = x
        self.posicao.y = y
        self.posicao.z = z
        self.calcMatriz() #Calculo a matriz de transformação com esse vetor.


    def calcMatriz(self):
        global M
        M[0] = glm.vec4(self.lateral,0) #1 COLUNA VETOR I, lateral do carro
        M[1] = glm.vec4(self.direcao,0) #2 COLUNA VETOR J, direção do carro
        M[2] = glm.vec4(0,0,1,0) #3 COLUNA VETOR K, topo do carro eixo z
        M[3] = glm.vec4(self.posicao,1) #4 COLUNA POSICAO DO CARRO

    def andar(self):
        self.posicao = self.posicao + velocidade*self.direcao  #altera a posição a cada frame modificando 


    def calculaProxDirec(self,vertice):
        vetorVertCarro = glm.normalize(vertice - self.posicao)#Vetor que sai do carro até o vertice e normalizo ele.

        escalar = glm.dot(self.direcao,vetorVertCarro) #Vai me voltar o cosseno desses angulos
        escalar = glm.clamp(escalar, -1.0, 1.0)  #Uso o clamp pra garantir que o valor esteja no intervalo correto.
        angulo = glm.acos(escalar) #Uso a função para pegar o angulo desse cosseno.

        #Faço produto vetorial entre os dois vetores para saber a direção deles.
        produtoVetorial = glm.cross(self.direcao, vetorVertCarro)
        
        #se a componente Z do vetor resultante produto vetorial for negativa, rotacionar para a direita
        if produtoVetorial.z < 0:
            angulo = -angulo  #rotaciona para a direita (sentido horário)
        
        #aplica a rotação na direção e no vetor lateral com base no ângulo
        self.direcao = glm.rotate(angulo) * self.direcao
        self.lateral = glm.rotate(angulo) * self.lateral

        self.calcMatriz() #calculo a matriz de transformação com os valores
        

    def desenhar(self):
        global v1,v2,v3,v4,v5,v6,trajeto
        #Desenhando ao redor do triângulo..
        glColor3f(0,0.5,0.8)
        glBegin(GL_TRIANGLES)
        for i in trajeto:
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
        for i in trajeto:
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