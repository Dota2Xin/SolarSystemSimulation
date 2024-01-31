import pygame as pg
from src.numerics import dkdLeapfrogIntegrator as lf
from GUI.graphicsEngine.engine import graphicsEngine
import numpy as np
import glm

def addObject(name, initialState, engine, currentState, names,textures,lengthScaleFactor, texture='sun'):
    newState=np.concatenate((currentState,np.asarray([initialState])),axis=0)
    textures.append(texture)
    names[name]=len(newState)-1
    engine.addRegularPlanet(initialState[0:3], initialState[-1], name,lengthScaleFactor, textureIndex=len(newState)-1, texture=texture)
    return np.asarray(newState)


