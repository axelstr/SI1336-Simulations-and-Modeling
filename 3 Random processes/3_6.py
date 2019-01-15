# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.6

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd
import pylab as pl

# ------------------- global

# Seed the random generator
rnd.seed()

# Values
stepsArray = [10, 100, 1000]


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

# ---------------------- Calculate

# storage

xDict = {}  # keys = [0,1,2]
yDict = {}  # keys = [0,1,2]

# loop

for i in range(len(stepsArray)):
    x = [0]
    y = [0]
    steps = stepsArray[i]
    for step in range(steps):
        x,y = randomStep(x,y)
    xDict[i] = x
    yDict[i] = y

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
plt.title('Random, two-dimensional walk with single steps along x or y.')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.savefig('assets6/random_walk.png', dpi = 300)
plt.show()
