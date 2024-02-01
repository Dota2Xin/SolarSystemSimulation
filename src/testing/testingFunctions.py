import matplotlib.pyplot as plt
from src.numerics.dkdLeapfrogIntegrator import *
from src.numerics.collisionCalculator import *

def testInitialConditionNumerically(solution,initialState,steps, finalTime, relative=True):
    #Calculates the data for our current test
    numericData=[]
    exactData=[]
    timeStep=finalTime/steps
    numericData.append(initialState)
    exactData.append(initialState)
    currentTime=0
    timeData=np.linspace(0,finalTime,steps)
    for i in range(steps-1):
        currentTime=currentTime+timeStep
        passedArray=numericData[-1]
        numericData.append(dkdLeapfrogStep(passedArray,timeStep))
        exactData.append(solution(currentTime))
    #starts by processing it into (x,y) for both sets of data
    plt.figure()
    for j in range(len(initialState)):
        xDataExact=[]
        yDataExact=[]
        xDataNumeric=[]
        yDataNumeric=[]
        for i in range(len(numericData)):
            xDataExact.append(exactData[i][j][0])
            yDataExact.append(exactData[i][j][1])
            xDataNumeric.append(numericData[i][j][0])
            yDataNumeric.append(numericData[i][j][1])
        #plots the data
        plt.subplot(211)
        plt.plot(xDataNumeric,yDataNumeric, label=f"Numeric Data OBJ:{j}")
        plt.plot(xDataExact,yDataExact,label=f"Exact Data OBJ:{j}",linestyle='--')
        plt.legend()
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Trajectories of Exact and Numeric Solutions")
        plt.subplot(212)
        if relative:
            relErrorX=np.abs((np.asarray(xDataExact)-np.asarray(xDataNumeric))/np.asarray(xDataExact))
            relErrorY=np.abs((np.asarray(yDataExact)-np.asarray(yDataNumeric))/np.asarray(yDataExact))
            plt.plot(relErrorX,timeData, label=f"X Error OBJ:{j}")
            plt.plot(relErrorY,timeData,label=f"Y Error OBJ:{j}")
            plt.yscale('log')
            plt.xlabel("Time(s)")
            plt.ylabel("Relative Error")
            plt.title("Relative Error vs Time for Simulation")
            plt.legend()
        else:
            errorX = np.asarray(xDataExact) - np.asarray(xDataNumeric)
            errorY = np.asarray(yDataExact) - np.asarray(yDataNumeric)
            plt.plot(timeData,errorX,  label=f"X Error OBJ:{j}")
            plt.plot(timeData,errorY,  label=f"Y Error OBJ:{j}")
            plt.xlabel("Time(s)")
            plt.ylabel("Error")
            plt.title("Error vs Time for Simulation")
            plt.legend()
    plt.tight_layout()
    plt.show()

def testInitialConditionQualitatively(initialState,steps, finalTime):
    #Calculates the data for our current test
    numericData=[]
    exactData=[]
    timeStep=finalTime/steps
    numericData.append(initialState)
    currentTime=0
    timeData=np.linspace(0,finalTime,steps)
    print("START")
    for i in range(steps-1):
        currentTime=currentTime+timeStep
        passedArray=numericData[-1]
        newState=dkdLeapfrogStep(passedArray,timeStep)
        newState=collisionCalculator(newState)
        numericData.append(newState)

    print("FINISH")
    #starts by processing it into (x,y) for both sets of data
    plt.figure()
    for j in range(len(initialState)):
        xDataNumeric=[]
        yDataNumeric=[]
        for i in range(int(len(numericData)/10)):
            xDataNumeric.append(numericData[i*10][j][0])
            yDataNumeric.append(numericData[i*10][j][1])
        #plots the data
        plt.plot(xDataNumeric,yDataNumeric, label=f"Numeric Data OBJ:{j}")
        plt.legend()
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Trajectories of Exact and Numeric Solutions")
    plt.show()
    return numericData
