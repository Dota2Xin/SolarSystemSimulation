import testingFunctions as tf
import numpy as np
import matplotlib.pyplot as plt

def testBasic2D():
    initialCondition = np.asarray([[2.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.001, .5], [-2.0,0.0,0.0,1.0,1.0,0.0,0.001,.5]])
    tf.testInitialConditionQualitatively(initialCondition, 1000, 10)

def testSlightlyMore2D():
    initialCondition = np.asarray(
        [[2.0, 0.0, 0.0, -1.0, 1.0, 0.0, 1.0, .5], [-2.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.1, .5], [-4.0,0.0,0.0,0.0,1.0,0.0,.1,.5]])
    tf.testInitialConditionQualitatively(initialCondition, 1000, 10)