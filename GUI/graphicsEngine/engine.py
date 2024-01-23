import moderngl as mgl
import sys
import glm
import pygame as pg
from .models import *
from .camera import *
from .menu import *

class graphicsEngine:
    def __init__(self,graphicsSettings,names, currentState, textures, winSize=[1300,700], cameraExtras=[], fullscreen=False):
        pg.init()
        self.winSize=winSize

        #tell pg what openGL to use
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        #set pg to display using doublebuffer
        if fullscreen:
            self.screen = pg.display.set_mode(self.winSize, flags=pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        else:
            self.screen=pg.display.set_mode(self.winSize,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        self.ctx=mgl.create_context()
        #self.ctx.front_face='cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST) #| mgl.CULL_FACE)

        self.clock=pg.time.Clock()

        cameraParams=graphicsSettings["cameraFrustumParams"]
        speedParams=[graphicsSettings["cameraSpeed"], graphicsSettings["cameraSensitivity"]]
        if cameraExtras !=[]:
            self.camera=camera([50,.1,10000],cameraParams, self.winSize, speedParams,cameraExtras=cameraExtras)
        else:
            self.camera=camera([50,.1,10000],cameraParams, self.winSize, speedParams)
        #scene
        self.scene={}
        self.createScene(names,currentState, textures)

    def createScene(self,names, currentState, textures):
        for name in names:
            self.scene[name]=sphere(currentState[names[name]][-1],currentState[names[name]][0:3],self,textureUnit=names[name], textureName=textures[names[name]])

    def updatePositions(self, positionNames, positionVals, lengthScaleFactor):
        for obj in positionNames:
            position=np.asarray(positionVals[positionNames[obj]][0:3])/lengthScaleFactor
            self.scene[obj].update(position)

    def addRegularPlanet(self, position, radius, name, textureIndex=0, texture="earth"):
        self.scene[name]=sphere(radius, position, self,textureUnit=textureIndex, textureName=texture)

    def updateScreenWindowed(self, winSize):
        self.winSize=winSize
        self.screen=pg.display.set_mode(self.winSize,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self.camera.width=winSize[0]
        self.camera.aspectRatio=winSize[0]/winSize[1]

    def render(self):
        #clears the framebuffer and then swaps buffers
        self.ctx.clear(color=(0.0,0.0,0.0))
        for obj in self.scene:
            self.scene[obj].render()
        #self.menu.render()
        #self.screen.blit(self.menu.menuSurface, tuple(self.menu.position))
        pg.display.flip()

    def destroy(self):
        for obj in self.scene:
            self.scene[obj].destroy()