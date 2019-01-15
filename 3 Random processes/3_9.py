# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.9

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
stepsArray = [10,20,30]
stepsRange = [x for x in range(1,50)]       # examine succesfullnes of self avoidance fo
attempts = 100000                             # number of tries for each step

# Functions

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

methods = ['random step method', 'improved random step method']
methodDict = {
    methods[0]: randomStep,
    methods[1]: improvedRandomStep
}

# ---------------------- Calculate

# loop stepsarray

xDict = {}  # keys = [0,1,2]
yDict = {}  # keys = [0,1,2]

for i in range(len(stepsArray)):
    steps = stepsArray[i]
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
    xDict[i] = x
    yDict[i] = y

# loop stepsrange

successrateDict = {}    # keys = ['random step method', 'improved random step method']

for method in methods:
    randomStepMethod = methodDict[method]
    successrateArray = []
    for steps in stepsRange:
        successfulAttempts = 0
        attempt = 0
        while attempt < attempts:
            step = 0
            x = [0]
            y = [0]
            while step < steps and attempt < attempts:
                step += 1
                x,y = randomStepMethod(x,y)
                xEnd, yEnd = x[-1], y[-1]
                for j in range(len(x)-1):
                    if xEnd == x[j] and yEnd == y[j]:
                        # print('breaking', x,y)
                        step,x,y = 0,[0],[0]
                        attempt += 1
                        break
                if step == steps:
                    successfulAttempts += 1
            attempt += 1
        successrateArray.append(successfulAttempts/attempts)
    successrateDict[method] = successrateArray


# --------------------- Plot

colors = pl.cm.viridis([0.1,0.5,0.9])
mSize = 30      # common markersize

legendArray = []
plt.scatter([0],[0],
    c = 'k',
    marker = 'x',
    s = mSize,
    zorder = 4)
for i in range(len(stepsArray)):
    x,y = xDict[i],yDict[i]
    plt.plot(x, y,
        linewidth = 1,
        color = colors[i],
        zorder = 3-i)
    legendArray.append(r'$n_{steps} = $' + str(stepsArray[i]))
    plt.scatter(x[-1],y[-1],
        c = [colors[i]],
        marker = 'x',
        s = mSize,
        zorder = 4)
legendArray.append('start/end - points')
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
plt.title('Random, two-dimensional, self-avoiding walk \n with single steps along x or y.')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.savefig('assets9/plot.png', dpi = 300)
# plt.show()

# plot successrate

colors = {
    methods[0]: pl.cm.jet(0.1),
    methods[1]: pl.cm.jet(0.9)
}
linestyles = {
    methods[0]: '-',
    methods[1]: '-'
}

# plot successrate

plt.clf()
legendArray = []
for method in methods:
    successrateArray = successrateDict[method]
    succesratePercentArray = [x*100 for x in successrateArray]
    plt.plot(stepsRange, succesratePercentArray,
        linewidth = 1,
        linestyle = linestyles[method],
        color = colors[method])
    legendArray.append(method)
plt.plot([3,3],[85,102], '--k', linewidth = 1)
legendArray.append(r'$n_{steps}=3$')
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
plt.title(r'Success rate of self avoiding random walk,' +'\n'+ r'%d attempts for each $n_{steps}$'%(attempts))
plt.xlabel(r'$n_{steps}$')
plt.ylabel(r'Succesrate, %')
plt.savefig('assets9/successplot.png', dpi = 300)
# plt.show()

# plot log(successrate)

def line1(x,k):
    return k*x
def line2(x,k):
    return k*(x-3)
lines = {
    methods[0]: line1,
    methods[1]: line2
}
colors2 = {
    methods[0]: pl.cm.jet(0.3),
    methods[1]: pl.cm.jet(0.7)
}

plt.clf()
legendArray = []
for method in methods:
    line = lines[method]
    successrateArray = successrateDict[method]
    removeFromX = []
    plotx = stepsRange[:]
    ploty = []
    for i in range(len(successrateArray)):
        if successrateArray[i] == 0:
            removeFromX.append(i)
        else:
            ploty.append(np.log(successrateArray[i]))
    removeFromX.reverse()
    for i in removeFromX: plotx.pop(i)
    popt, pcov = curve_fit(line, plotx, ploty)
    k = popt[0]
    plt.plot(plotx, ploty,
        linewidth = 1,
        color = colors[method])
    plt.plot(plotx, [line(x,k) for x in plotx],
        linewidth = 1,
        color = colors2[method],
        linestyle = '--')
    legendArray.append(method)
    legendArray.append('regression, slope = %f'%(k))
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
plt.title(r'Semilog plot of success rate of self avoiding random walk,' +'\n'+ r'%d attempts for each $n_{steps}$'%(attempts))
plt.xlabel(r'$n_{steps}$')
plt.ylabel(r'ln(Succesrate)')
plt.savefig('assets9/successsemilogplot.png', dpi = 300)
# plt.show()
