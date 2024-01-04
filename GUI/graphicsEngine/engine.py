import moderngl as mgl
import sys
import glm
import pygame as pg
from .models import *
from .camera import *

class graphicsEngine:
    def __init__(self,graphicsSettings, winSize=(1600,900)):
        pg.init()
        self.winSize=winSize

        #tell pg what openGL to use
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        #set pg to display using doublebuffer
        pg.display.set_mode(self.winSize,flags=pg.OPENGL | pg.DOUBLEBUF)

        self.ctx=mgl.create_context()
        #self.ctx.front_face='cw'
        #self.ctx.enable(flags=mgl.DEPTH_TEST) #| mgl.CULL_FACE)

        self.clock=pg.time.Clock()


        cameraParams=graphicsSettings["cameraFrustumParams"]
        speedParams=[graphicsSettings["cameraSpeed"], graphicsSettings["cameraSensitivity"]]
        self.camera=camera([50,0,100],cameraParams, self.winSize, speedParams)
        #scene
        self.scene=sphere(1.0,[0.0,0.0,0.0],"Sphere1",self)

    def updatePosition(self, position):
        self.scene.update(position)

    def render(self):
        #clears the framebuffer and then swaps buffers
        self.ctx.clear(color=(.08,.16,.18))
        self.scene.render()
        pg.display.flip()