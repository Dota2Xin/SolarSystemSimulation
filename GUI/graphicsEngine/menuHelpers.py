import pygame as pg
from GUI.graphicsEngine.button import *
import pygame as pg
from GUI.graphicsEngine.buttonFunctions import *
from GUI.graphicsEngine.dropdown import *
from GUI.graphicsEngine.textbox import *
from GUI.graphicsEngine.entityMenuBox import *

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

    graphicsLabelY=int(menu.height*.03)
    graphicsLabelX=int(menu.width*.03)
    labelHeight=int(menu.height*.12)
    labelWidth=int(menu.width*.12)
    graphicsLabelBox=textbox(menu.color, (graphicsLabelX, graphicsLabelY), (labelHeight,labelWidth), menu, "graphicsLabel", mutable=False, borderThickness=0, rightAligned=True)
    graphicsLabelBox.text="Graphics Settings:"

    elementWidth=int(menu.width*.12)

    fullScreenLabelY=graphicsLabelY+labelHeight+int(menu.height*.03)
    fullScreenLabelX=graphicsLabelX
    fullScreenLabel=textbox(menu.color, (fullScreenLabelX, fullScreenLabelY), (labelHeight, elementWidth),menu, "fullscreenLabel", mutable=False, borderThickness=0, rightAligned=True)
    fullScreenLabel.text="Fullscreen:"

    simulationSettingsY = fullScreenLabelY + labelHeight + int(menu.height * .05)
    simulationSettingsX = graphicsLabelX
    simulationSettings=textbox(menu.color, (simulationSettingsX, simulationSettingsY), (labelHeight,labelWidth),menu, "simulationSettings",mutable=False, borderThickness=0, rightAligned=True)
    simulationSettings.text="Simulation Settings:"

    simulationParamsY=simulationSettingsY + labelHeight + int(menu.height * .03)
    simulationParamsX=graphicsLabelX

    simSpeedLabel=textbox(menu.color, (simulationParamsX, simulationParamsY), (labelHeight,elementWidth),menu, "simSpeedLabel", mutable=False, borderThickness=0, rightAligned=True)
    simSpeedLabel.text="Sim Speed:"

    simSpeedInput=textbox(buttonColor, (simulationParamsX+spacing+elementWidth, simulationParamsY), (labelHeight, elementWidth), menu, "simSpeed")

    cameraSpeedLabel = textbox(menu.color, (simulationParamsX+2*(spacing+elementWidth), simulationParamsY), (labelHeight, elementWidth), menu,"cameraSpeedLabel", mutable=False, borderThickness=0, rightAligned=True)
    cameraSpeedLabel.text = "Camera Speed:"

    cameraSpeedInput = textbox(buttonColor, (simulationParamsX + 3*(spacing + elementWidth), simulationParamsY),(labelHeight, elementWidth), menu, "cameraSpeed")

    collisionsX=graphicsLabelX
    collisionsY=simulationParamsY+ labelHeight + int(menu.height * .03)

    collisionsLabel=textbox(menu.color, (collisionsX, collisionsY), (labelHeight,elementWidth), menu, "collisionsLabel", mutable=False, borderThickness=0, rightAligned=True)
    collisionsLabel.text="Collisions:"

    menu.textboxes.append(collisionsLabel)
    menu.textboxes.append(cameraSpeedInput)
    menu.textboxes.append(cameraSpeedLabel)
    menu.textboxes.append(simSpeedInput)
    menu.textboxes.append(simSpeedLabel)
    menu.textboxes.append(simulationSettings)
    menu.textboxes.append(graphicsLabelBox)
    menu.textboxes.append(fullScreenLabel)

    fullscreenDropboxX=collisionsX+elementWidth+spacing
    fullscreenDropboxY=fullScreenLabelY

    fullScreenDropbox=dropdown(buttonColor, (fullscreenDropboxX, fullscreenDropboxY), (labelHeight,elementWidth), menu, ["Off", "On"], "fullscreen")

    collisionsDropbox = dropdown(buttonColor, (fullscreenDropboxX, collisionsY), (labelHeight, elementWidth),menu, ["Off", "On"], "collisions")

    menu.dropDowns.append(collisionsDropbox)
    menu.dropDowns.append(fullScreenDropbox)

    pass

def createEntityMenu(menu):
    buttonColor = (255, 255, 255)

    entityPosition=[menu.width/10.0, menu.height/10.0]
    entityMenu=entityMenuBox(buttonColor,entityPosition,[menu.height*(3.0/4.0), menu.width/2.0],menu,"entityMenu")

    menu.entityMenus.append(entityMenu)

    pass
