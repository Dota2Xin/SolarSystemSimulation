from GUI.graphicsEngine.button import *

class menu:

    def __init__(self, winSize, engine):
        self.state=0 #describes state of menu, 0= Menu is off, 1=general graphics/app options,
                     # 2=simulation options, 3=Menu for adding entity, 4=Menu for viewing, editing, and taking away entities

        self.height = winSize[1] / 2.0
        self.width = winSize[0] / 6.0

        self.engine=engine

        self.menuSurface = pg.Surface((int(self.width), int(self.height)))
        #Play with the scaling options

        # position of top left of menu
        self.position = [winSize[0]-self.width*1.1, winSize[1]-self.height*1.1]
        print(self.position)
        self.currentButtons=[]
        self.buttons=[]
        self.onInit()

    #this function will initialize all the objects we need and then the different states will just change the ones we render
    #objects means buttons, rectangles, etc...
    def onInit(self):
        self.buttons.append(button([255,255,255],self.position,(100,200),"Press me",self))
        self.currentButtons.append(self.buttons[0])
        pass

    def render(self):
        self.menuSurface.fill((255,255,255, 255))
        for button in self.currentButtons:
            button.render()
        #self.engine.screen.blit(self.menuSurface, tuple(self.position))

    def renderGraphicsSettings(self):
        pass

    def renderSimulationSettings(self):
        pass

    def renderAddingEntity(self):
        pass

    def renderEntityMenu(self):
        pass




