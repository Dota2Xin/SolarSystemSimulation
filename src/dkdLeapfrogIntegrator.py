import numpy as np
from numba import njit

#State is formatted as an array with [numpy array of position, numpy array of velocities, mass, radius]
@njit
def dkdLeapfrogStep(state, timeStep):
    updatedState=np.asarray([])
    G=6.67430*(10**-11)
    for i in range(len(state)):
        updatedState.append(np.asarray([0,0,0],[0,0,0],state[i][2],state[i][3]))
        halfPosition=state[i][0]+state[i][1]*(timeStep/2.0)
        a=[0,0,0]
        for j in range(len(state)):
            if i!=j:
                positionDifference=(state[j][0]-state[i][0])
                b=.01*(min(state[i][3],state[j][3]))
                r=np.sum(positionDifference**2)**.5
                a=a+G*state[j][2]*positionDifference/((r+b)**3)
        updatedState[i][1]=state[i][1]+timeStep*a
        updatedState[i][0]=halfPosition+(timeStep/2.0)*updatedState[i][1]
    return updatedState