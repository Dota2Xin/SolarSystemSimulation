from GUI.graphicsEngine.button import *
import pygame as pg
from GUI.graphicsEngine.buttonFunctions import *

class menu:

    def __init__(self, winSize):
        self.state=0 #describes state of menu, 0= Menu is off, 1=general graphics/app options,
                     # 2=simulation options, 3=Menu for adding entity, 4=Menu for viewing, editing, and taking away entities

        self.height = winSize[0]
        self.width = winSize[1]

        self.color=[50, 230, 230]
        self.screen=pg.display.set_mode(winSize, flags= pg.DOUBLEBUF | pg.RESIZABLE)

        #self.menuSurface = pg.Surface((int(self.width), int(self.height)))
        #Play with the scaling options

        # position of top left of menu
        #self.position = [winSize[0]-self.width*1.1, winSize[1]-self.height*1.1]
        #print(self.position)
        self.currentButtons=[]
        self.buttons=[]
        self.onInit()

    #this function will initialize all the objects we need and then the different states will just change the ones we render
    #objects means buttons, rectangles, etc...
    def onInit(self):
        self.buttons.append(button([255,255,255],(int(self.height/2.0),int(self.width/2.0)),(100,200),"Press me",self, changeColor, self))
        self.currentButtons.append(self.buttons[0])
        pass

    def render(self):
        #self.menuSurface.fill((255,255,255, 255))
        self.screen.fill(tuple(self.color))
        for button in self.currentButtons:
            button.render()

        pg.display.flip()
        #self.engine.screen.blit(self.menuSurface, tuple(self.position))

    def renderGraphicsSettings(self):
        pass

    def renderSimulationSettings(self):
        pass

    def renderAddingEntity(self):
        pass

    def renderEntityMenu(self):
        pass

    def run(self):
        running=True
        while running:
            self.render()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                elif event.type==pg.KEYUP:
                    if event.key==pg.K_m:
                        running=False
                elif event.type==pg.MOUSEBUTTONDOWN:
                    if event.button==1:
                        for button in self.currentButtons:
                            button.checkInside(event.pos)
                elif event.type==pg.MOUSEBUTTONUP:
                    if event.button==1:
                        for button in self.currentButtons:
                            if button.pressed:
                                button.unpressButton()




