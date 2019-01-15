# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 4.5

# -------------------- Import libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random as rnd
import pylab as pl
from scipy.optimize import curve_fit
import sys

sys.setrecursionlimit(10000)

# -------------------- Define functions

spreadDirections = np.array([[1,0],[0,1],[-1,0],[0,-1]])

def spread_fire(forestSquare,L,x,y):
    global clusterSizeCounter
    clusterSizeCounter += 1
    for nb in range(0,4):
        nx = (x + spreadDirections[nb,0] + L) % L
        ny = (y + spreadDirections[nb,1] + L) % L
        if forestSquare[nx,ny] == 1:
            forestSquare[nx,ny] = 2
            # Spread the fire recursively
            spread_fire(forestSquare,L,nx,ny)

def countOccurances(inputArray):
    """This function takes inputArray as an array of integers and returns a new array where
    the value for each index is the number of times that index value appears
    in inputArray."""
    outputArray = [0 for x in range(max(inputArray)+1)]
    for integer in inputArray:
        outputArray[integer] += 1
    return outputArray


# -------------------- Define variables

L = 50      # side length of forest square
g = 0.1     # The chance of growing a new tree
f = 0.1     # The change of a tree being struck by lightning

gArray = [0.01,0.1]
fArray = [0.01,0.1,0.3]

nSteps = 500

# -------------------- Storage

titles = []
N_sArray = []
N_sMeansArray = []
sPositionsArray = []
legends = []

# -------------------- Calculation

for g in gArray:
    for f in fArray:
        clusterSizesArray = []  # will contain arrays of N(s), each array corresponding
                                # to each step, thus len(clusterSizesArray) = nSteps
        # s=0: empty
        # s=1: a tree
        # s=2: a tree that just caught fire at time t
        forestSquare = np.zeros((L,L))
        maxClusterSize = 0
        for step in range(nSteps):
            clusterArray = []   # everytime a fire spreads of clustersize s, s is added to this array

            # go through forest, grow random trees, ignite random trees, remove dead trees
            for x in range(0,L):
                for y in range(0,L):
                    if forestSquare[x,y] == 0:
                        if rnd.random() < g:
                            forestSquare[x,y] = 1
                    else:
                        if forestSquare[x,y] == 1:
                            if rnd.random() < f:
                                forestSquare[x,y] = 2
            # spread the fire recursively
            for x in range(0,L):
                for y in range(0,L):
                    if forestSquare[x,y] >= 2:
                        clusterSizeCounter = 1
                        spread_fire(forestSquare,L,x,y)
                        clusterArray.append(clusterSizeCounter)
                        if clusterSizeCounter > maxClusterSize:
                            maxClusterSize = clusterSizeCounter
            # Remove dead trees
            for x in range(0,L):
                for y in range(0,L):
                    # Spread the fire
                    if forestSquare[x,y] == 2:
                        forestSquare[x,y] = 0
            # print(clusterArray)
            if clusterArray != []: # sometimes nothing happens
                clusterSizesArray.append(countOccurances(clusterArray))

        N_s = [ [] for x in range(maxClusterSize+1)]        # the number of clusters of trees of size (index) that catch fire in each iteration
        sPositions = [x for x in range(maxClusterSize+1)]

        for clusterSizes in clusterSizesArray:
            for clusterSize in range(len(clusterSizes)):
                N_s[clusterSize].append(clusterSizes[clusterSize])
        N_sMeans = [np.mean(array) for array in N_s]
        N_sArray.append(N_s)
        N_sMeansArray.append(N_sMeans)
        sPositionsArray.append(sPositions)
        titles.append(r'Clustersizes, $N$, of size $s$ that catch on fire each step.'+'\n'+r'$g=%s, f=%s$'%(g,f))
        legends.append(r'$g=%s, f=%s$'%(g,f))

# ----------------------- Plots

# box plot with graph fit
for i in range(len(gArray)*len(fArray)):

    # gather data
    N_s = N_sArray[i]
    N_sMeans = N_sMeansArray[i]
    sPositions = sPositionsArray[i]
    currentTitle = titles[i]

    # fit functions
    sPositions2 = sPositions[2:21]
    N_sMeans2 = N_sMeans[2:21]

    def fFitted(s,c,alfa):
        return c*s**(-alfa)

    popt, _ = curve_fit(fFitted, sPositions2, N_sMeans2)
    c = popt[0]
    alfa = popt[1]
    cRounded = round(c)
    alfaRounded = round(alfa,2)

    xArray = np.linspace(sPositions2[0], sPositions2[-1], 1001)
    plt.plot(xArray, [fFitted(x, c,alfa) for x in xArray],
            color = 'r',
            zorder = 2)
    plt.legend([
        r'$\langle N(s) \rangle =  %s \, s^{-%s}$'%(cRounded,alfaRounded)
        ],
        fancybox = True,
        shadow = True)

    currentTitle += r'$\rightarrow \alpha = %s $'%(alfaRounded)

    # boxplot
    plt.boxplot(N_s, positions = sPositions,
            patch_artist = True,
            zorder = 1) # width = 0.1

    plt.title(currentTitle)
    # plt.axis([-0.5, 10.5, -0.5, 500])
    plt.xlim(-0.5,10.5)
    plt.ylabel(r'$N(s)$')
    plt.xlabel(r'$s$')
    plt.savefig('assets5/boxplot%d.png'%(i), dpi = 300)
    plt.clf()

# plot all means in one plot
colors = pl.cm.viridis( np.linspace(0.1,0.9,len(gArray)*len(fArray)) )
commonLinewidth = 1
commonMarker = 'o'
commonMarkersize = 4

for i in range(len(gArray)*len(fArray)):
    N_sMeans = N_sMeansArray[i]
    sPositions = sPositionsArray[i]
    plt.plot(sPositions, N_sMeans,
            color = colors[i],
            linewidth = commonLinewidth,
            marker = commonMarker,
            markersize = commonMarkersize)
plt.legend(legends,
        fancybox = True,
        shadow = True)
plt.title(r'$\langle N(s) \rangle$: Means of clustersizes of size $s$ that catch on fire each step.')
plt.xlim(-0.5,10.5)
plt.ylabel(r'$\langle N(s) \rangle$')
plt.xlabel(r'$s$')
plt.savefig('assets5/meansplot.png', dpi = 300)
