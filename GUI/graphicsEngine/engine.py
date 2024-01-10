import moderngl as mgl
import sys
import glm
import pygame as pg
from .models import *
from .camera import *

class graphicsEngine:
    def __init__(self,graphicsSettings,names, currentState, textures, winSize=(1300,700)):
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
        self.ctx.enable(flags=mgl.DEPTH_TEST) #| mgl.CULL_FACE)

        self.clock=pg.time.Clock()


        cameraParams=graphicsSettings["cameraFrustumParams"]
        speedParams=[graphicsSettings["cameraSpeed"], graphicsSettings["cameraSensitivity"]]
        self.camera=camera([50,.1,10000],cameraParams, self.winSize, speedParams)
        #scene
        self.scene={}
        self.createScene(names,currentState, textures)

    def createScene(self,names, currentState, textures):
        for name in names:
            self.scene[name]=sphere(currentState[names[name]][-1],currentState[names[name]][0:3],self,textureUnit=names[name], textureName=textures[names[name]])

    def updatePositions(self, positionNames, positionVals):
        for obj in positionNames:
            self.scene[obj].update(positionVals[positionNames[obj]][0:3])

    def addRegularPlanet(self, position, radius, name, textureIndex=0, texture="earth"):
        self.scene[name]=sphere(radius, position, self,textureUnit=textureIndex, textureName=texture)

    def render(self):
        #clears the framebuffer and then swaps buffers
        self.ctx.clear(color=(.08,.16,.18))
        for obj in self.scene:
            self.scene[obj].render()
        pg.display.flip()

    def destroy(self):
        for obj in self.scene:
            self.scene[obj].destroy()