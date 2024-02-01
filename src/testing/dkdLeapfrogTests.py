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

def testEarthJupiterSun():
    earthCond = [147.095 * (10.0 ** 9.0), 0.0, 0.0, 0.0, 30.29 * 1000, 0.0, 5.9724 * (10.0 ** 24.0), 1000]
    jupiterCond = [740.595 * (10.0 ** 9.0), 0.0, 0.0, 0.0, 13.72 * 1000, 0.0, 1898.13 * (10.0 ** 24.0), 1000]
    sunCond = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1988500.0 * (10.0 ** 24.0), 0.0]
    initialCondition = np.asarray([earthCond, jupiterCond, sunCond])
    tf.testInitialConditionQualitatively(initialCondition, 1000000, 311536000.0)

def testSolarSystem():
    initialCondition=np.asarray([[-1.16965046e+09, -4.65883915e+08,  3.12461702e+07 , 8.79617818e+00,
  -1.18029206e+01, -8.76556358e-02,  1.98850000e+30 , 6.96500000e+09],
 [-2.51136394e+10 ,-6.58106673e+10, -3.11255401e+09 , 3.59580825e+04,
  -1.43639219e+04 ,-4.47036096e+03 , 3.30200000e+23,  2.44000000e+07],
 [-6.43715465e+10, -8.84519963e+10 , 2.46969385e+09,  2.82091382e+04,
  -2.06057019e+04 ,-1.91009693e+03 , 4.86850000e+24, 6.05184000e+07],
 [-9.67935825e+10 , 1.11952002e+11 , 3.17469820e+07 ,-2.30676521e+04,
  -2.03156090e+04 ,-8.24754064e+01 , 7.34900000e+22, 1.73753000e+07],
 [-9.63926605e+10 , 1.12004687e+11 , 2.54818939e+07, -2.32115466e+04,
  -1.93611059e+04 , 2.15103945e+00 , 5.97219000e+29,  6.37101000e+07],
 [ 1.97978116e+10, -2.15435224e+11 ,-4.98820831e+09,  2.50367470e+04,
   4.42037865e+03 ,-5.21109814e+02,  6.41710000e+27 , 3.38998000e+07],
 [ 4.96277444e+11 , 5.56134682e+11, -1.34103237e+10 ,-9.89363756e+03,
   9.31859478e+03,  1.82677939e+02,  1.89818722e+27 , 6.99110000e+08],
 [ 1.35258144e+12 ,-5.33198549e+11, -4.45817987e+10 , 3.00330337e+03,
   8.96632817e+03 ,-2.74902622e+02,  5.68340000e+26 , 5.82320000e+08],
 [ 1.82058782e+12,  2.29863419e+12 ,-1.50489175e+10 ,-5.38868988e+03,
   3.91088171e+03,  8.41768200e+01 , 8.68130000e+25 , 2.53620000e+08],
 [ 4.46398462e+12, -2.54202644e+11, -9.76421916e+10 , 2.73863303e+02,
   5.45894062e+03, -1.19142544e+02,  1.02409000e+26 , 2.46240000e+08],
 [ 2.58599596e+12, -4.53515777e+12 ,-2.62733693e+11 , 4.87531258e+03,
   1.50026430e+03 ,-1.58770780e+03,  1.30700000e+22 , 1.18830000e+07]])
    tf.testInitialConditionQualitatively(initialCondition,50000,500)