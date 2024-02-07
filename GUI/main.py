import pygame as pg
from src.numerics import dkdLeapfrogIntegrator as lf
from src.numerics import collisionCalculator as cc
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np
import glm
import controlEntities
from GUI import solarSystemData
import time
from numba import njit
from GUI.graphicsEngine.menu import menu
@njit
def calcFullTimeStep(currentState,timeStep, deltaTime, timeScale):
    tempArray=currentState[:]
    if timeScale >= 5000:
        while timeStep > 5000:
            tempArray = np.asarray(lf.dkdLeapfrogStep(tempArray, deltaTime * 5000))
            tempArray = np.asarray(cc.collisionCalculator(tempArray))
            timeStep = timeStep - 5000
        tempArray= np.asarray(lf.dkdLeapfrogStep(tempArray, deltaTime * timeStep))
        tempArray=np.asarray(cc.collisionCalculator(tempArray))
    else:
        tempArray = np.asarray(lf.dkdLeapfrogStep(tempArray, deltaTime * timeScale))
        tempArray = np.asarray(cc.collisionCalculator(tempArray))
    return tempArray

@njit
def calcFullTimeStepNoCollisions(currentState,timeStep, deltaTime, timeScale):
    tempArray = currentState[:]
    if timeScale >= 5000:
        while timeStep > 5000:
            tempArray = np.asarray(lf.dkdLeapfrogStep(tempArray, deltaTime * 5000))
            timeStep = timeStep - 5000
        tempArray = np.asarray(lf.dkdLeapfrogStep(tempArray, deltaTime * timeStep))
    else:
        tempArray = np.asarray(lf.dkdLeapfrogStep(tempArray, deltaTime * timeScale))
    return tempArray

def main():
    #Params
    timeScale=5000.0 #describes the correspondence between real time and sim time
    #Initialize this to solar system
    #describes the current state numerically
    currentState=np.asarray([[-1.0,0.0,0.0,.0000913393398,.0001582044,0.0,1000,.5],[1.0,0.0,0.0,.0000913393398,-.0001582044,0.0,1000,.5], [0.0,-1.732,0.0,-.00018267868,0.0,0.0,1000,.5]])
    names = {"Sphere1": 0, "Sphere2":1, "Sphere3":2}
    textures=["earth", "moon", "mars"]
    currentState, names, textures= solarSystemData.getSolarSystemData()
    #print(currentState)
    #Dictionary that contains the full state of the solar system, references to physical data, as well as graphics data
    mathematicalPositions=[]
    lengthScaleFactor=100000000
    radiusScaleFactor=0
    cameraPos=[currentState[0][0]/lengthScaleFactor,currentState[0][1]/lengthScaleFactor,currentState[0][2]/lengthScaleFactor]

    cameraSpeed=10.0

    currentSettings = {"fullscreen": False, "cameraSpeed": cameraSpeed, "simSpeed": timeScale, "collisions": True, "currentPos":cameraPos, "lengthScale":lengthScaleFactor}

    graphicsSettings={"cameraSpeed": cameraSpeed, "cameraSensitivity": .05, "cameraFrustumParams": [cameraPos,glm.vec3(0), [0.0,1.0,.5]]}
    #Initialize window
    engine=graphicsEngine(graphicsSettings,names, currentState, textures,lengthScaleFactor, fullscreen=currentSettings['fullscreen'])
    deltaTime=engine.clock.tick(60)*.001
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    freeMouse=False
    run=True
    objCount=len(currentState)
    while run:
        timeStep=timeScale
        '''
        Some logic for when timescales become more important
        if timeScale>=10000:
            while timeStep>10000:
                currentState = np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime * 10000))
                timeStep=timeStep-10000
            currentState = np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime * timeStep))
        else:
            currentState=np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime*timeScale))
        '''
        #currentState = np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime * timeScale))
        if currentSettings["collisions"]:
            currentState=calcFullTimeStep(currentState,timeStep, deltaTime,timeScale)
        else:
            currentState=calcFullTimeStepNoCollisions(currentState,timeStep, deltaTime,timeScale)
        #currentState=np.asarray(cc.collisionCalculator(currentState))
        engine.updatePositions(names,currentState, lengthScaleFactor)
        engine.render()
        engine.camera.update(deltaTime)
        deltaTime=engine.clock.tick(60)*.001
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
            elif event.type == pg.ACTIVEEVENT:
                if event.gain == 1:
                    pg.mouse.set_pos((engine.winSize[0]/2.0, engine.winSize[1]/2.0))
            elif event.type==pg.KEYUP:
                if event.key==pg.K_ESCAPE:
                    run=False
                elif event.key==pg.K_i:
                    currentPos=engine.camera.position+engine.camera.forward
                    objCount = objCount+1
                    currentState=controlEntities.addObject(f"Sphere{objCount}", [currentPos[0], currentPos[1], currentPos[2], 0.0,0.0,0.0,1000,1.0], engine, currentState, names, textures, lengthScaleFactor)
                if event.key==pg.K_y:
                    print(engine.camera.position)
                if event.key==pg.K_f:
                    freeMouse= not freeMouse
                    pg.mouse.set_visible(freeMouse)
                    pg.event.set_grab(not freeMouse)
                if event.key==pg.K_m:
                    freeMouse=True
                    pg.mouse.set_visible(True)
                    pg.event.set_grab(False)
                    ###UPDATE CAMERA SETTINGS BEFORE DESTROY ENGINE
                    graphicsSettings = {"cameraSpeed": currentSettings["cameraSpeed"], "cameraSensitivity": .05,
                                        "cameraFrustumParams": [engine.camera.position, glm.vec3(0), [0.0, 1.0, .5]]}
                    currentSettings["currentPos"]=engine.camera.position
                    cameraExtras=[engine.camera.pitch, engine.camera.yaw, engine.camera.forward, engine.camera.up, engine.camera.right]
                    engine.destroy()
                    tempMenu = menu(engine.winSize, currentSettings,currentState,names, textures, currentSettings['fullscreen'])
                    currentState, names, textures, currentSettings=tempMenu.run()
                    timeScale=currentSettings["simSpeed"]
                    graphicsSettings["cameraFrustumParams"]=[currentSettings["currentPos"], glm.vec3(0), [0.0, 1.0, .5]]
                    #RESET CAMERA TO HAVE RIGHT SETTINGS
                    engine=graphicsEngine(graphicsSettings,names,currentState,textures,lengthScaleFactor, cameraExtras=cameraExtras, fullscreen=currentSettings["fullscreen"])
                    pg.event.set_grab(True)
                    pg.mouse.set_visible(False)
                    freeMouse = False
            elif event.type == pg.VIDEORESIZE and (not currentSettings['fullscreen']):
                screenSize=[event.w, event.h]
                engine.updateScreenWindowed(screenSize)

    engine.destroy()
    pg.quit()

if __name__=='__main__':
    try:
        main()
    finally:
        pg.quit()



#timeStep=timeScale
        '''
        Some logic for when timescales become more important
        if timeScale>=10000:
            while timeStep>10000:
                currentState = np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime * 10000))
                timeStep=timeStep-10000
            currentState = np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime * timeStep))
        else:
            currentState=np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime*timeScale))
        '''