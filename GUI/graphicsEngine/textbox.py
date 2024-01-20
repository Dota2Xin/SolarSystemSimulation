import pygame as pg
import numpy as np
from GUI.graphicsEngine.button import *
from GUI.graphicsEngine.buttonFunctions import *

class textbox:

    def __init__(self, color,position, size, menu,name,borderThickness=1, mutable=True):
        # position of top left of button
        self.borderThickness = borderThickness
        self.position = position
        self.height = size[0]
        self.width = size[1]
        self.color = color
        self.name=name
        #text stuff, current location is essentially which part of the string we add to or take away from
        self.currentLocation=0
        self.text=""
        # engine the game is running
        self.menu = menu

        self.font = pg.font.Font(None, int(self.height / 4.0))
        self.textColor = color
        if np.sum(self.color) > 382:
            self.textColor = [0, 0, 0]
        else:
            self.textColor = [255, 255, 255]

        self.on=False
        self.pressed=False
        self.mutable=mutable
        # self.hover=False

    def checkInside(self, eventPos):
        eventX=eventPos[0]
        eventY=eventPos[1]
        if ((eventX>self.position[0]) and eventX<(self.position[0]+self.width)) and ((eventY>self.position[1]) and eventY<(self.position[1]+self.height)):
            self.pressed=True
            self.color=[self.color[0]/1.5,self.color[1]/1.5,self.color[2]/1.5]
            return True

        return False

    def unpress(self):
        self.pressed=False
        self.color=[self.color[0]*1.5,self.color[1]*1.5,self.color[2]*1.5]

        if self.on:
            self.on=False
        else:
            self.on=True
            self.menu.typing=True

    def render(self):
        invertColor = [255 - self.color[0], 255 - self.color[1], 255 - self.color[2]]
        pg.draw.rect(self.menu.screen, tuple(invertColor), (
            self.position[0], self.position[1], self.width, self.height))
        pg.draw.rect(self.menu.screen, self.color, (
        self.position[0] + self.borderThickness, self.position[1] + self.borderThickness,
        self.width - 2 * self.borderThickness, self.height - 2 * self.borderThickness))


        textSurface = self.font.render(self.text, True, self.textColor)
        # print("HELLO NURESE!!!!")
        textX = int(self.position[0] + (self.width - textSurface.get_width()) / 2.0)
        textY = int(self.position[1] + (self.height - textSurface.get_height()) / 2.0)
        self.menu.screen.blit(textSurface, (textX, textY))

        if self.on:
            if len(self.text)==0:
                barX=textX
            else:
                barX = textX + (self.currentLocation/len(self.text)) * textSurface.get_width()
            barY = textY #textSurface.get_height()
            pg.draw.rect(self.menu.screen, self.textColor, (
                barX, barY,
                1, 15))

