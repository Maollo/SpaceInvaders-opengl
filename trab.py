from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np

ATIRAR = 0
CRIAR_INIMIGO = 1

class nave:
    px = 0.0
    vx = 1.0
    pz = 17.0

    def atualizaNavi(self):
        self.px += self.vx


class inimigos:
    vx  = 0.0
    vz = 0.1
    raio = 1.0

    def __init__(self,x,z):
        self.px  = x
        self.pz = z

    def atualizaInimigo(self):
        self.pz += self.vz
        self.px += self.vx

        #if( not (abs(self.px)<=4.0)):
        #    self.vx *= -1 

        if( not (abs(self.pz)<=35.0)):
            self.pz = 0.0


class tiros:
    pz = 0.0
    px = 0.0 
    vz = 0.1
    raio = 1.0
    def __init__(self, nave):
        self.pz = nave.pz - 1.0
        self.px = nave.px

    def atualizaTiro(self):
        self.pz -= self.vz

    def contatoComInimigo(self,inim):
        #print(f"distancia = {np.sqrt( (np.square(self.pz - inim.pz))  + (np.square(self.px - inim.px)) )}")
        if (self.raio + inim.raio >=  np.sqrt( (np.square(self.pz - inim.pz))  + (np.square(self.px - inim.px)) )  ):
            print("colidiu!!!!!")
            return 1
        else:
            return 0

    
anave = nave()
list_tiros = []
list_inimigos = []

def display():
    global ATIRAR , CRIAR_INIMIGO
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    
    #Corpo do navi

    glTranslatef(0.0, 0.0, anave.pz)
    glTranslatef(anave.px, 0.0, 0.0)
    glColor3f(0.0, 0.3, 0.3)
    visualization.draw(navi)
    glPopMatrix()

# inimigos
    if (CRIAR_INIMIGO):
        list_inimigos.append(inimigos(10.0,-15.0))
        list_inimigos.append(inimigos(0.0,-15.0))
        list_inimigos.append(inimigos(-10.0,-15.0))
        CRIAR_INIMIGO = 0

    
    for inim in list_inimigos:
        inim.atualizaInimigo()
        if inim.pz >= 5.0:
            inim.pz = -15.0

        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)
        glTranslatef(inim.px, 0.0, inim.pz)
        visualization.draw(inimigo)
        glPopMatrix()
         
    
    #tratar os tiros
    if ATIRAR == 1:
        list_tiros.append(tiros(anave))
        ATIRAR += 1
        

    for t in list_tiros:    
        t.atualizaTiro()
        for i in list_inimigos:
            if (t.contatoComInimigo(i)):
                list_inimigos.pop(list_inimigos.index(i))
                list_tiros.pop(list_tiros.index(t))
                print("removidos")
                
        if t.pz < 0.0:
            list_tiros.pop(list_tiros.index(t))
        else:
            glPushMatrix()
            glColor3f(0.0, 0.0, 0.0)
            glTranslatef(t.px, 0.0,t.pz)
            glRotatef(90,0.0,1.0,0.0)
            visualization.draw(tiro)
            glPopMatrix()


    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()

  
  


    glutSwapBuffers()
    
def Keys(key, x, y):

    if(key == GLUT_KEY_LEFT ): 
        anave.px -= anave.vx 
    elif(key == GLUT_KEY_RIGHT ): 
        anave.px += anave.vx 


def Keys_letras(key, x ,y):

    global ATIRAR

    if(key == b' ' ): #Espaço
        ATIRAR += 1      
       

def animacao(value):

    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
    
def maisInimigos(value):
    global CRIAR_INIMIGO
    CRIAR_INIMIGO = 1
    glutTimerFunc(15000,maisInimigos,1)


    
    
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 7.0, 25.0, 0.0, 1.0, -15.0,0.0, 0.3, 0.0)

  

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.1, 0.0, 0.5 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0] )
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.6, 0.6, 0.6, 1.0] )
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0] )
    glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] );
    glLightfv( GL_LIGHT0, GL_POSITION, [2.0, 2.0, 1.0, 0.0])
    glEnable( GL_LIGHT0 )
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1280, 720)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Cubo")
init()
inimigo = pywavefront.Wavefront("inimigo2.obj")
navi = pywavefront.Wavefront("navi2.obj")
tiro = pywavefront.Wavefront("tiro.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutTimerFunc(15000,maisInimigos,1)
glutSpecialFunc(Keys)
glutKeyboardFunc(Keys_letras)
glutMainLoop()
