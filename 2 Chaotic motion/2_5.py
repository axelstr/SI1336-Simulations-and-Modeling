# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 2.5

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import pylab as pl

# -------------------------- First starting points, close to r_0

## Variables

sigma = 10
b = 8/3
r = 28

dt = 0.01        #
h = dt
t0 = 0.
tmax = 20
N = (tmax-t0)/dt

# xExamine = np.linspace(20,21,2)
# yExamine = np.linspace(20,21,2)
# zExamine = np.linspace(20,21,2)

xExamine = [10,20]
yExamine = [10,20]
zExamine = [10,20]

colors = pl.cm.viridis(np.linspace(0,1,len(xExamine)*len(yExamine)*len(zExamine)))

## Functions

def fx(x,y,z):
    return -sigma*x + sigma*y;

def fy(x,y,z):
    return -x*z + r*x -y

def fz(x,y,z):
    return x*y - b*z;



i = -1

xyDict = {}     # [xArray, yArray, color]
yzDict = {}
zxDict = {}
zmDict = {}

for x0 in xExamine:
    for y0 in yExamine:
        for z0 in zExamine:
            x = x0
            y = y0
            z = z0

            i += 1
            t = t0

            xArray = [x]
            yArray = [y]
            zArray = [z]
            zmArray = []

            xyDict[i] = []     # [xArray, yArray, color]
            yzDict[i] = []
            zxDict[i] = []
            zmDict[i] = []

            while t <= tmax:

                k1x = fx(x,y,z)
                k1y = fy(x,y,z)
                k1z = fz(x,y,z)

                k2x = fx(h*k1x/2,h*k1y/2,h*k1z/2)
                k2y = fy(h*k1x/2,h*k1y/2,h*k1z/2)
                k2z = fz(h*k1x/2,h*k1y/2,h*k1z/2)

                k3x = fx(h*k2x/2,h*k2y/2,h*k2z/2)
                k3y = fy(h*k2x/2,h*k2y/2,h*k2z/2)
                k3z = fz(h*k2x/2,h*k2y/2,h*k2z/2)

                k4x = fx(h*k3x,h*k3y,h*k3z)
                k4y = fy(h*k3x,h*k3y,h*k3z)
                k4z = fz(h*k3x,h*k3y,h*k3z)

                t += dt
                x += h/6*(k1x + 2*k2x + 2*k3x + k4x)
                y += h/6*(k1y + 2*k2y + 2*k3y + k4y)
                z += h/6*(k1z + 2*k2z + 2*k3z + k4z)

                xArray.append(x)
                yArray.append(y)
                zArray.append(z)

                if (xArray[-1]*yArray[-1]-b*zArray[-1]) * (xArray[-2]*yArray[-2]-b*zArray[-2]) < 0:
                    zmArray.append((zArray[-1]*zArray[-2])/2)

            xyDict[i] = [xArray, yArray]
            yzDict[i] = [yArray, zArray]
            zxDict[i] = [zArray, xArray]
            zmDict[i] = zmArray

imax = i

line1 = [[61.53,690.30], [891.77, 11.19]]
line2 = [[633.848, 1250.39], [2.6946, 537.452]]
k1 = (line1[1][1]-line1[1][0])/(line1[0][1]-line1[0][0])
k2 = (line2[1][1]-line2[1][0])/(line2[0][1]-line2[0][0])
m1 = line1[1][0] - line1[0][0]*k1
m2 = line2[1][0] - line2[0][0]*k2

plt.plot(line1[0], line1[1], '--k', linewidth = 0.5)
plt.plot(line2[0], line2[1], '-.k', linewidth = 0.5)

plt.legend([
    'y = ' + str(round(k1,2)) + 'x + ' + str(round(m1,2)),
    'y = ' + str(round(k2,2)) + 'x + ' + str(round(m2,2))
])

for i in range(imax+1):
    zmArray = zmDict[i]
    plt.scatter(zmArray[:-1], zmArray[1:], c = colors[i], s = 1, marker = '.')

plt.title(r'$z_{m+1}$ vs $z_m$')
plt.xlabel(r'$z_m$')
plt.ylabel(r'$z_{m+1}$')

plt.savefig('assets5/plot1.png', dpi = 300)
plt.show()
