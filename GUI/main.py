import pygame
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine

def main():
    #Initialize this to solar system
    #Dictionary that contains the full state of the solar system, references to physical data, as well as graphics data
    currentState={}

    #Initialize window
    engine=graphicsEngine()

    run=True
    while run:
        for event in pygame.event.get():
            engine.render()
            engine.clock.tick(60)
            if event.type==pygame.QUIT:
                run=False
    pygame.quit()

if __name__=='__main__':
    main()