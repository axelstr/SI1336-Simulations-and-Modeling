# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.10

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
stepsArray = [step for step in range(1,41,1)]  # step range to examine
simulations = 10000                             # simulations for each step range

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

def improvedRandomStep(x,y):
    """This function takes integer x and y arrays of same length and returns new x and y arrays with a
    new, random step taken at the end of the arrays. It only takes steps left,
    forwards or right in relation to the current direction, thus it never walks
    back into itself. If the current walk length is zero a random step is taken
    in any of the four directions."""
    if len(x) == 1: return randomStep(x,y)
    a = x[-1]-x[-2]
    b = y[-1]-y[-2]
    currentDirection    = [a,b]
    leftDirection       = [-b,a]
    rightDirection      = [b,-a]
    directions = {
        0:  leftDirection,
        1:  currentDirection,
        2:  rightDirection,
    }
    direction = directions[int(3*rnd.random())]
    x.append(x[-1]+direction[0])
    y.append(y[-1]+direction[1])
    return x,y


# ---------------------- Calculate

# storage

meanRSquaredArray_normal = []       # stores mean(R^2) corresponding to step range in stepsArray
meanRSquaredArray_avoiding = []     # stores mean(R^2) corresponding to step range in stepsArray

# noraml loop

for steps in stepsArray:
    rEndSquaredArray = []
    for simulation in range(simulations):
        x = [0]
        y = [0]
        for step in range(int(steps)):
            x,y = randomStep(x,y)
        rEndSquaredArray.append(x[-1]**2+y[-1]**2)
    meanRSquaredArray_normal.append(mean(rEndSquaredArray))

for steps in stepsArray:
    rEndSquaredArray = []
    print(steps)
    for simulations in range(simulations):
        step = 0
        x = [0]
        y = [0]
        while step < steps:
            step += 1
            x,y = improvedRandomStep(x,y)
            xEnd, yEnd = x[-1], y[-1]
            for j in range(len(x)-1):
                if xEnd == x[j] and yEnd == y[j]:
                    # print('breaking', x,y)
                    step,x,y = 0,[0],[0]
                    break
        rEndSquaredArray.append(x[-1]**2+y[-1]**2)
    meanRSquaredArray_avoiding.append(mean(rEndSquaredArray))

meanRSquaredArray_normal_logged = [np.log(x) for x in meanRSquaredArray_normal]
meanRSquaredArray_avoiding_logged = [np.log(x) for x in meanRSquaredArray_avoiding]
stepsArray_logged = [np.log(x) for x in stepsArray]

def fLinear_normal(x,k,m):
    return k*x+m
def fLinear_avoiding(x,k,m):
    return k*x+m

popt, pcov = curve_fit(fLinear_normal, stepsArray_logged, meanRSquaredArray_normal_logged)
k_normal = popt[0]
m_normal = popt[1]

popt, pcov = curve_fit(fLinear_normal, stepsArray_logged, meanRSquaredArray_avoiding_logged)
k_avoiding = popt[0]
m_avoiding = popt[1]

# --------------------- Plot


colors = pl.cm.plasma([0.1,0.8])                # succes rate
colors2 = pl.cm.plasma([0.3,0.6])               # regression
# print(colors)

commonLinewidth = 1

# plot proportional

plt.plot(stepsArray, meanRSquaredArray_normal,
    color = colors[0],
    linewidth = commonLinewidth)
plt.plot(stepsArray, meanRSquaredArray_avoiding,
    color = colors[1],
    linewidth = commonLinewidth)
plt.title(r'$\langle R^2 \rangle$ vs $n_{steps}$' + '\n' + r'for random and random, self-avoiding walks')
plt.xlabel(r'$n_{steps}$')
plt.ylabel(r'$\langle R^2 \rangle$')
plt.legend([
    r'normal',
    r'self-avoiding'
    ],
    fancybox = True,
    shadow = True)
# plt.axis('equal')
plt.savefig('assets10/linear_plot.png', dpi = 300)
# plt.show()

# plot logerithmized
plt.clf()
plt.plot(stepsArray_logged, meanRSquaredArray_normal_logged,
    color = colors[0],
    linewidth = commonLinewidth)
plt.plot(stepsArray_logged, [fLinear_normal(x,k_normal,m_normal) for x in stepsArray_logged],
    color = colors2[0],
    linewidth = commonLinewidth,
    linestyle = '--')
plt.plot(stepsArray_logged, meanRSquaredArray_avoiding_logged,
    color = colors[1],
    linewidth = commonLinewidth)
plt.plot(stepsArray_logged, [fLinear_avoiding(x,k_avoiding,m_avoiding) for x in stepsArray_logged],
    color = colors2[1],
    linewidth = commonLinewidth,
    linestyle = '--')
plt.title(r'loglog-plot of $\langle R^2 \rangle$ vs $n_{steps}$' + '\n' + r'for random and random, self-avoiding walks')
plt.legend([
    r'normal',
    r'$\ln \, \langle R^2 \rangle = %f \cdot \ln \, n_{steps} + (%f)$' % (k_normal, m_normal),
    r'self-avoiding',
    r'$\ln \, \langle R^2 \rangle = %f \cdot \ln \, n_{steps} + (%f)$' % (k_avoiding, m_avoiding)
    ],
    fancybox = True,
    shadow = True)
plt.xlabel(r'$\ln \, n_{steps}$')
plt.ylabel(r'$\ln \, \langle R^2 \rangle$')
# plt.axis('equal')
plt.savefig('assets10/log_plot.png', dpi = 300)
# plt.show()
