# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 4.2

# -------------------- Import libraries

import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from scipy.optimize import curve_fit
import os

rnd.seed(0)

# -------------------- Define functions

def getFlowrate(carVelocities, roadLength):
    """Takes array carVelocities and float or int roadLength. Returns the
    flowrate as the sum of all values in carVelocities devided by roadLength."""
    sum = 0
    for velocity in carVelocities:
        sum += velocity
    flowrate = sum/roadLength
    return flowrate

def randomizeCarPositions(nCars, roadLength):
    """This function takes integers nCars and roadLength. It then returns a
    sorted array of unique random integers from 0 to roadLength-1. The array is
    of length nCars."""
    carPositions = [x for x in range(roadLength)]
    while len(carPositions) > nCars:
        randomIndex = int(len(carPositions)*rnd.random()) % len(carPositions)
        del carPositions[randomIndex]
    return carPositions

def randomizeCarVelocities(nCars, vMax):
    """This function takes integers nCars, and vMax. It then returns an array
    of of random integers from 0 to vMax. The array is of length nCars.
    No integers in the returned array are the same."""
    carVelocities = []
    for i in range(nCars):
        randomVelocity = int((vMax+1)*rnd.random()) % (vMax+1)
        carVelocities.append(randomVelocity)
    return carVelocities


# -------------------- Calculation

# calculate flow rate for fundamental diagram

## variables

densityArray = [0.04, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
roadLengthArray = [50, 150, 300, 500]
nSimulations = 100      # number of simulations for each nCars
vMax = 2
pBrake = 0.5
tStop = 100             # calculate flowrate at this time, after initial transition

## storage

flowrateDict = {}       # keys are items in roadLengthArray

for roadLength in roadLengthArray:
    flowrateArray = []      # will contain (nCars number of) arrays (of length nSimulations) corresponding to densityArray
    print('Currently working on roadLength = %d'%(roadLength))
    for density in densityArray:
        nCars = int(density * roadLength)
        flowrateArray_nCars = []
        for simulation in range(nSimulations):
            t = 0
            carPositions = randomizeCarPositions(nCars, roadLength)
            carVelocities = randomizeCarVelocities(nCars, vMax)
            while t < tStop:
                t += 1
                # accelerate on step towards max speed
                for i in range(nCars):
                    if carVelocities[i] < vMax:
                        carVelocities[i] += 1
                # brake if close to next car
                for i in range(nCars):
                    distance = (carPositions[(i+1)%nCars] - carPositions[i]) % roadLength
                    if carVelocities[i] >= distance:
                        carVelocities[i] = distance - 1
                # random braking
                for i in range(nCars):
                    if rnd.random() <= pBrake and carVelocities[i] > 0 :
                        if carVelocities[i] > 0:
                            carVelocities[i] -= 1
                # move cars forwards, the road is a circle
                for i in range(nCars):
                    carPositions[i] += carVelocities[i]
                    carPositions[i] %= roadLength
                # store data
            flowrateArray_nCars.append(getFlowrate(carVelocities, roadLength))
        flowrateArray.append(flowrateArray_nCars[:])
    flowrateDict[roadLength] = flowrateArray[:]


# plot

for i in range(len(roadLengthArray)):
    roadLength = roadLengthArray[i]
    flowrateArray = flowrateDict[roadLength]

    # regression
    def fFitted(x,a,b,c):
        return (a * (x**b)) * np.exp(-c*x)

    meanFlowrateArray = [np.mean(array) for array in flowrateArray]

    popt, pcov = curve_fit(fFitted, densityArray, meanFlowrateArray)
    a = popt[0]
    b = popt[1]
    c = popt[2]
    aRounded = round(a,2)
    bRounded = round(b,2)
    cRounded = round(c,2)

    xArray = np.linspace(min(densityArray), max(densityArray), 1001)
    plt.plot(xArray, [fFitted(x, a,b,c) for x in xArray],
            color = 'r',
            zorder = 2)
    plt.legend([
            r'$f(x) =  %s \, x^{%s} \, e^{- %s \, x }$'%(aRounded,bRounded,cRounded)
            ],
            fancybox = True,
            shadow = True)

    # boxplot
    plt.boxplot(flowrateArray, positions = densityArray,
            patch_artist = True,
            widths = 0.1,
            zorder = 1)
    plt.title('Fundamental diagram for cellular automaton traffic model.\n $L = %d$'%(roadLength))
    plt.axis([-0.05, 1.05, -0.05, 0.5])
    plt.ylabel(r'flow rate at t = %d' % (tStop))
    plt.xlabel(r'density = $n_{cars} / L$')

    filename = 'assets2/boxplot%d.png'%(i)
    plt.savefig(filename, dpi = 300)
    # os.startfile(filename.replace('/','\\'))
    plt.clf()
