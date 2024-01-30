import numpy as np
from GUI.graphicsEngine.switch import *

def changeColor(menu):
    menu.color=[255-menu.color[0],255-menu.color[1],255-menu.color[2]]

def updateDropbox(dropboxParams):
    dropboxParams[0].currentText=dropboxParams[1]
    dropboxParams[0].on=False
    dropboxParams[0].currentButtons=[]

def leaveMenu(menu):
    menu.running=False

def applyChanges(menu):
    for dropdown in menu.currentDropdowns:
        if dropdown.name=="fullscreen":
            if dropdown.currentText=="On":
                menu.simulationParams['fullscreen']=True
            else:
                menu.simulationParams['fullscreen'] = False
        elif dropdown.name=="collisions":
            if dropdown.currentText == "On":
                menu.simulationParams['collisions'] = True
            else:
                menu.simulationParams['collisions'] = False

    for textbox in menu.currentTextboxes:
        if textbox.name=="cameraSpeed":
            if textbox.text=="":
                pass
            else:
                try:
                    menu.simulationParams['cameraSpeed']=float(textbox.text)
                except:
                    print("ERROR: Must imput valid float to speed")
        elif textbox.name=="simSpeed":
            if textbox.text=="":
                pass
            else:
                try:
                    menu.simulationParams['simSpeed']=float(textbox.text)
                except:
                    print("ERROR: Must imput valid float to speed")
    print("ALL GOOD")

def entityMenuSwap(menu):
    menu.renderEntityMenu()
    pass

def upEntity(entityMenu):
    startIndex=entityMenu.startIndex

    if startIndex==0:
        pass
    else:
        entityMenu.startIndex=startIndex-1
        entityMenu.endIndex=entityMenu.endIndex-1
        entityMenu.updateCurrentSwitches(True)

def downEntity(entityMenu):
    endIndex = entityMenu.endIndex

    if endIndex == len(entityMenu.switches):
        pass
    else:
        entityMenu.endIndex = endIndex + 1
        entityMenu.startIndex = entityMenu.startIndex + 1
        entityMenu.updateCurrentSwitches(False)
def mainMenuSwap(menu):
    menu.renderMainSettings()
    pass

def entitySwitch(params):
    menu=params[0]
    selfIndex=params[1]
    switchName=params[2]
    menu.entityMenus[0].onSwitch=menu.entityMenus[0].switches[selfIndex]
    currentObject=menu.currentState[menu.names[switchName]]
    position=currentObject[0:3]
    x=position[0]
    y=position[1]
    z=position[2]
    velocities=currentObject[3:6]
    vx=velocities[0]
    vy=velocities[1]
    vz=velocities[2]
    mass=currentObject[6]
    radius=currentObject[7]
    updatePosition=f"({x:.0f}, {y:.0f}, {z:.0f})"
    updateVelocity=f"({vx:.0f}, {vy:.0f}, {vz:0f})"

    updateMass=f"{mass:.6f}"
    updateRadius=f"{radius:.4f}"
    for textbox in menu.currentTextboxes:
        if textbox.name=="positionValues":
            textbox.text=updatePosition
        elif textbox.name=="velocityValues":
            textbox.text=updateVelocity
        elif textbox.name=="radiusValues":
            textbox.text=updateRadius
        elif textbox.name=="massValues":
            textbox.text=updateMass
    pass

def addSwitch(menu):
    menu.entityMenus[0].onSwitch=menu.entityMenus[0].switches[-1]
    for textbox in menu.currentTextboxes:
        if textbox.name == "positionValues":
            textbox.text = ""
        elif textbox.name == "velocityValues":
            textbox.text = ""
        elif textbox.name == "radiusValues":
            textbox.text = ""
        elif textbox.name == "massValues":
            textbox.text = ""
        elif textbox.name=="textureValues":
            textbox.text=""
        elif textbox.name=="nameValues":
            textbox.text=""

def parseDynamicString(string):
    updateStr=string.replace(" ", "")
    #gets rid of () at edges
    updateStr=string[1:len(string)-1]
    positions=updateStr.split(",")
    x=float(positions[0])
    y=float(positions[1])
    z=float(positions[2])
    return [x,y, z]
def editEntity(menu):
    if menu.entityMenus[0].onSwitch !=None:
        newPosition=[]
        newVelocities=[]
        mass=0
        radius=0
        name=menu.entityMenus[0].onSwitch.name
        texture=menu.textures[menu.names[name]]
        for textbox in menu.currentTextboxes:
            if textbox.name=="positionValues":
                newPosition=parseDynamicString(textbox.text)
            elif textbox.name=="velocityValues":
                newVelocities=parseDynamicString(textbox.text)
            elif textbox.name=="radiusValues":
                radius=float(textbox.text.replace(" ", ""))
            elif textbox.name=="massValues":
                mass=float(textbox.text.replace(" ", ""))
            elif textbox.name=="textureValues":
                if textbox.text!="":
                    texture=textbox.text.replace(" ", "").lower()
        newState=[newPosition[0],newPosition[1],newPosition[2], newVelocities[0], newVelocities[1], newVelocities[2], mass, radius]
        objectName=menu.entityMenus[0].onSwitch.name
        objectIndex=menu.names[objectName]
        menu.textures[objectIndex]=texture
        menu.currentState[objectIndex]=newState
    else:
        pass

def addEntity(menu):
    if menu.entityMenus[0].onSwitch ==None:
        return

    if menu.entityMenus[0].onSwitch.name=="add":
        newPosition = []
        newVelocities = []
        mass = 0
        radius = 0
        name=""
        texture=""
        good=True
        for textbox in menu.currentTextboxes:
            try:
                if textbox.name == "positionValues":
                    newPosition = parseDynamicString(textbox.text)
                elif textbox.name == "velocityValues":
                    newVelocities = parseDynamicString(textbox.text)
                elif textbox.name == "radiusValues":
                    radius = float(textbox.text.replace(" ", ""))
                elif textbox.name == "massValues":
                    mass = float(textbox.text.replace(" ", ""))
                elif textbox.name=="nameValues":
                    name=textbox.text
                elif textbox.name=="textureValues":
                    texture=textbox.text.replace(" ", "").lower()
            except:
                textbox.text="Value Error"
                good=False
                break
        if good:
            if (name.lower() in (key.lower() for key in menu.names)) or name=="add":
                for textbox in menu.currentTextboxes:
                    if textbox.name=="nameValues":
                        textbox.text="Err:Name in Use"
                pass
            else:
                newState = [newPosition[0], newPosition[1], newPosition[2], newVelocities[0], newVelocities[1],
                            newVelocities[2], mass, radius]
                menu.currentState=np.concatenate((menu.currentState,np.asarray([newState])),axis=0)
                menu.names[name]=len(menu.currentState)-1
                menu.textures.append(texture)
                switches=menu.entityMenus[0].switches
                switchPos=switches[-1].position
                tempSwitch=switch((255,255,255), switchPos, (switches[0].height, switches[0].width), name, menu, entitySwitch,(menu, len(switches)-2, name),name,borderThickness=1)
                menu.entityMenus[0].switches.insert(len(switches)-1, tempSwitch)
                menu.entityMenus[0].switches[-1].position=[switchPos[0],switchPos[1]+switches[0].height]
                upEntity(menu.entityMenus[0])
                downEntity(menu.entityMenus[0])
    else:
        pass

def teleport(menu):
    if menu.entityMenus[0].onSwitch != None:
        newPosition = []
        for textbox in menu.currentTextboxes:
            if textbox.name == "positionValues":
                newPosition = parseDynamicString(textbox.text)
        lengthScale=menu.simulationParams["lengthScale"]
        menu.simulationParams['currentPos']=[newPosition[0]/lengthScale, newPosition[1]/lengthScale, newPosition[2]/lengthScale]