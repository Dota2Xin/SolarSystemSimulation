from switchUI import *
from buttonUI import *
from buttonFunctionsUI import *
from dropdownUI import *
from entityMenuBoxUI import *
from textboxUI import *

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

    entityPosition=[menu.width/20.0, .02*menu.height]
    entityMenu=entityMenuBox(buttonColor,entityPosition,[menu.height*(25.0/32.0), menu.width/2.0],menu,"entityMenu")

    menu.entityMenus.append(entityMenu)

    #stuff for buttons
    buttonColor = (255, 255, 255)

    buttonY = int(menu.height * .85)
    buttonX = int(menu.width * .45)

    spacing = int(menu.width * .02)
    buttonHeight = int(menu.height * .12)
    buttonWidth = int(menu.width * .16)

    outputButton = button(buttonColor, (buttonX-2*buttonWidth-2*spacing, buttonY), (buttonHeight, buttonWidth), "Output Dir",
                        menu, outputDirFunc, menu, "outputButton")
    editButton= button(buttonColor, (buttonX-buttonWidth-spacing, buttonY), (buttonHeight, buttonWidth), "Edit",
                         menu, editEntity, menu, "editButton")
    addButton= button(buttonColor, (buttonX, buttonY), (buttonHeight, buttonWidth), "Add",
                         menu, addEntity, menu, "addButton")
    leaveButton = button(buttonColor, (buttonX + buttonWidth + spacing, buttonY), (buttonHeight, buttonWidth), "Exit",
                         menu, leaveMenu, menu, "leaveButtonEntity")
    runButton = button(buttonColor, (buttonX + 2 * buttonWidth + 2 * spacing, buttonY), (buttonHeight, buttonWidth),
                          "Run Simulation", menu, runSim, menu, "runButton")

    menu.buttons.append(leaveButton)
    menu.buttons.append(runButton)
    menu.buttons.append(outputButton)
    menu.buttons.append(editButton)
    menu.buttons.append(addButton)

    #stuff for textboxes:
    graphicsLabelY = menu.height * .02
    graphicsLabelX = int(menu.width * .01)+menu.width/20.0+ menu.width/2.0
    labelHeight = int(menu.height * .08)
    labelWidth = int(menu.width * .12)

    #position
    positionLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY), (labelHeight, labelWidth), menu,
                               "positionLabel", mutable=False, borderThickness=0, rightAligned=True)
    positionLabelBox.text = "Position:"

    elementWidth=menu.width*.23
    positionValueBox = textbox(buttonColor, (graphicsLabelX+spacing+labelWidth, graphicsLabelY), (labelHeight, elementWidth), menu,
                               "positionValues")

    spacingY=labelHeight+menu.height*.015
    #velocity
    velocityLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY+ spacingY), (labelHeight, labelWidth), menu,
                               "velocityLabel", mutable=False, borderThickness=0, rightAligned=True)
    velocityLabelBox.text = "Velocity:"

    velocityValueBox = textbox(buttonColor, (graphicsLabelX + spacing + labelWidth, graphicsLabelY+spacingY),
                               (labelHeight, elementWidth), menu,
                               "velocityValues")

    # mass
    massLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY + 2*spacingY),
                               (labelHeight, labelWidth), menu,
                               "massLabel", mutable=False, borderThickness=0, rightAligned=True)
    massLabelBox.text = "Mass:"

    massValueBox = textbox(buttonColor,
                               (graphicsLabelX + spacing + labelWidth, graphicsLabelY + 2*spacingY),
                               (labelHeight, elementWidth), menu,
                               "massValues")

    # Radius
    radiusLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY + 3 * spacingY),
                           (labelHeight, labelWidth), menu,
                           "radiusLabel", mutable=False, borderThickness=0, rightAligned=True)
    radiusLabelBox.text = "Radius:"

    radiusValueBox = textbox(buttonColor,
                           (graphicsLabelX + spacing + labelWidth, graphicsLabelY + 3 * spacingY),
                           (labelHeight, elementWidth), menu,
                           "radiusValues")

    #Textboxes for params only for adding stuff:
    addLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY +3.8 * spacingY),
                             (labelHeight, labelWidth), menu,
                             "addLabel", mutable=False, borderThickness=0, rightAligned=True)
    addLabelBox.text = "Sim Params:"

    timeLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY + 4.5 * spacingY),
                             (labelHeight, labelWidth), menu,
                             "timeLabel", mutable=False, borderThickness=0, rightAligned=True)
    timeLabelBox.text = "Final Time:"

    timeValueBox = textbox(buttonColor,
                             (graphicsLabelX + spacing + labelWidth, graphicsLabelY + 4.5 * spacingY),
                             (labelHeight, elementWidth), menu,
                             "timeValues")

    stepsLabelBox = textbox(menu.color, (graphicsLabelX, graphicsLabelY + 5.5 * spacingY),
                           (labelHeight, labelWidth), menu,
                           "stepsLabel", mutable=False, borderThickness=0, rightAligned=True)
    stepsLabelBox.text = "Total Steps:"

    stepsValueBox = textbox(buttonColor,
                           (graphicsLabelX + spacing + labelWidth, graphicsLabelY + 5.5 * spacingY),
                           (labelHeight, elementWidth), menu,
                           "stepsValues")
    #inputFile
    inputFileButton=button(buttonColor, (graphicsLabelX+menu.width*.07, graphicsLabelY + 6.5 * spacingY),
                             (labelHeight, elementWidth*.75), "Input File",menu,setInputFile,menu,
                             "inputFileButton", borderThickness=2)

    #dropdown menu
    inputDropdown=dropdown(buttonColor, (graphicsLabelX+spacing+elementWidth*.75+menu.width*.07, graphicsLabelY + 6.5 * spacingY), (labelHeight,elementWidth*.75), menu, ["Use Input", "Don't Use Input"], "inputDropdown")

    menu.buttons.append(inputFileButton)
    menu.dropDowns.append(inputDropdown)
    menu.textboxes.append(radiusValueBox)
    menu.textboxes.append(radiusLabelBox)
    menu.textboxes.append(massValueBox)
    menu.textboxes.append(massLabelBox)
    menu.textboxes.append(velocityValueBox)
    menu.textboxes.append(velocityLabelBox)
    menu.textboxes.append(positionValueBox)
    menu.textboxes.append(positionLabelBox)
    menu.textboxes.append(timeValueBox)
    menu.textboxes.append(timeLabelBox)
    menu.textboxes.append(addLabelBox)
    menu.textboxes.append(stepsLabelBox)
    menu.textboxes.append(stepsValueBox)
    pass
