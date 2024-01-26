

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

def entitySwitch(menu):
    pass

def addEntity(menu):
    pass

def editEntity(menu):
    pass

def teleport(menu):
    pass