# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.8


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl
from scipy.optimize import curve_fit

# ------------------- global

# Seed the random generator
rnd.seed()

# Values
stepsArray = [step for step in range(1,1000, 10)]  # step range to examine
stepsArray.append(1000)
simulations = 1000                # simulations for each step range

# Functions
def mean(array):
    """This function returns the mean of an array of floats."""
    sum = 0
    for x in array: sum += x
    return sum/len(array)

def randomStep(x,y):
    """This function takes x and y arrays and returns new x and y arrays with a
    new, random step taken at the end of the arrays."""
    directions = {
        0:  [1,0],
        1:  [0,1],
        2:  [-1,0],
        3:  [0,-1]
    }
    direction = directions[int(4*rnd.random())]
    x.append(x[-1]+direction[0])
    y.append(y[-1]+direction[1])
    return x,y


# ---------------------- Calculate

# storage
meanRSquaredArray = []  # stores mean(R^2) corresponding to step range in stepsArray

# loop
for steps in stepsArray:
    rEndSquaredArray = []
    for simulation in range(simulations):
        x = [0]
        y = [0]
        for step in range(int(steps)):
            x,y = randomStep(x,y)
        rEndSquaredArray.append(x[-1]**2+y[-1]**2)
    meanRSquaredArray.append(mean(rEndSquaredArray))

def fLinear(x,k):
    return k*x

popt, pcov = curve_fit(fLinear, stepsArray, meanRSquaredArray)
k = popt[0]
std = np.sqrt(pcov[0][0])

# --------------------- Plot

colors = pl.cm.jet([0.25,0.8])
commonLinewidth = 1

plt.plot(stepsArray, meanRSquaredArray,
    color = colors[0],
    linewidth = commonLinewidth)
plt.plot(stepsArray, [k*step for step in stepsArray],
    color = colors[1],
    linewidth = commonLinewidth)
plt.xlabel(r'$n_{steps}$')
plt.ylabel(r'$\langle R^2 \rangle$')
plt.legend([r'$\langle R^2 \rangle$',r'linear fit'])
plt.title(r'$\langle R^2 \rangle$ for walks with $n_{steps} \in [1,1000]$'+'\n' \
    + r'Linear fit: $\langle R^2 \rangle = %f \cdot n_{steps}, \quad \sigma = %f$' %(round(k,10),round(std,10)))
plt.savefig('assets8/plot.png', dpi = 300)
plt.show()
