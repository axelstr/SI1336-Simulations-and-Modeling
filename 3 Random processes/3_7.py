# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 3.7

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab as pl

# ------------------- global


# Values

steps = 100
r0Array = [1,2,3]
aArray = [3,5]
cArray = [4,7]
mArray = [128,129,130]

# Functions

def random(a,c,m):
    global r
    """This function returns a random numer in the range 0 to m. The new seed r
    overwrites the global old seed r."""
    r = (a*r+c) % m
    return r/(m-1)%1

def randomStep(x,y,a,c,m):
    """This function takes x and y arrays and returns new x and y arrays with a
    new, random step taken at the end of the arrays."""
    directions = {
        0:  [1,0],
        1:  [0,1],
        2:  [-1,0],
        3:  [0,-1]
    }
    direction = directions[int(4*random(a,c,m))]
    x.append(x[-1]+direction[0])
    y.append(y[-1]+direction[1])
    return x,y

# ---------------------- Calculate

# storage

xDict = {}  # keys = [,1,2,...]
yDict = {}  # keys = [0,1,2,...]

# loop

def runSimulation(r0,a,c,m, steps = 100):
    global r
    r = r0
    x = [0]
    y = [0]
    for step in range(steps):
        x,y = randomStep(x,y,a,c,m)
    return x,y

# --------------------- Plot

# examine r0 dependence

r0Array = [1,3,7]
a = 3
c = 4
m = 128

colors = pl.cm.viridis(np.linspace(0.1,0.9,3))
i = -1          # counts color to use and zorder
mSize = 30      # common markersize
linestyles = [':','--','-']

legendArray = []
plt.scatter([0],[0],
    c = 'k',
    marker = 'x',
    s = mSize,
    zorder = 4)
for r0 in r0Array:
    i += 1
    x, y = runSimulation(r0,a,c,m)
    plt.plot(x, y,
        linewidth = 1,
        color = colors[i],
        zorder = 3-i,
        linestyle = linestyles[i])
    legendArray.append(r'$r_0 = $' + str(r0))
    plt.scatter(x[-1],y[-1],
        c = [colors[i]],
        marker = 'x',
        s = mSize,
        zorder = 4)
legendArray.append('start/end - points')
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
print(r0, a,c)
plt.title('Random, two-dimensional walk with single steps along x or y. \n' \
    + r'$a=%d, \quad c = %d, \quad m = %d$' %(a,c,m))
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.savefig('assets7/random_walk_r0-dependence.png', dpi = 300)
# plt.show()

# examine a dependence

plt.clf()

r0 = 1
aArray = [2,3,5]
c = 4
m = 128

colors = pl.cm.viridis(np.linspace(0.1,0.9,3))
i = -1          # counts color to use and zorder
mSize = 30      # common markersize
linestyles = [':','--','-']

legendArray = []
plt.scatter([0],[0],
    c = 'k',
    marker = 'x',
    s = mSize,
    zorder = 4)
for a in aArray:
    i += 1
    x, y = runSimulation(r0,a,c,m)
    plt.plot(x, y,
        linewidth = 1,
        color = colors[i],
        zorder = 3-i,
        linestyle = linestyles[i])
    legendArray.append(r'$a = $' + str(a))
    plt.scatter(x[-1],y[-1],
        c = colors[i],
        marker = 'x',
        s = mSize,
        zorder = 4)
legendArray.append('start/end - points')
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
print(r0, a,c)
plt.title('Random, two-dimensional walk with single steps along x or y. \n' \
    + r'$r_0 = %d, \quad c = %d, \quad m = %d$' %(r0,c,m))
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.axis([-7.5,7.5,-7.5,7.5])
plt.savefig('assets7/random_walk_a-dependence.png', dpi = 300)
# plt.show()

# examine c dependence

plt.clf()

r0 = 1
a = 3
cArray = [3,4,9]
m = 128

colors = pl.cm.viridis(np.linspace(0.1,0.9,3))
i = -1          # counts color to use and zorder
mSize = 30      # common markersize
linestyles = [':','--','-']

legendArray = []
plt.scatter([0],[0],
    c = 'k',
    marker = 'x',
    s = mSize,
    zorder = 4)
for c in cArray:
    i += 1
    x, y = runSimulation(r0,a,c,m)
    plt.plot(x, y,
        linewidth = 1,
        color = colors[i],
        zorder = 3-i,
        linestyle = linestyles[i])
    legendArray.append(r'$c = $' + str(c))
    plt.scatter(x[-1],y[-1],
        c = [colors[i]],
        marker = 'x',
        s = mSize,
        zorder = 4)
legendArray.append('start/end - points')
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
print(r0, a,c)
plt.title('Random, two-dimensional walk with single steps along x or y. \n' \
    + r'$r_0 = %d, \quad a = %d, \quad m = %d$' %(r0,a,m))
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.axis([-7.5,7.5,-7.5,7.5])
plt.savefig('assets7/random_walk_c-dependence.png', dpi = 300)
# plt.show()

# examine m dependence
plt.clf()

r0 = 1
a = 3
c = 4
mArray = [128,129,130]

colors = pl.cm.viridis(np.linspace(0.1,0.9,len(mArray)))
i = -1          # counts color to use and zorder
mSize = 30      # common markersize
linestyles = [':','--','-']


legendArray = []
plt.scatter([0],[0],
    c = 'k',
    marker = 'x',
    s = mSize,
    zorder = 4)
for m in mArray:
    i += 1
    x, y = runSimulation(r0,a,c,m)
    plt.plot(x, y,
        linewidth = 1,
        color = colors[i],
        zorder = 3-i,
        linestyle = linestyles[i])
    legendArray.append(r'$m = $' + str(m))
    plt.scatter(x[-1],y[-1],
        c = colors[i],
        marker = 'x',
        s = mSize,
        zorder = 4)
legendArray.append('start/end - points')
plt.legend(legendArray,
    fancybox = True,
    shadow = True)
print(r0, a,c)
plt.title('Random, two-dimensional walk with single steps along x or y. \n' \
    + r'$r_0 = %d, \quad a=%d, \quad c = %d$' %(r0,a,c))
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.savefig('assets7/random_walk_m-dependence.png', dpi = 300)
# plt.show()
