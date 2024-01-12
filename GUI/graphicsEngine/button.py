import pygame as pg
import numpy as np

class button:

    def __init__(self, color, position, size, text, menu):
        #position of top left of button
        self.position=position
        self.height=size[0]
        self.width=size[1]

        self.color=color

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
        self.pressed=False
        #self.hover=False

    def checkInside(self, eventPos, pressed):
        eventX=eventPos[0]
        eventY=eventPos[1]

        if ((eventX>self.position[0]) and eventX<(self.position[0]+self.width)) and ((eventY>self.position[1]) and eventY<(self.position[1]+self.height)):
            if pressed:
                self.pressed=True
                self.color=[self.color[0]/1.5,self.color[1]/1.5,self.color[2]/1.5]
            return True

        return False

    def unpressButton(self):
        self.pressed=False
        self.color=[self.color[0]*1.5,self.color[1]*1.5,self.color[2]*1.5]

    def render(self):
        pg.draw.rect(self.menu.menuSurface, self.color, (self.position[0], self.position[1], self.width, self.height))
        textSurface=self.font.render(self.text, True, self.textColor)
        #print("HELLO NURESE!!!!")
        self.menu.menuSurface.blit(textSurface, ((self.position[0]+self.width-textSurface.get_width())/2.0,(self.position[1]+self.height-textSurface.get_height())/2.0))


