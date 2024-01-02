import moderngl as mgl
import sys
import pygame as pg

class graphicsEngine:
    def __init__(self, winSize=(1600,900)):
        pg.init()
        self.winSize=winSize

        #tell pg what openGL to use
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        #set pg to display using doublebuffer
        pg.display.set_mode(self.winSize,flags=pg.OPENGL | pg.DOUBLEBUF)

        self.ctx=mgl.create_context()

        self.clock=pg.time.Clock()

    def render(self):
        #clears the framebuffer and then swaps buffers
        self.ctx.clear(color=(.08,.16,.18))
        pg.display.flip()