import numpy as np
from numba import njit
from numba import jit

#checks if there is a collision happening
@njit
def detectCollisions(state):
    collisionArray=[]
    for i in range(len(state)):
        for j in range(len(state)):
            if i != j:
                positionDifference = state[j][:3] - state[i][:3]
                posMagnitude = np.linalg.norm(positionDifference)
                if posMagnitude < (state[j][-1] + state[i][-1]):
                    alreadySeen=False
                    for collision in collisionArray:
                        if collision==(i,j) or collision==(j,i):
                            alreadySeen=True
                    if not alreadySeen:
                        collisionArray.append((i,j))
    return collisionArray

#calculates the effect of a collision
@njit
def collisionCalculator(state):
    '''
    params:
        state=State is formatted as an array with [[x,y,z, vx,vy,vz, mass, radius],...,...,...]
    return:
        updatedState= Same format as state but with updated values to reflect collisions
    '''
    updatedState=np.copy(state)
    collisionArray=detectCollisions(state)
    for collision in collisionArray:
        posDifference=state[collision[0]][0:3]-state[collision[1]][0:3]
        velDifference=state[collision[0]][3:6]-state[collision[1]][3:6]
        storeVel1=state[collision[0]][3:6]
        storeVel2=state[collision[1]][3:6]
        m1=state[collision[0]][-2]
        m2=state[collision[1]][-2]
        updatedState[collision[0]][3:6]=storeVel1-2*m2*np.dot(posDifference, velDifference)*posDifference/((m2+m1)*(np.linalg.norm(posDifference)**2))
        updatedState[collision[1]][3:6] = storeVel2+ 2 * m1 * np.dot(posDifference, velDifference) * posDifference / ((m2 + m1) * (np.linalg.norm(posDifference) ** 2))

    return updatedState

