# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 5.2

# ---------------------- Import libraries

import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import random as rnd
import pylab as pl
import numpy as np
import datetime

# ---------------------- Define variables

sigma = 1
epsilon = 1

nParticles = 20     # Number of particles
Lx = 5.6            # Unit cell size
Ly = 5.6

kB = 1          # Boltzmann constant
T = 0.6         # Temperature
kBT = kB * T    # kb*T

start  = 1000
nSteps = 5000
# start = 0
# nSteps = 1000
nStepsPerFrame = 1
numframes = int(nSteps/nStepsPerFrame)
rnd.seed()

# The maximum step size
# FOR OPTIMAL PERFORMANCE, TUNE THIS FOR THE GIVEN SYSTEM AND DENSITY
delta = 0.0001
# deltaArray = np.linspace(0.0001,0.01, 10)
deltaArray = [0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
print('Simulating with deltas:', deltaArray)
# storage
stepArray = []
epotArray = []


# ---------------------- Define functions

def V(r):
    return 4*epsilon*( (sigma/r)**12 - (sigma/r)**6 )

# Calculate the shortest periodic distance, unit cell [0,Lx],[0,Ly]
# This code assumes all particles are within [0,Lx],[0,Ly]
def pbc_dist(x1,y1,x2,y2,Lx,Ly):
    dx = x1 - x2
    dy = y1 - y2
    while dx < -0.5*Lx:
        dx += Lx
    while dx > 0.5*Lx:
        dx -= Lx
    while dy < -0.5*Ly:
        dy += Ly
    while dy > 0.5*Ly:
        dy -= Ly
    return math.sqrt(dx*dx + dy*dy)



# Initialize the particle position to a nearly hexagonal lattice
x = []
y = []
for i in range (0,nParticles):
    x.append(Lx/5*((i % 5) + 0.5*(int(i/5))))
    y.append(Lx/5*0.87*(int(i/5)))

# Determine the initial value of the potential
v = 0
for i in range(0,nParticles):
    for j in range(i+1,nParticles):
        r = pbc_dist(x[i],y[i],x[j],y[j],Lx,Ly)
        v += V(r)

step = 0
# The sum of the acceptance ratio over start to numsteps
sar = 0
# The sum of the potential and the potential squared
sv  = 0
svv = 0

# Perform one MC sweep over all particles
def mc_sweep():
    global nParticles, start, step, x, y, v, sar, sv, svv

    for i in range(0,nParticles):
        xn = x[i] + delta*(2*rnd.random() - 1)
        yn = y[i] + delta*(2*rnd.random() - 1)
        dV = 0
        for j in range(0,nParticles):
            if i != j:
                r = pbc_dist(x[i],y[i],x[j],y[j],Lx,Ly)
                rn = pbc_dist(xn, yn, x[j], y[j], Lx, Ly)
                dV  += V(rn) - V(r)

        ratio = math.exp(-dV/kBT)
        # ratio=1

        sar += min(1,ratio)

        if ratio > rnd.random():
            # Accept the new configuration
            x[i] = xn
            y[i] = yn
            v += dV

        # Put the particle back in the box
        if x[i] < 0:
            x[i] += Lx
        if x[i] >= Lx:
            x[i] -= Lx
        if y[i] < 0:
            y[i] += Ly
        if y[i] >= Ly:
            y[i] -= Ly

    if step >= start:
        sv  += v
        svv += v*v

    if step % nStepsPerFrame == 0:
        stepArray.append(step)
        epotArray.append(v)
        if step > start:
            v_av  = sv/(step + 1 - start)
            vv_av = svv/(step + 1 - start)

            # print("<V>", v_av, "cV", (vv_av - v_av*v_av)/(kB*T*T), "ratio", sar/((step+1)*nParticles))

    step += 1


def animate(iterationNumber):
    global nStepsPerFrame, nParticles, step, x, y, v, sar, sv, svv
    for it in range(nStepsPerFrame):
        mc_sweep()

    # return ax.scatter(x, y, s=1500, marker='o', c="r"),

plt.figure()
colors = pl.cm.jet( np.linspace(0.1,0.9, len(deltaArray)) )
legendArray = []
k = -1
for delta in deltaArray:
    print('-------------- Current delta:', delta, '\nRunning', nSteps,'iteartions.')
    # Initialize the particle position to a nearly hexagonal lattice
    x = []
    y = []
    for i in range (0,nParticles):
        x.append(Lx/5*((i % 5) + 0.5*(int(i/5))))
        y.append(Lx/5*0.87*(int(i/5)))

    # Determine the initial value of the potential
    v = 0
    for i in range(0,nParticles):
        for j in range(i+1,nParticles):
            r = pbc_dist(x[i],y[i],x[j],y[j],Lx,Ly)
            v += V(r)

    step = 0
    # The sum of the acceptance ratio over start to numsteps
    sar = 0
    # The sum of the potential and the potential squared
    sv  = 0
    svv = 0
    stepArray = []
    epotArray = []
    k += 1
    for iterationNumber in range(nSteps):
        if iterationNumber % 1000 == 0: print('Current iteration:',iterationNumber)
        animate(iterationNumber)
    plt.plot(stepArray,epotArray,
            color = colors[k],
            linewidth = 0.3)
    legendArray.append(r'$\delta = %s$'%(round(delta, 7)))
plt.legend(legendArray,
        fancybox = True)
plt.title(r'Convergence of $V$ for different $\delta$.')
plt.ylabel('V')
plt.xlabel('step')
filename = 'assets2/archive/plot '+str(datetime.datetime.now()).replace(':','.')+'.png'
plt.savefig(filename, dpi = 300)
plt.show()
