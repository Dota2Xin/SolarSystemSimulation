from GUI.graphicsEngine.button import *
import pygame as pg
from GUI.graphicsEngine.buttonFunctions import *
from GUI.graphicsEngine.dropdown import *
from GUI.graphicsEngine.textbox import *
from GUI.graphicsEngine.menuHelpers import *

class menu:

    def __init__(self, winSize, simulationParams, currentState, names, textures, fullscreen):
        self.state=0 #describes state of menu, 0= Menu is off, 1=general graphics/app options,
                     # 2=simulation options, 3=Menu for adding entity, 4=Menu for viewing, editing, and taking away entities

        self.height = winSize[1]
        self.width = winSize[0]

        self.color=[50, 230, 230]
        if fullscreen:
            self.screen = pg.display.set_mode(winSize, flags=pg.DOUBLEBUF | pg.FULLSCREEN)
        else:
            self.screen=pg.display.set_mode(winSize, flags= pg.DOUBLEBUF | pg.RESIZABLE)
        self.typing=False
        #self.menuSurface = pg.Surface((int(self.width), int(self.height)))
        #Play with the scaling options
        #Store sim data
        self.simulationParams=simulationParams
        self.currentState=currentState
        self.names=names
        self.textures=textures
        # position of top left of menu
        #self.position = [winSize[0]-self.width*1.1, winSize[1]-self.height*1.1]
        #print(self.position)
        self.currentButtons=[]
        self.currentDropdowns=[]
        self.currentTextboxes = []

        self.buttons=[]
        self.dropDowns=[]
        self.textboxes=[]
        self.running=True
        self.onInit()

    #this function will initialize all the objects we need and then the different states will just change the ones we render
    #objects means buttons, rectangles, etc...
    def onInit(self):
        createMainMenu(self)

        self.buttons.append(button([255,255,255],(int(self.height/2.0),int(self.width/2.0)),(100,200),"Press me",self, changeColor, self, "button1"))
        self.currentButtons.append(self.buttons[0])
        options1=["Press this one", "No press me!", "LOL IDK BRO"]
        dropDown1=dropdown([255,255,255],(int(self.height/2.0-250),int(self.width/2.0-250)),(100,200),self, options1, "dropdown1")
        self.dropDowns.append(dropDown1)
        self.currentDropdowns.append(dropDown1)

        textBox1=textbox([255,255,255],(int(self.height/2.0-250),int(self.width/2.0)),(100,200),self, "textbox1")
        self.textboxes.append(textBox1)
        self.currentTextboxes.append(textBox1)

        self.renderMainSettings()
        pass

    def render(self):
        #self.menuSurface.fill((255,255,255, 255))
        self.screen.fill(tuple(self.color))
        for button in self.currentButtons:
            button.render()

        for textboxes in self.currentTextboxes:
            textboxes.render()

        for dropdown in self.currentDropdowns:
            dropdown.render()

        pg.display.flip()
        #self.engine.screen.blit(self.menuSurface, tuple(self.position))

    def renderMainSettings(self):
        buttonNames={"applyButton":1, "leaveButton":1, "entityButton":1}
        self.currentButtons=[]
        self.currentTextboxes=[]
        self.currentDropdowns=[]

        for button in self.buttons:
            if button.name in buttonNames:
                self.currentButtons.append(button)
                print("HERE WE Gz")

        textboxNames={"graphicsLabel":1, "fullscreenLabel":1, "simulationSettings":1, "simSpeedLabel":1, "cameraSpeedLabel":1, "cameraSpeed":1, "simSpeed":1, "collisionsLabel":1}

        for textbox in self.textboxes:
            if textbox.name in textboxNames:
                self.currentTextboxes.append(textbox)

        dropdownNames={"fullscreen":1, "collisions":1}

        for dropdown in self.dropDowns:
            if dropdown.name in dropdownNames:
                self.currentDropdowns.append(dropdown)

    def renderSimulationSettings(self):
        pass

    def renderAddingEntity(self):
        pass

    def renderEntityMenu(self):
        pass

    def controlTextboxKeydown(self, event):
        if self.typing:
            for textbox in self.textboxes:
                if textbox.on:
                    currentStr = str(pg.key.name(event.key))
                    if event.key == pg.K_SPACE:
                        textbox.currentLocation = textbox.currentLocation + 1
                        textbox.text = textbox.text[0:textbox.currentLocation] + " " + textbox.text[
                                                                                       textbox.currentLocation:]
                    elif event.key == pg.K_RIGHT:
                        textbox.currentLocation = textbox.currentLocation + 1
                    elif event.key == pg.K_LEFT:
                        textbox.currentLocation = textbox.currentLocation - 1
                    elif event.key == pg.K_BACKSPACE:
                        if currentStr != "":
                            textbox.text = textbox.text[0:textbox.currentLocation - 1] + textbox.text[
                                                                                         textbox.currentLocation:]
                            textbox.currentLocation = textbox.currentLocation - 1
                    elif len(currentStr) > 1:
                        currentStr = ""
                    else:
                        textbox.text = textbox.text[0:textbox.currentLocation] + currentStr + textbox.text[
                                                                                              textbox.currentLocation:]
                        if currentStr != "":
                            textbox.currentLocation = textbox.currentLocation + 1

    def controlMouseButtonDown(self, event):
        self.typing = False
        if event.button == 1:
            for button in self.currentButtons:
                button.checkInside(event.pos)
            for textbox in self.currentTextboxes:
                if textbox.mutable:
                    textbox.checkInside(event.pos)
            for dropdown in self.currentDropdowns:
                dropdown.checkInside(event.pos)
                for dropdownButtons in dropdown.currentButtons:
                    dropdownButtons.checkInside(event.pos)

    def controlMouseButtonUp(self, event):
        self.typing = False
        if event.button == 1:
            for button in self.currentButtons:
                if button.pressed:
                    button.unpressButton()
            for textbox in self.currentTextboxes:
                if textbox.pressed:
                    textbox.unpress()
            for dropdown in self.currentDropdowns:
                for dropdownButtons in dropdown.currentButtons:
                    if dropdownButtons.pressed:
                        dropdownButtons.unpressButton()
                if dropdown.pressed:
                    dropdown.unpress()

    def run(self):
        self.running=True
        while self.running:
            self.render()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                elif event.type==pg.KEYDOWN:
                    self.controlTextboxKeydown(event)
                elif event.type==pg.KEYUP:
                    if not self.typing:
                        if event.key==pg.K_m:
                            self.running=False
                elif event.type==pg.MOUSEBUTTONDOWN:
                    self.controlMouseButtonDown(event)
                elif event.type==pg.MOUSEBUTTONUP:
                    self.controlMouseButtonUp(event)

        return self.currentState, self.names, self.textures, self.simulationParams




