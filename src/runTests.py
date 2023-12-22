import numpy as np
import matplotlib.pyplot as plt
from dkdLeapfrogIntegrator import *

def testInitialConditionNumerically(solution,initialState,steps, finalTime):
    #Calculates the data for our current test
    numericData=[]
    exactData=[]
    timeStep=finalTime/steps
    numericData.append(initialState)
    exactData.append(initialState)
    currentTime=0
    for i in range(steps-1):
        currentTime=currentTime+timeStep
        numericData.append(dkdLeapfrogStep(numericData[-1],timeStep))
        exactData.append(solution(currentTime))
    #Plots the data
