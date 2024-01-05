import pygame as pg
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np
import glm
import controlEntities





def main():
    #Initialize this to solar system
    #describes the current state numerically
    currentState=[[0.0,0.0,0.0,0.0,0.0,0.0,1000,1.0],[0.0,1.0,0.0,0.0,0.0,0.0,1000,1.0], [0.0,-1.0,0.0,0.0,0.0,0.0,1000,1.0]]
    names = {"Sphere1": 0, "Sphere2":1, "Sphere3":2}
    #Dictionary that contains the full state of the solar system, references to physical data, as well as graphics data
    mathematicalPositions=[]

    graphicsSettings={"cameraSpeed": .01, "cameraSensitivity": .05, "cameraFrustumParams": [[0,0,1],glm.vec3(0), [0.0,1.0,.5]]}
    #Initialize window
    engine=graphicsEngine(graphicsSettings,names, currentState)
    deltaTime=engine.clock.tick(60)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    run=True
    objCount=len(currentState)
    count=0
    while run:
        count+=1
        if count==300:
            print("LOLS)")
        currentTime=pg.time.get_ticks()*.001
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
                    controlEntities.addObject(f"Sphere{objCount}", [currentPos[0], currentPos[1], currentPos[2], 0.0,0.0,0.0,1000,1.0], engine, currentState, names)

    engine.destroy()
    pg.quit()

if __name__=='__main__':
    main()