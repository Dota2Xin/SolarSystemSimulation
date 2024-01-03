import pygame
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np

def main():
    #Initialize this to solar system
    #Dictionary that contains the full state of the solar system, references to physical data, as well as graphics data
    currentState={}

    #Initialize window
    engine=graphicsEngine()

    run=True
    while run:
        currentTime=pygame.time.get_ticks()*.001
        engine.updatePosition([np.sin(currentTime),0.0,0.0])
        engine.render()
        engine.clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
    engine.scene.destroy()
    pygame.quit()

if __name__=='__main__':
    main()