import pygame as pg
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np
import glm


def main():
    #Initialize this to solar system
    #Dictionary that contains the full state of the solar system, references to physical data, as well as graphics data
    currentState={}

    graphicsSettings={"cameraSpeed": .01, "cameraSensitivity": .05, "cameraFrustumParams": [[0,0,1],glm.vec3(0), [0.0,1.0,.5]]}
    #Initialize window
    engine=graphicsEngine(graphicsSettings)
    deltaTime=engine.clock.tick(60)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    run=True
    while run:

        currentTime=pg.time.get_ticks()*.001
        engine.updatePosition([0.0,0.0,0.0])
        engine.render()
        engine.camera.update(deltaTime)
        deltaTime=engine.clock.tick(60)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
    engine.scene.destroy()
    pg.quit()

if __name__=='__main__':
    main()