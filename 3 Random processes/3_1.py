# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.1

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl

# ------------------------- global variables

# Total number of particles
nTotArray = [8,64,800]

nStepsDict = {
8:      100,
64:     1000,
800:    10000
}

# Number of simulations for each n
nSimulations = 10000

# Seed the random generator
rnd.seed()

# storage
leftDict = {}
endLeftDict = {}
stepDict = {}

# ---------------------------- calculation
for nTot in nTotArray:
    stepArray = [ ]
    leftArray = [ ]
    endLeftArray = [ ]
    # Perform nsims independent simulations
    for simulation in range(nSimulations):
        # Initial number of particles on the left side
        nLeft = nTot
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

# -------------------------- plot

colors = pl.cm.plasma(np.linspace(0,0.9,len(nTotArray)))

for i in range(len(nTotArray)):
    plt.clf()
    stepArray = stepDict[nTotArray[i]]
    leftArray = leftDict[nTotArray[i]]
    plt.plot(stepArray,leftArray,
            color = colors[i])
    plt.plot([0, stepArray[-1]], [nTotArray[i]/2, nTotArray[i]/2],
            '--k', linewidth = 1)
    plt.legend([r'$n_{left}$', r'$n_{tot}/2$'],
            fancybox=True, shadow=True)
    plt.title('Particles in a box\n'+r'$n_{tot} = $' + str(nTotArray[i]))
    plt.savefig('assets1/plot_'+str(nTotArray[i])+'.png', dpi = 300)
    # plt.show()

if nSimulations > 1:
    plt.clf()
    for i in range(3):
        nTot = nTotArray[i]
        endLeftArray = endLeftDict[nTot]
        plt.subplot(3,1,i+1)
        if i==0:     plt.title('Final number of particles on the left, ' + str(nSimulations) + ' simulations.')
        n, bins, patches = plt.hist(endLeftArray,
                color = colors[i],
                bins = [x-0.5 for x in range(min(endLeftArray), max(endLeftArray)+2)])
        plt.legend([r'$n_{tot} = $' + str(nTot) + ', ' + str(nStepsDict[nTot]) + ' steps'],
                loc='upper left', ncol=1, fancybox=True, shadow=True)
        print('nTot',nTot,'\nn:\t', n, '\nbins:\t', bins, '\npatches\t', patches)
    plt.savefig('assets1/plot_hist.png', dpi = 300)
    # plt.show()
