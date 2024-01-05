import pygame as pg
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np
import glm

def addObject(name, initialState, engine, currentState, names):
    currentState.append(initialState)
    names[name]=len(currentState)-1
    engine.addRegularPlanet(initialState[0:3], initialState[-1], name)


