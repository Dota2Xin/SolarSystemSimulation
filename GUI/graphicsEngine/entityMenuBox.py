from GUI.graphicsEngine.button import *
import pygame as pg
from GUI.graphicsEngine.buttonFunctions import *
from GUI.graphicsEngine.dropdown import *
from GUI.graphicsEngine.textbox import *
from GUI.graphicsEngine.menuHelpers import *
from GUI.graphicsEngine.switch import *

class entityMenuBox:

    def __init__(self, color,position, size, menu , name, borderThickness=2):
        #position of top left of button
        self.borderThickness=borderThickness
        self.position=position
        self.height=size[0]
        self.width=size[1]
        self.color=color
        self.name=name

        #engine the game is running
        self.menu=menu

        #Pick font to stand out from thingy
        self.font=pg.font.Font(None, int(self.height/4.0))
        self.textColor=color
        if np.sum(self.color)>382:
            self.textColor=[0,0,0]
        else:
            self.textColor=[255,255,255]

        #State settings
        self.pressed=False
        self.on=False

        self.upButton=button(self.color,self.position,(int(self.height/2.0), int(self.width/8.0)),"U",self.menu,upEntity,self, "upButton")
        self.downButton=button(self.color,(self.position[0],int(self.position[1]+self.height/2.0)),(int(self.height/2.0), int(self.width/8.0)),"D",self.menu,downEntity,self, "downButton")
        self.switches=self.initSwitches()
        self.startIndex=0
        self.endIndex=7
        if self.endIndex>len(self.switches):
            self.currentSwitches=self.switches
        else:
            self.currentSwitches=self.switches[self.startIndex:self.endIndex]
        self.onSwitch=None
        #self.hover=False

    def initSwitches(self):
        switches=[]
        i=0
        for name in self.menu.names:
            xPos=self.position[0]+self.upButton.width
            yPos=self.position[1]+(i)*self.height/7
            switchName=name
            tempSwitch=switch(self.color, [xPos, yPos],(self.height/7,self.width*(7.0/8)),switchName, self.menu, entitySwitch,self.menu, switchName, borderThickness=1)
            switches.append(tempSwitch)
            i=i+1
        return switches

    #Updates display based on whether up (direction=True) or down (direction=False) was pressed
    def updateCurrentSwitches(self, direction):
        if direction:
            deltaY=self.height/7.0
        else:
            deltaY=-self.height/7.0
        for switchThing in self.switches:
            switchThing.position=[switchThing.position[0],switchThing.position[1]+deltaY]
        self.currentSwitches=self.switches[self.startIndex:self.endIndex]

    def render(self):
        invertColor = [255 - self.color[0], 255 - self.color[1], 255 - self.color[2]]
        pg.draw.rect(self.menu.screen, tuple(invertColor), (
            self.position[0], self.position[1], self.width, self.height))
        pg.draw.rect(self.menu.screen, self.color, (
        self.position[0] + self.borderThickness, self.position[1] + self.borderThickness,
        self.width - 2 * self.borderThickness, self.height - 2 * self.borderThickness))
        #if self.on:
            #print(self.currentButtons)
        self.upButton.render()
        self.downButton.render()
        for switch in self.currentSwitches:
            switch.render()


