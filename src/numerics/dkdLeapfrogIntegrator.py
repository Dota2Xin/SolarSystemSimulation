import numpy as np
from numba import njit
from numba import jit

#State is formatted as an array with [[x,y,z, vx,vy,vz, mass, radius],...,...,...]
@njit
def dkdLeapfrogStep(state, timeStep):
    updatedState = np.zeros_like(state)
    G = 6.67430 * (10**-11)

    for i in range(len(state)):
        updatedState[i][0:] = state[i][0:]
        halfPosition = state[i][:3] + state[i][3:6] * (timeStep / 2.0)
        a = np.zeros(3)

        for j in range(len(state)):
            if i != j:
                positionDifference = state[j][:3] - state[i][:3]
                b = 0.01 * min(state[i][3], state[j][3])
                r = np.sqrt(np.sum(positionDifference**2))
                a += G * state[j][6] * positionDifference / ((r + b)**3)

        newVelocities = state[i][3:6] + timeStep * a
        newPositions = halfPosition + (timeStep / 2.0) * newVelocities

        updatedState[i][3:6] = newVelocities
        updatedState[i][:3] = newPositions

    return updatedState

'''
@njit
def dkdLeapfrogStep(state, timeStep):
    updatedState=[]
    G=6.67430*(10**-11)
    for i in range(len(state)):
        updatedState.append([0.0,0.0,0.0,0.0,0.0,0.0,state[i][2],state[i][3]])
        halfPosition=[state[i][0]+state[i][3]*(timeStep/2.0),state[i][1]+state[i][4]*(timeStep/2.0),state[i][2]+state[i][5]*(timeStep/2.0)]
        a=[0.0,0.0,0.0]
        for j in range(len(state)):
            if i!=j:
                positionDifference=[(state[j][0]-state[i][0]),(state[j][1]-state[i][1]),(state[j][2]-state[i][2])]
                b=.01*(min(state[i][3],state[j][3]))
                r=(positionDifference[0]**2+positionDifference[1]**2+positionDifference[2]**2)**.5

                a=[a[0]+G*state[j][2]*positionDifference[0]/((r+b)**3),a[1]+G*state[j][2]*positionDifference[1]/((r+b)**3),a[2]+G*state[j][2]*positionDifference[2]/((r+b)**3)]
        newVelocities=[state[i][3]+timeStep*a[0],state[i][4]+timeStep*a[1],state[i][5]+timeStep*a[2]]
        newPositions=[halfPosition[0]+(timeStep/2.0)*newVelocities[0],halfPosition[1]+(timeStep/2.0)*newVelocities[1],halfPosition[2]+(timeStep/2.0)*newVelocities[2]]
        updatedState[i][3]=newVelocities[0]
        updatedState[i][4] =newVelocities[1]
        updatedState[i][5] =newVelocities[2]
        updatedState[i][0]=newPositions[0]
        updatedState[i][1] = newPositions[1]
        updatedState[i][2] = newPositions[2]

    return updatedState
'''