import pygame as pg
from GUI.graphicsEngine.button import *
import pygame as pg
from GUI.graphicsEngine.buttonFunctions import *
from GUI.graphicsEngine.dropdown import *
from GUI.graphicsEngine.textbox import *

#creates the buttons and textboxes and stuff for the main menu
def createMainMenu(menu):

    buttonColor=(255,255,255)

    buttonY=int(menu.height*.85)
    buttonX=int(menu.width*.4)

    spacing=int(menu.width*.02)
    buttonHeight=int(menu.height*.12)
    buttonWidth=int(menu.width*.18)

    applyButton=button(buttonColor,(buttonX, buttonY) , (buttonHeight,buttonWidth),"Apply", menu, applyChanges, menu, "applyButton")
    leaveButton=button(buttonColor, (buttonX+buttonWidth+spacing,buttonY), (buttonHeight,buttonWidth), "Exit", menu, leaveMenu, menu, "leaveButton")
    entityButton=button(buttonColor,(buttonX+2*buttonWidth+2*spacing,buttonY),(buttonHeight,buttonWidth), "Entities", menu, entityMenuSwap,menu, "entityButton")

    menu.buttons.append(applyButton)
    menu.buttons.append(leaveButton)
    menu.buttons.append(entityButton)
    pass

def createEntityMenu(menu):
    pass
