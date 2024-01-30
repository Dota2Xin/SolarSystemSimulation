import numpy as np
from numba import njit
from numba import jit

@njit
def dkdLeapfrogStep(state):
    '''
    params:
        state=State is formatted as an array with [[x,y,z, vx,vy,vz, mass, radius],...,...,...]
    return:
        updatedState= Same format as state but with updated values to reflect collisions
    '''
    updatedState = np.zeros_like(state)
    return updatedState

