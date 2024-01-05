import moderngl as mgl
import sys
import glm
import pygame as pg
from .models import *
from .camera import *

class graphicsEngine:
    def __init__(self,graphicsSettings,names, currentState, winSize=(1600,900)):
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
        self.camera=camera([50,.1,1000],cameraParams, self.winSize, speedParams)
        #scene
        self.scene={}
        self.createScene(names,currentState)

    def createScene(self,names, currentState):
        for name in names:
            self.scene[name]=sphere(currentState[names[name]][-1],currentState[names[name]][0:3],self)

    def updatePositions(self, positionNames, positionVals):
        for obj in positionNames:
            self.scene[obj].update(positionVals[positionNames[obj]][0:3])

    def addRegularPlanet(self, position, radius, name):
        self.scene[name]=sphere(radius, position, self)

    def render(self):
        #clears the framebuffer and then swaps buffers
        self.ctx.clear(color=(.08,.16,.18))
        for obj in self.scene:
            self.scene[obj].render()
            if len(self.scene)>1:
                print("")
        pg.display.flip()