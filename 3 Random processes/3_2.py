# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.2

from scipy.stats import norm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl


# ------------------------- global variables

# Total number of particles
nTotArray = [800]

# Number of steps
# nSteps = 1000
nStepsDict = {
8:      100,
64:     1000,
800:    1000000
}

# Number of simulations for each n
nSimulations = 1

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

## fit leftEnd[2000:] to normal distribution
leftArray = leftDict[800]
examineArray = leftArray[50000:]

mean, std = norm.fit(examineArray)
x = np.linspace(340, 460, 1001)
p = norm.pdf(x,mean,std)

# -------------------------- plot

colors = [pl.cm.plasma(0.9)]

for i in range(len(nTotArray)):
    plt.clf()
    stepArray = stepDict[nTotArray[i]]
    leftArray = leftDict[nTotArray[i]]
    plt.plot(stepArray,leftArray,
            color = colors[i])
    plt.plot([0, stepArray[-1]], [nTotArray[i]/2, nTotArray[i]/2],
            '--k', linewidth = 1)
    plt.plot([50000, 50000], [300,500], ':k')
    plt.plot([1000000, 1000000], [300,500], ':k')
    plt.legend([r'$n_{left}$', r'$n_{tot}/2$', r'interval for distribution analysis'],
                fancybox=True, shadow=True)
    plt.title('Particles in a box\n'+r'$n_{tot} = $' + str(nTotArray[i]))
    plt.savefig('assets2/plot_'+str(nTotArray[i])+'.png', dpi = 300)
    # plt.show()

plt.clf()
plt.title(r'Distribution of $n_{left}$ for $t\in [50\,000,1\,000\,000]$ .' + '\n' \
        + r'$\mu = $' + str(round(mean,2)) + '\t' + r'$\sigma$ = ' + str(round(std,2)))

n, bins, patches = plt.hist(examineArray,
        color = colors[i],
        bins = [x-0.5 for x in range(min(examineArray), max(examineArray)+2)],
        density = True)
plt.plot(x,p,
        color = [0.1,0.3,1],
        linewidth = 1)
plt.legend([r'fitted normal distribution', r'$n_{left}$ -distribution'])
print('nTot',nTot,'\nn:\t', n, '\nbins:\t', bins, '\npatches\t', patches)
plt.savefig('assets2/plot_hist.png', dpi = 300)
# plt.show()
