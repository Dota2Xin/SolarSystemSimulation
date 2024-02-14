import numpy as np
from switchUI import *
from tkinter import Tk, filedialog


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
        for textbox in menu.currentTextboxes:
            if textbox.name=="positionValues":
                newPosition=parseDynamicString(textbox.text)
            elif textbox.name=="velocityValues":
                newVelocities=parseDynamicString(textbox.text)
            elif textbox.name=="radiusValues":
                radius=float(textbox.text.replace(" ", ""))
            elif textbox.name=="massValues":
                mass=float(textbox.text.replace(" ", ""))
        newState=[newPosition[0],newPosition[1],newPosition[2], newVelocities[0], newVelocities[1], newVelocities[2], mass, radius]
        objectName=menu.entityMenus[0].onSwitch.name
        objectIndex=menu.names[objectName]
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
        name="entity"+str(len(menu.names))
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
            except:
                textbox.text="Value Error"
                good=False
                break
        if good:
            newState = [newPosition[0], newPosition[1], newPosition[2], newVelocities[0], newVelocities[1],
                        newVelocities[2], mass, radius]
            if menu.currentState==[]:
                print("HELLO")
                menu.currentState = np.asarray([newState])
            else:
                menu.currentState=np.concatenate((menu.currentState,np.asarray([newState])),axis=0)
            menu.names[name]=len(menu.currentState)-1
            switches=menu.entityMenus[0].switches
            switchPos=switches[-1].position
            tempSwitch=switch((255,255,255), switchPos, (switches[0].height, switches[0].width), name, menu, entitySwitch,(menu, len(switches)-2, name),name,borderThickness=1)
            menu.entityMenus[0].switches.insert(len(switches)-1, tempSwitch)
            menu.entityMenus[0].switches[-1].position=[switchPos[0],switchPos[1]+switches[0].height]
            upEntity(menu.entityMenus[0])
    else:
        pass

def outputDirFunc(menu):
    try:
        root = Tk()
        root.withdraw()
        inputPath = filedialog.askdirectory()
        root.destroy()
        menu.outputPath = inputPath
        name = inputPath.split("/")[-1]
        if len(name) > 18:
            name = name[0:18] + ".."
        for textbox in menu.textboxes:
            if textbox.name == "outputLabel":
                textbox.text = "Output Dir:" + name
    except:
        return

def setInputFile(menu):
    try:
        root=Tk()
        root.withdraw()
        inputPath=filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        root.destroy()
        menu.inputPath=inputPath
        name=inputPath.split("/")[-1]
        if len(name)>18:
            name=name[0:18]+".."
        for textbox in menu.textboxes:
            if textbox.name=="inputLabel":
                textbox.text="Input File:"+name
    except:
        return

def parseInputFile(inputPath):
    initialStates=[]
    try:
        with open(inputPath, "r") as f:
            for line in f:
                currentLine=line.strip()
                stringValues=currentLine.split(" ")
                posX=float(stringValues[0])
                posY=float(stringValues[1])
                posZ=float(stringValues[2])
                velX=float(stringValues[3])
                velY=float(stringValues[4])
                velZ=float(stringValues[5])
                m=float(stringValues[6])
                R=float(stringValues[7])
                initialStates.append(np.asarray([posX, posY, posZ, velX, velY, velZ, m, R]))
        initialStates=np.asarray(initialStates)
        #print(initialStates)
        return initialStates
    except:
        print("Invalid Input File")
        return None


def runSim(menu):
    finalTime=0
    finalSteps=0
    for textbox in menu.textboxes:
        if textbox.name=="stepsValues":
            try:
                finalSteps=int(textbox.text)
            except:
                print("ERROR: Need integer steps")
        elif textbox.name=="timeValues":
            try:
                finalTime=float(textbox.text)
            except:
                print("ERROR: Need float final time")
    for dropdown in menu.currentDropdowns:
        if dropdown.name=="inputDropdown":
            if dropdown.currentText=="Use Input":
                menu.simStartState=np.asarray(parseInputFile(menu.inputPath))
                menu.simFinalTime=finalTime
                menu.simSteps=finalSteps
                menu.simRunning=True
                return
    menu.simStartState=np.asarray(menu.currentState)
    menu.simFinalTime = finalTime
    menu.simSteps = finalSteps
    menu.simRunning=True
    return