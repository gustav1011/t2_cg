import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Objeto3D import Objeto3D

# Controle da animação
is_playing = False
is_reversing = False
movement_phase = 0
frame = 0
max_frames = 600
particles = []
velocities = []
frame_positions = []
camera_pos = [0.0, 100.0, 300.0]  # Posição inicial da câmera
camera_target = [0.0, 0.0, 0.0]   # Ponto que a câmera está olhando
camera_up = [0.0, 1.0, 0.0]       # Vetor "para cima" da câmera
camera_speed = 10.0               # Velocidade de movimento



def init():
    glClearColor(0.1, 0.1, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    DefineLuz()


def resize(w, h):
    if h == 0:
        h = 1
    aspect = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)


def DesenhaChao():
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-500, -50, -500)
    glVertex3f(-500, -50, 500)
    glVertex3f(500, -50, 500)
    glVertex3f(500, -50, -500)
    glEnd()


def DefineLuz():
    luz_ambiente = [0.4, 0.4, 0.4, 1.0]
    luz_difusa = [0.7, 0.7, 0.7, 1.0]
    luz_especular = [1.0, 1.0, 1.0, 1.0]
    posicao_luz = [100.0, 200.0, 100.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)


def update_particles():
    global particles, velocities
    gravity = -0.75
    floor_y = -50
    for i, p in enumerate(particles):
        velocities[i][1] += gravity
        p[1] += velocities[i][1]
        if p[1] < floor_y:
            p[1] = floor_y
            velocities[i][1] *= -0.5

    if len(frame_positions) <= frame:
        frame_positions.append([p[:] for p in particles])
    else:
        frame_positions[frame] = [p[:] for p in particles]


def apply_frame():
    global frame, particles, frame_positions
    if 0 <= frame < len(frame_positions):
        particles = [p[:] for p in frame_positions[frame]]


def display():
    global particles
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(*camera_pos, *camera_target, *camera_up)

    DesenhaChao()

    glPointSize(3)
    glColor3f(1.0, 0.8, 0.6)
    glBegin(GL_POINTS)
    for p in particles:
        glVertex3f(p[0], p[1], p[2])
    glEnd()

    glutSwapBuffers()

def creative_movements():
    global particles, frame

    # Movimento 1: Espiral ascendente
    if 300 <= frame < 420:
        for i, p in enumerate(particles):
            radius = math.sqrt(p[0]**2 + p[2]**2)
            theta = math.atan2(p[2], p[0]) + 0.05
            p[0] = radius * math.cos(theta)
            p[2] = radius * math.sin(theta)
            p[1] += 0.5  # sobe mais rápido

    # Movimento 2: Explosão radial com pulsação
    elif 420 <= frame < 600:
        t = frame - 420
        for i, p in enumerate(particles):
            direction = [p[0], p[1], p[2]]
            length = math.sqrt(sum(x**2 for x in direction)) + 0.001
            norm = [x / length for x in direction]
            pulse = 1 + 0.2 * math.sin(t * 0.5)
            for j in range(3):
                p[j] += norm[j] * 0.7 * pulse


def timer(value):
    global frame, max_frames

    if is_playing:
        if is_reversing:
            frame -= 1
            if frame < 0:
                frame = max_frames - 1
        else:
            if frame < 300:
                update_particles()
            else:
                creative_movements()

            frame += 1
            if frame >= max_frames:
                frame = 0

        apply_frame()
        glutPostRedisplay()

    glutTimerFunc(33, timer, 0)



def rotate_particles_y(angle=0.1):
    global particles
    for p in particles:
        x = p[0]
        z = p[2]
        new_x = x * math.cos(angle) - z * math.sin(angle)
        new_z = x * math.sin(angle) + z * math.cos(angle)
        p[0] = new_x
        p[2] = new_z


def rotate_particles_x(angle=0.1):
    global particles
    for p in particles:
        y = p[1]
        z = p[2]
        new_y = y * math.cos(angle) - z * math.sin(angle)
        new_z = y * math.sin(angle) + z * math.cos(angle)
        p[1] = new_y
        p[2] = new_z


def keyboard(key, x, y):
    global is_playing, frame, is_reversing
    try:
        key = key.decode("utf-8")
    except:
        return

    print(f"Tecla pressionada: {key}")

    if key == 'p':
        is_playing = not is_playing

    elif key == 'r':
        frame = max(0, frame - 1)
        is_playing = False
        apply_frame()

    elif key == 'f':
        frame = min(max_frames - 1, frame + 1)
        is_playing = False
        apply_frame()

    elif key == 'v':
        is_reversing = not is_reversing
        is_playing = True

    elif key == 'g':
        rotate_particles_y()

    elif key == 'h':
        rotate_particles_x()

    elif key == 'w':
        forward = [camera_target[i] - camera_pos[i] for i in range(3)]
        length = math.sqrt(sum(x**2 for x in forward))
        forward = [x / length for x in forward]
        for i in range(3):
            camera_pos[i] += forward[i] * camera_speed
            camera_target[i] += forward[i] * camera_speed

    elif key == 's':
        forward = [camera_target[i] - camera_pos[i] for i in range(3)]
        length = math.sqrt(sum(x**2 for x in forward))
        forward = [x / length for x in forward]
        for i in range(3):
            camera_pos[i] -= forward[i] * camera_speed
            camera_target[i] -= forward[i] * camera_speed

    elif key == 'a':
        forward = [camera_target[i] - camera_pos[i] for i in range(3)]
        right = [
            forward[2] * camera_up[1] - forward[1] * camera_up[2],
            forward[0] * camera_up[2] - forward[2] * camera_up[0],
            forward[1] * camera_up[0] - forward[0] * camera_up[1]
        ]
        length = math.sqrt(sum(x**2 for x in right))
        right = [x / length for x in right]
        for i in range(3):
            camera_pos[i] -= right[i] * camera_speed
            camera_target[i] -= right[i] * camera_speed

    elif key == 'd':
        forward = [camera_target[i] - camera_pos[i] for i in range(3)]
        right = [
            forward[2] * camera_up[1] - forward[1] * camera_up[2],
            forward[0] * camera_up[2] - forward[2] * camera_up[0],
            forward[1] * camera_up[0] - forward[0] * camera_up[1]
        ]
        length = math.sqrt(sum(x**2 for x in right))
        right = [x / length for x in right]
        for i in range(3):
            camera_pos[i] += right[i] * camera_speed
            camera_target[i] += right[i] * camera_speed


    glutPostRedisplay()


def load_particles_from_obj(path):
    global particles, velocities
    obj = Objeto3D()
    obj.LoadFile(path)
    particles = [[v.x * 30, v.y * 30, v.z * 30] for v in obj.vertices]
    velocities = [[0.0, 0.0, 0.0] for _ in particles]


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"Animacao de Particulas - Cabeca Caindo")

    init()
    load_particles_from_obj("Human_Head.obj")

    global frame_positions
    frame_positions.append([p[:] for p in particles])

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyboard)
    print("Teclas: p = play/pause, r = rewind, f = forward, v = reverso, g/h = rotacao")
    glutTimerFunc(0, timer, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
        