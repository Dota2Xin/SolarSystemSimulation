import moderngl as mgl
import sys
import glm
import pygame as pg
from .models import *
from .camera import *
from .menu import *

class graphicsEngine:
    def __init__(self,graphicsSettings,names, currentState, textures,lengthScale, winSize=[1300,700], cameraExtras=[], fullscreen=False):
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
            self.camera=camera([50,.01,100000],cameraParams, self.winSize, speedParams,cameraExtras=cameraExtras)
        else:
            self.camera=camera([50,.01,100000],cameraParams, self.winSize, speedParams)
        #scene
        self.scene={}
        self.decorators = []
        self.createScene(names,currentState, textures, lengthScale)
        self.skybox = cube(49999, self.camera.position, self,textureName="hipp8")

    def createScene(self,names, currentState, textures, lengthScale):
        for name in names:
            self.scene[name]=sphere(currentState[names[name]][-1]/lengthScale,currentState[names[name]][0:3]/lengthScale,self,textureUnit=names[name]+1, textureName=textures[names[name]])
        saturn=self.scene["Saturn"]
        self.decorators.append(ring(saturn.radius+5.0,saturn.radius+10.0,saturn.position, self, saturn, textureUnit=names["Saturn"]+100))


    def updatePositions(self, positionNames, positionVals, lengthScaleFactor):
        for obj in positionNames:
            position=np.asarray(positionVals[positionNames[obj]][0:3])/lengthScaleFactor
            self.scene[obj].update(position)
        for decorator in self.decorators:
            decorator.update()
        self.skybox.update(self.camera.position)

    def addRegularPlanet(self, position, radius, name,lengthScale, textureIndex=0, texture="earth"):
        self.scene[name]=sphere(radius/lengthScale, position, self,textureUnit=textureIndex+1, textureName=texture)

    def updateScreenWindowed(self, winSize):
        self.winSize=winSize
        self.screen=pg.display.set_mode(self.winSize,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        self.camera.width=winSize[0]
        self.camera.aspectRatio=winSize[0]/winSize[1]

    def render(self):
        #clears the framebuffer and then swaps buffers
        self.ctx.clear(color=(1.0,.4,.4))
        for obj in self.scene:
            self.scene[obj].render()
        for decorator in self.decorators:
            decorator.render()
        self.skybox.render()
        #self.menu.render()
        #self.screen.blit(self.menu.menuSurface, tuple(self.menu.position))
        pg.display.flip()

    def destroy(self):
        for obj in self.scene:
            self.scene[obj].destroy()