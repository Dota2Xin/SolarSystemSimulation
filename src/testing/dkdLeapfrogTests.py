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
    initialCondition=np.asarray([[-1.16888995e+09, -4.66903128e+08,  3.12385808e+07 , 8.80822413e+00,
  -1.17899850e+01, -8.80260733e-02,  1.98850000e+30,  6.96500000e+08],
 [-2.19733536e+10 ,-6.69555314e+10 ,-3.49400678e+09,  3.67155070e+04,
  -1.21325850e+04 ,-4.35748707e+03 , 3.30100000e+23 , 2.44000000e+06],
 [-6.19099934e+10, -9.01978521e+10,  2.30373378e+09 , 2.87675106e+04,
  -1.98050806e+04, -1.93132011e+03,  4.86730000e+24,  6.05184000e+06],
 [-9.87628520e+10,  1.10181304e+11,  2.45354230e+07, -2.25173677e+04,
  -2.06645884e+04 ,-8.38105634e+01,  7.34900000e+22 , 1.73753000e+06],
 [-9.83834078e+10,  1.10314547e+11 , 2.56696661e+07, -2.28693872e+04,
  -1.97615596e+04 , 2.18750101e+00, 5.97219000e+24 , 6.37101000e+06],
 [ 2.19599207e+10 ,-2.15042741e+11, -5.03298472e+09,  2.50116550e+04,
   4.66488620e+03 ,-5.15370321e+02,  6.41710000e+23,  3.38998000e+06],
 [ 4.95422104e+11 , 5.56939094e+11 ,-1.33945255e+10, -9.90564030e+03,
   9.30319447e+03 , 1.83066168e+02,  1.89818722e+27,  6.99110000e+07],
 [ 1.35284073e+12, -5.32423773e+11 ,-4.46055449e+10, 2.99875016e+03,
   8.96831915e+03,-2.74788182e+02,  5.68340000e+26 , 5.82320000e+07],
 [ 1.82012221e+12 , 2.29897204e+12, -1.50416338e+10, -5.38946478e+03,
   3.90985017e+03,  8.43783304e+01 , 8.68130000e+25,  2.53620000e+07],
 [ 4.46400825e+12 ,-2.53730991e+11, -9.76524822e+10 , 2.73209006e+02,
   5.45896961e+03 ,-1.19066372e+02 , 1.02409000e+26,  2.46240000e+07],
 [ 2.58641652e+12, -4.53502888e+12 ,-2.62870924e+11,  4.85902198e+03,
   1.48451968e+03, -1.58546248e+03 , 1.30700000e+22 , 1.18830000e+06]])
    tf.testInitialConditionQualitatively(initialCondition,100000, 311536000.0)