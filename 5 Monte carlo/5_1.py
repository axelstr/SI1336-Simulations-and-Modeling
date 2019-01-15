# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 5.1

# ---------------------- Import libraries

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl

# ---------------------- Define variables

x_0 = 1     # initial trial point
delta = 10   # size of delta interval
deltaArray = np.linspace(0.0001,0.1,10001)
pointsToGenerate = 10000      # generated points
pointsToThrow = 100          # skip initial point to approach the target distribution

# ---------------------- Define functions

def f(x):
    return x

def P(x):
    return np.exp(-x)


def mean(inputArray):
    sum = 0
    N = len(inputArray)
    for f in inputArray:
        sum += f
    return sum/N

def getSigma(inputArray):
    return (mean([x**2 for x in inputArray]) - (mean(inputArray))**2)**(1/2)

# ---------------------- Algorithm

# storage
mean_fArray = []    # korresponding to deltaArray
sigma_f_through_nArray = [] # korresponding to deltaArray

# loop
for delta in deltaArray:
    xArray = [ ]
    x_old = x_0
    generatedPoints = - pointsToThrow
    while generatedPoints < pointsToGenerate:
        delta_i = (2*rnd.random()-1) * delta
        # print(delta_i)
        x_new = x_old + delta_i
        w = f(x_new)/f(x_old)
        r = rnd.random()
        # print(x_new)
        if w > r:
            x_old = x_new
            if generatedPoints >= 0:
                # print(x_new)
                xArray.append(x_new)
        else:
            x_new = x_old
            if generatedPoints >= 0:
                xArray.append(x_new)
        generatedPoints += 1
    fArray = [f(x) for x in xArray]
    mean_f = mean(fArray)
    # print(fArray)
    sigma_f = getSigma(fArray)

    # store
    mean_fArray.append(mean_f)
    sigma_f_through_nArray.append(sigma_f/len(fArray))


commonLinewidth = 0.2
colorBlue = pl.cm.jet(0.1)
colorRed = pl.cm.jet(0.9)

plt.subplot(2,1,1)
plt.plot(deltaArray, mean_fArray,
        linewidth = commonLinewidth,
        color = colorBlue)
plt.plot([deltaArray[0], deltaArray[-1]], [1, 1],
        linewidth = commonLinewidth,
        color = colorRed,
        linestyle = '--')
plt.title(r'Calculating $\langle x \rangle = \frac{\int_0^\infty x e^{-x} \, dx}{\int_0^\infty e^{-x} \, dx}$ using the metropolis method.'+'\n')
plt.ylabel(r'$\langle x \rangle$')
plt.legend([
        r'numerical',
        r'analytical'],
        loc = 'upper left',
        fancybox = True,
        shadow = False
        )
plt.subplot(2,1,2)
plt.plot(deltaArray, sigma_f_through_nArray,
        linewidth = commonLinewidth,
        color = colorBlue)
plt.ylabel(r'$\sigma / N$')
plt.xlabel(r'$\delta$')

plt.savefig('assets1/plot_wide.png', dpi = 300)
plt.subplot(2,1,1); plt.xlim(deltaArray[0]*0.9, 0.01*1.1); plt.ylim(0,2)
plt.subplot(2,1,2); plt.xlim(deltaArray[0]*0.9, 0.01*1.1); plt.ylim(0,.0001)
plt.savefig('assets1/plot_narrow.png', dpi = 300)
# plt.show()
