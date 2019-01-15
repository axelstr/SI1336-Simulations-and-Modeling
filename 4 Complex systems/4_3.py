# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 4.3

# -------------------- Import libraries

import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import os
from scipy.optimize import curve_fit

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

# iteration for positions vs time, nCars = 10

roadLength = 100
vMaxArray = [1,2,5]
pBrake = 0.5
tStop = 300      # stop calculating at this time
nCars = 20
tArray = [t for t in range(1,tStop+1)]

carPositionsDictArray = []  # storing lists in dicts in a list

for vMax in vMaxArray:

    carPositions = [x for x in range(nCars)]
    carVelocities = [0 for x in range(nCars)]
    t = 0
    carPositionsDict = {}       # keys are t in tArray

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
            if rnd.random() <= pBrake:
                if carVelocities[i] > 0:
                    carVelocities[i] -= 1

        # move cars forwards, the road is a circle
        for i in range(nCars):
            carPositions[i] += carVelocities[i]
            carPositions[i] %= roadLength

        # store data
        carPositionsDict[t] = carPositions[:]
    carPositionsDictArray.append(carPositionsDict)


# calculate flow rate for fundamental diagram

# variables

roadLength = 100
vMaxArray = [1,2,5]
densityArray = [0.04, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
pBrake = 0.5
tStop = 300      # stop calculating at this time
nCars = 20
tArray = [t for t in range(1,tStop+1)]
nSimulations = 100      # number of simulations for each nCars

## storage

flowrateDict = {}       # keys are items in roadLengthArray

for vMax in vMaxArray:
    print(vMax)
    flowrateArray = []      # will contain (nCars number of) arrays (of length nSimulations) corresponding to densityArray

    for density in densityArray:
        print(density)
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
    flowrateDict[vMax] = flowrateArray[:]


# -------------------- Plot


fig = plt.figure()

# positions vs time

colors = pl.cm.jet(np.linspace(0.1,0.9,20))
commonMarker = '.'
commonMarkersize = 2

for i in range(len(vMaxArray)):
    vMax = vMaxArray[i]
    carPositionsDict = carPositionsDictArray[i]
    plt.clf()
    plt.title(r'Cellular automaton traffic model with with $v_{max} = %d$ .'%(vMax))
    plt.xlabel(r'Time')
    plt.ylabel(r'Car positions')
    for j in range(len(tArray)):
        t = tArray[j]
        carPositions = carPositionsDict[t]
        for k in range(len(carPositions)):
            plt.plot(t, carPositions[k],
                marker = commonMarker,
                markersize = commonMarkersize,
                color = colors[k]
            )
    filename = 'assets3/positionsplot%d.png'%(i)
    plt.savefig(filename, dpi = 300)
    # os.startfile(filename.replace('/','\\'))

# boxplot of flow rate

plt.clf()
for i in range(len(vMaxArray)):
    vMax = vMaxArray[i]
    flowrateArray = flowrateDict[vMax]

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
    plt.title('Fundamental diagram for cellular automaton traffic model.\n $v_{max} = %d$'%(vMax))
    plt.axis([-0.05, 1.05, -0.05, 0.5])
    plt.ylabel(r'flow rate at t = %d' % (tStop))
    plt.xlabel(r'density = $n_{cars} / L$')

    filename = 'assets3/boxplot%d.png'%(i)
    plt.savefig(filename, dpi = 300)
    # os.startfile(filename.replace('/','\\'))
    plt.clf()
