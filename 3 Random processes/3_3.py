# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl

# ------------------------- global variables

# Total number of particles
nTotArray = [8]
nTot = 8

# Number of steps
# nSteps = 1000
nStepsDict = {
8:      100,
}

# Seed the random generator
seeds = [0,0,1]

# storage
leftDict = {}       # keys are 0,1,2
endLeftDict = {}    # keys are 0,1,2
stepDict = {}       # keys are 0,1,2

# ---------------------------- calculation
nSimulations = 3
for simulation in range(nSimulations):
    stepArray = [ ]
    leftArray = [ ]
    rnd.seed(seeds[simulation])
    # Initial number of particles on the left side
    nLeft = nTot
    nRight = 0
    nSteps = nStepsDict[nTot]
    for step in range(0,nSteps):
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
    leftDict[simulation] = leftArray
    stepDict[simulation] = stepArray

nSimulations = 1000
seeds = ['random', 0]
for i in range(len(seeds)):
    endLeftArray = [ ]
    for simulation in range(nSimulations):
        if seeds[i] == 0: rnd.seed(0)
        nLeft = nTot
        nRight = 0
        nSteps = nStepsDict[nTot]
        oddEvenEnding = round(rnd.random())
        for step in range(0,nSteps-oddEvenEnding):
            p = nLeft/nTot
            r = rnd.random()
            if r < p:
                nLeft -= 1
                nRight += 1
            elif r >= p:
                nLeft += 1
                nRight -= 1
        endLeftArray.append(nLeft)
    endLeftDict[i] = endLeftArray

# -------------------------- plot

colors = pl.cm.plasma(np.linspace(0,0.7,3))
colors = [colors[0], colors[2], colors[1]]

# graphs
linestyles = ['-', '--', '-']
for simulation in range(3):
    stepArray = stepDict[simulation]
    leftArray = leftDict[simulation]
    plt.plot(stepArray,leftArray,
            color = colors[simulation],
            linestyle = linestyles[simulation])
plt.plot([0, stepArray[-1]], [nTot/2, nTot/2],
        '--k', linewidth = 1)
plt.legend([r'seed = 0', r'seed = 0', r'seed = 1', r'$n_{tot}/2$'],
            fancybox=True, shadow=True)
plt.title('Particles in a box\n'+r'$n_{tot} = $' + str(nTot))
plt.savefig('assets3/plot_'+str(nTot)+'.png', dpi = 300)
# plt.show()

# histogram
plt.clf()
endLeftArray = endLeftDict[0]
plt.subplot(2,1,1)
plt.title('Final number of particles on the left, ' + str(nSimulations) + ' simulations.')
n, bins, patches = plt.hist(endLeftArray,
        color = colors[0],
        bins = [x-0.5 for x
        in range(min(endLeftArray), max(endLeftArray)+2)])
plt.legend(['seed = random'],
        fancybox=True, shadow=True)
endLeftArray = endLeftDict[1]
plt.subplot(2,1,2)
n, bins, patches = plt.hist(endLeftArray,
        color = colors[2],
        bins = [x-0.5 for x in range(min(endLeftArray), max(endLeftArray)+2)])
plt.axis([-1,9,0,1000])
plt.legend(['seed = 0'],
        fancybox=True, shadow=True)

print('nTot',nTot,'\nn:\t', n, '\nbins:\t', bins, '\npatches\t', patches)
plt.savefig('assets3/plot_hist.png', dpi = 300)
# plt.show()
