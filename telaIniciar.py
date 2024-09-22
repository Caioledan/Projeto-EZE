import glfw
from OpenGL.GL import *

def init_opengl():
    glClearColor(0.1, 0.1, 0.1, 1.0)

def draw_menu():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Desenha um retângulo como exemplo
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(-0.5, 0.5)
    glEnd()

    # Aqui você pode adicionar mais elementos, como texto

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        print("Iniciando o jogo...")
        # Lógica para iniciar o jogo

def main():
    if not glfw.init():
        print("Falha ao inicializar GLFW")
        return
    
    window = glfw.create_window(800, 600, "Menu do Jogo", None, None)
    if not window:
        print("Falha ao criar a janela")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    init_opengl()
    
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        draw_menu()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
