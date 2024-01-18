

def changeColor(menu):
    menu.color=[255-menu.color[0],255-menu.color[1],255-menu.color[2]]

def updateDropbox(dropboxParams):
    dropboxParams[0].currentText=dropboxParams[1]
    dropboxParams[0].on=False
    dropboxParams[0].currentButtons=[]