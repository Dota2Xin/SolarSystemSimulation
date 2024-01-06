import requests
import numpy as np
import datetime

#this fail contains a set of helper functions that will use the NASA API: https://ssd.jpl.nasa.gov/horizons/ to get live data on the solar system
#This function returns a current state array that is from the whole solar system


def getSolarSystemData():

    #loads list of important astronomical objects, mass and radius are hardcoded in
    objectList=np.loadtxt("importantBodies.txt", dtype='str')
    for object in objectList:
        getObjectData(object[1])

    #pass the actual request
    #getObjectData(command)

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
    print(data.text)
    #TODO= Get position data from the data by finding the string and doing substrings and string.split(' '), mass and radius are already hardcoded in

