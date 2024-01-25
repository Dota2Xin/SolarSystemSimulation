import pygame as pg
import numpy as np

class switch:

    def __init__(self, color,position, size, text, menu, switchFunc,switchFuncParams,name, borderThickness=5):
        #position of top left of button
        self.borderThickness=borderThickness
        self.switchFuncParams=switchFuncParams
        self.position=position
        self.height=size[0]
        self.width=size[1]
        self.switchFunc=switchFunc
        self.color=color
        self.name=name
        #engine the game is running
        self.menu=menu

        self.text=text
        self.font=pg.font.Font(None, int(self.height/4.0))
        self.textColor=color
        if np.sum(self.color)>382:
            self.textColor=[0,0,0]
        else:
            self.textColor=[255,255,255]

        #State settings
        self.on=False
        self.pressed=False
        #self.hover=False

    def checkInside(self, eventPos):
        eventX=eventPos[0]
        eventY=eventPos[1]
        if ((eventX>self.position[0]) and eventX<(self.position[0]+self.width)) and ((eventY>self.position[1]) and eventY<(self.position[1]+self.height)):
            self.pressed=True
            self.color=[self.color[0]/1.5,self.color[1]/1.5,self.color[2]/1.5]
            self.borderThickness=2*self.borderThickness
            return True

        return False

    def unpressButton(self):
        self.pressed=False
        self.on=True
        self.borderThickness=self.borderThickness/2
        #self.color=[self.color[0]*1.5,self.color[1]*1.5,self.color[2]*1.5]
        self.switchFunc(self.switchFuncParams)
        print("Working lolz")

    def switchOff(self):
        self.on=False
        self.color = [self.color[0] * 1.5, self.color[1] * 1.5, self.color[2] * 1.5]

    def render(self):
        invertColor = [255 - self.color[0], 255 - self.color[1], 255 - self.color[2]]
        pg.draw.rect(self.menu.screen, tuple(invertColor), (
        self.position[0], self.position[1], self.width,self.height))
        pg.draw.rect(self.menu.screen, self.color, (self.position[0]+self.borderThickness, self.position[1]+self.borderThickness, self.width-2*self.borderThickness, self.height-2*self.borderThickness))
        textSurface=self.font.render(self.text, True, self.textColor)
        #print("HELLO NURESE!!!!")
        textX=int(self.position[0]+(self.width-textSurface.get_width())/2.0)
        textY=int(self.position[1]+(self.height-textSurface.get_height())/2.0)
        self.menu.screen.blit(textSurface, (textX,textY))


