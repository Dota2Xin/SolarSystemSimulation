import testingFunctions as tf
import numpy as np
import matplotlib.pyplot as plt
#This file contains all the tests for the dkdLeapfrogIntegrator method
#let R=0 for tests unless otherwise specified

#tests a particle starting at (0,0,0) with velocity (1,0,0) with mass=1
def testLinearSolutionFunc(currentTime):
    position=np.asarray([currentTime,0,0])
    velocity=np.asarray([1,0,0])
    return [[currentTime,0.0,0.0,1.0,0.0,0.0,1.0,0.0]]

def testLinear():
    position = np.asarray([0, 0, 0])
    velocity = np.asarray([1, 0, 0])
    initialCondition=np.asarray([[0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0]])
    tf.testInitialConditionNumerically(testLinearSolutionFunc, initialCondition,1000,10,relative=False)


#tests two particles in a circular orbit where particle 1 starts at (10,0,0) with velocity (0,-8.16963891*(10**-4),0) and particle 2 is at (-10,0,0) with opposite velocity
#Masses=10^5 for both
def testCircularSolutionFunc(currentTime):
    omega=(4.08481946*(10**-4))/10.0
    x=10.0*np.cos(omega*currentTime)
    y=10.0*np.sin(omega*currentTime)
    velocityY=(4.08481946*(10**-4))*np.cos(omega*currentTime)
    velocityX=(4.08481946*(10**-4))*np.sin(omega*currentTime)
    return [[x,-y,0,velocityX,-velocityY,0,10**5,0],[-x,y,0,-velocityX,velocityY,0,10**5,0]]

def testCircular():
    initialCondition=np.asarray([[10.0,0.0,0.0,0.0,-4.08481946*(10.0**-4.0),0.0,10.0**5.0,0.0],[-10.0,0.0,0.0,0.0,4.08481946*(10.0**-4.0),0.0,10.0**5.0,0.0]])
    tf.testInitialConditionNumerically(testCircularSolutionFunc,initialCondition,1000000,10000000,relative=False)


#####################Qualitative Tests################################

#first test plugs in Earth Sun and Moon and runs it for ten years:

def testEarthMoonSun():
    earthCond=[147.095*(10.0**9.0),0.0,0.0,0.0,30.29*1000,0.0,5.9724 * (10.0 ** 24.0),1000]
    moonCond=[147.4583*(10.0**9.0),0.0,0.0,0.0,31.372*1000,0.0,.07346*(10.0**24.0),100]
    sunCond=[0.0,0.0,0.0,0.0,0.0,0.0,1988500.0*(10.0**24.0),0.0]
    initialCondition=np.asarray([earthCond,moonCond,sunCond])
    numericData=tf.testInitialConditionQualitatively(initialCondition,1000000,311536000.0)

    moonYwrtEarth=[]
    moonXwrtEarth=[]
    for i in range(len(numericData)):
        moonXwrtEarth.append(numericData[i][1][0]-numericData[i][0][0])
        moonYwrtEarth.append(numericData[i][1][1] - numericData[i][0][1])
    plt.plot(moonXwrtEarth,moonYwrtEarth)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Moon's Trajectory With Respect to Earth")
    plt.show()

