import pygame as pg
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np
import glm
import controlEntities
from GUI import solarSystemData


def main():
    #Params
    timeScale=1.0 #describes the correspondence between real time and sim time

    #Initialize this to solar system
    #describes the current state numerically
    currentState=np.asarray([[-1.0,0.0,0.0,.0000913393398,.0001582044,0.0,1000,.5],[1.0,0.0,0.0,.0000913393398,-.0001582044,0.0,1000,.5], [0.0,-1.732,0.0,-.00018267868,0.0,0.0,1000,.5]])
    names = {"Sphere1": 0, "Sphere2":1, "Sphere3":2}

    #currentState, names= solarSystemData.getSolarSystemData()
    #print(currentState)
    #Dictionary that contains the full state of the solar system, references to physical data, as well as graphics data
    mathematicalPositions=[]
    cameraPos=[currentState[0][0],currentState[0][1],currentState[0][2]]
    graphicsSettings={"cameraSpeed": .01, "cameraSensitivity": .05, "cameraFrustumParams": [cameraPos,glm.vec3(0), [0.0,1.0,.5]]}
    #Initialize window
    engine=graphicsEngine(graphicsSettings,names, currentState)
    deltaTime=engine.clock.tick(60)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    run=True
    objCount=len(currentState)
    while run:
        currentState=np.asarray(lf.dkdLeapfrogStep(currentState, deltaTime*timeScale))
        engine.updatePositions(names,currentState)
        engine.render()
        engine.camera.update(deltaTime)
        deltaTime=engine.clock.tick(60)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
            elif event.type==pg.KEYUP:
                if event.key==pg.K_i:
                    currentPos=engine.camera.position+engine.camera.forward
                    objCount = objCount+1
                    currentState=controlEntities.addObject(f"Sphere{objCount}", [currentPos[0], currentPos[1], currentPos[2], 0.0,0.0,0.0,1000,1.0], engine, currentState, names)
                if event.key==pg.K_y:
                    print(engine.camera.position)

    engine.destroy()
    pg.quit()

if __name__=='__main__':
    main()