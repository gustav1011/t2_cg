from OpenGL.GL import *
from OpenGL.GLUT import *
import sys

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(200, 200)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Teste GLUT")

glutDisplayFunc(display)
glutMainLoop()
