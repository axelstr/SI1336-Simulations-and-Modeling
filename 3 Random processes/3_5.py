# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.5

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl

# ------------------------- global variables

# Total number of particles
nTotArray = [8,64,800]

# Number of steps
# nSteps = 1000
nStepsDict = {
8:      1000,
64:     10000,
800:    100000
}

# Number of simulations for each n
# nSimulations = 10000
nSimulations = 10000

# Seed the random generator
rnd.seed()

# storage
leftDict = {}
endLeftDict = {}
stepDict = {}

# functions
def mean(array):
    """This function returns the mean of an array of floats."""
    sum = 0
    for x in array: sum += x
    return sum/len(array)

# ---------------------------- calculation
for nTot in nTotArray:
    stepArray = [ ]
    leftArray = [ ]
    endLeftArray = [ ]
    for simulation in range(nSimulations):
        nLeft = nTot/2
        nRight = 0
        nSteps = nStepsDict[nTot]
        oddEvenEnding = round(rnd.random())
        for step in range(0,nSteps-oddEvenEnding):
            if simulation == 0:
                stepArray.append(step)
                leftArray.append(nLeft)
            p = nLeft/nTot
            r = rnd.random()
            if r < p:
                nLeft -= 1
                nRight += 1
            elif r >= p:
                nLeft += 1
                nRight -= 1
        endLeftArray.append(nLeft)
        if simulation == 0:
            leftDict[nTot] = leftArray
            stepDict[nTot] = stepArray
    endLeftDict[nTot] = endLeftArray

# ------------------------- print of values

print('\nEnd values:\n')
for nTot in nTotArray:
    print(nTot, '\t', mean(endLeftDict[nTot]))
print('\nAround equilibrium:\n')
for nTot in nTotArray:
    print(nTot, '\t', mean(leftDict[nTot]))
