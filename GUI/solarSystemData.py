import requests
import numpy as np
import datetime

#this fail contains a set of helper functions that will use the NASA API: https://ssd.jpl.nasa.gov/horizons/ to get live data on the solar system
#This function returns a current state array that is from the whole solar system


def getSolarSystemData():

    #loads list of important astronomical objects, mass and radius are hardcoded in
    objectList=np.loadtxt("importantBodies.txt", dtype='str')
    stateArray=[]
    names={}
    count=0
    textures=[]
    for object in objectList:
        currentObject=np.asarray(getObjectData(object[1])+[float(object[3])/(10**27)]+[float(object[4])/1000000])
        stateArray.append(currentObject)
        names[object[0]]=count
        textures.append(object[2])
        count+=1
    stateArray=np.asarray(stateArray)
    return stateArray, names, textures


def getVar(dataText, type):
    index = dataText.find(f"{type}=")
    tempData = dataText[index + 3:index + 102].split(' ')
    numIndex = 0
    if tempData[0] == "":
        numIndex = 1
    pos = float(tempData[numIndex])
    return pos


def getObjectData(command):
    #info on command format at this link:https://ssd-api.jpl.nasa.gov/doc/horizons.html
    dataFormat = "text"
    objectData="YES"
    ephemData="YES"
    dataType="VECTORS"
    coordinateCenter="500@0"

    currentDate=datetime.date.today()
    tommorowDate=currentDate+datetime.timedelta(days=1)
    startTime=str(currentDate)
    finalTime=str(tommorowDate)
    stepSize='1d'

    data=requests.get(f"https://ssd.jpl.nasa.gov/api/horizons.api?format={dataFormat}&COMMAND={command}&OBJ_DATA={objectData}&MAKE_EPHEM={ephemData}&EPHEM_TYPE={dataType}&CENTER={coordinateCenter}&START_TIME={startTime}&STOP_TIME={finalTime}&STEP_SIZE={stepSize}")
    dataText=data.text
    position=(getVar(dataText,"X "), getVar(dataText,"Y "), getVar(dataText, "Z "))
    velocity=(getVar(dataText, "VX"), getVar(dataText, "VY"), getVar(dataText, "VZ"))
    return [position[0],position[1],position[2], velocity[0], velocity[1], velocity[2]]
