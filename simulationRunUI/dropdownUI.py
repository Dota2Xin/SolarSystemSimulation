import pygame as pg
import numpy as np
from buttonFunctionsUI import *
from buttonUI import *

class dropdown:

    def __init__(self, color,position, size, menu,options , name, borderThickness=1):
        #position of top left of button
        self.borderThickness=borderThickness
        self.position=position
        self.height=size[0]
        self.width=size[1]
        self.color=color
        self.name=name
        #Options the menu lets you select between
        self.options=options
        self.currentText=options[0]

        #engine the game is running
        self.menu=menu

        self.font=pg.font.Font(None, int(self.height/4.0))
        self.textColor=color
        if np.sum(self.color)>382:
            self.textColor=[0,0,0]
        else:
            self.textColor=[255,255,255]

        #State settings
        self.pressed=False
        self.on=False
        self.buttons=self.createButtons()
        self.currentButtons=[]
        #self.hover=False

    def createButtons(self):
        buttons=[]
        for i in range(len(self.options)):
            xPos=self.position[0]
            yPos=self.position[1]+self.height+(i)*self.height/2.0
            buttonName=self.name+"button"+str(i)
            tempButton=button(self.color, [xPos, yPos],(self.height/2.0,self.width),self.options[i], self.menu, updateDropbox, [self, self.options[i]], buttonName, borderThickness=1)
            buttons.append(tempButton)
        return buttons

    def checkInside(self, eventPos):
        eventX=eventPos[0]
        eventY=eventPos[1]
        if ((eventX>self.position[0]) and eventX<(self.position[0]+self.width)) and ((eventY>self.position[1]) and eventY<(self.position[1]+self.height)):
            self.pressed=True
            self.color=[self.color[0]/1.5,self.color[1]/1.5,self.color[2]/1.5]
            return True

        return False

    def unpress(self):
        self.pressed = False
        self.color = [self.color[0] * 1.5, self.color[1] * 1.5, self.color[2] * 1.5]
        if self.on:
            self.on=False
            self.currentButtons=[]
        else:
            self.on=True
            self.currentButtons=self.buttons[0:]


    def render(self):
        invertColor = [255 - self.color[0], 255 - self.color[1], 255 - self.color[2]]
        pg.draw.rect(self.menu.screen, tuple(invertColor), (
            self.position[0], self.position[1], self.width, self.height))
        pg.draw.rect(self.menu.screen, self.color, (
        self.position[0] + self.borderThickness, self.position[1] + self.borderThickness,
        self.width - 2 * self.borderThickness, self.height - 2 * self.borderThickness))
        textSurface = self.font.render(self.currentText, True, self.textColor)
        # print("HELLO NURESE!!!!")
        textX = int(self.position[0] + (self.width - textSurface.get_width()) / 2.0)
        textY = int(self.position[1] + (self.height - textSurface.get_height()) / 2.0)
        self.menu.screen.blit(textSurface, (textX, textY))
        #if self.on:
            #print(self.currentButtons)
        for button in self.currentButtons:
            button.render()



