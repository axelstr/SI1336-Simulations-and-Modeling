# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 2.4

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
tmax = 4
N = (tmax-t0)/dt

xExamine = np.linspace(20,21,2)
yExamine = np.linspace(20,21,2)
zExamine = np.linspace(20,21,2)

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

            xyDict[i] = []     # [xArray, yArray, color]
            yzDict[i] = []
            zxDict[i] = []

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

            xyDict[i] = [xArray, yArray]
            yzDict[i] = [yArray, zArray]
            zxDict[i] = [zArray, xArray]

            # ax1.plot(xArray, yArray, color = colors[i])
            # ax2.plot(yArray, zArray, color = colors[i])
            # ax3.plot(zArray, xArray, color = colors[i])

imax = i
i = 0

## plot

plt.figure(figsize=(8,6))
plt.tight_layout()
plt.title('Small initial values.')
linewidhtStandard = 0.4
markersizeStandard = 1

plt.subplot(2,2,1)
plt.title('y vs x')
for i in range(imax+1):
    plt.plot(xyDict[i][0], xyDict[i][1], color = colors[i], linewidth = linewidhtStandard)

    plt.plot(xyDict[i][0][0], xyDict[i][1][0], color = colors[i], markersize = markersizeStandard, marker = 'o')
plt.subplot(2,2,2)
plt.title('z vs y')
for i in range(imax+1):
    plt.plot(yzDict[i][0], yzDict[i][1], color = colors[i], linewidth = linewidhtStandard)
    plt.plot(yzDict[i][0][0], yzDict[i][1][0], color = colors[i], markersize = markersizeStandard, marker = 'o')

plt.subplot(2,2,3)
plt.title('x vs z')
for i in range(imax+1):
    plt.plot(zxDict[i][0], zxDict[i][1], color = colors[i], linewidth = linewidhtStandard)
    plt.plot(zxDict[i][0][0], zxDict[i][1][0], color = colors[i], markersize = markersizeStandard, marker = 'o')

plt.subplot(2,2,4)
text =  r'$x _0 \in [$'+ str(int(xExamine[0])) +', ' + str(int(xExamine[-1])) +'] \n' + \
        r'$y _0 \in [$'+ str(int(yExamine[0])) +', ' + str(int(yExamine[-1])) +'] \n' + \
        r'$z _0 \in [$'+ str(int(zExamine[0])) +', ' + str(int(zExamine[-1])) +'] \n' + \
        r'$\bullet$ are starting points'

plt.text(0.25,0.25, text, fontsize=10)

plt.savefig('assets4/plot1.png', dpi = 300)

# ------------------- second starting points, far from r_0

sigma = 10
b = 8/3
r = 28

dt = 0.01        #
h = dt
t0 = 0.
tmax = 4
N = (tmax-t0)/dt

xExamine = np.linspace(200,201,2)
yExamine = np.linspace(200,201,2)
zExamine = np.linspace(200,201,2)

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

            xyDict[i] = []     # [xArray, yArray, color]
            yzDict[i] = []
            zxDict[i] = []

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

            xyDict[i] = [xArray, yArray]
            yzDict[i] = [yArray, zArray]
            zxDict[i] = [zArray, xArray]

            # ax1.plot(xArray, yArray, color = colors[i])
            # ax2.plot(yArray, zArray, color = colors[i])
            # ax3.plot(zArray, xArray, color = colors[i])

imax = i
i = 0

## plot

plt.figure(figsize=(8,6))
plt.tight_layout()
plt.title('Large initial values.')
linewidhtStandard = 0.4
markersizeStandard = 1

plt.subplot(2,2,1)
plt.title('y vs x')
for i in range(imax+1):
    plt.plot(xyDict[i][0], xyDict[i][1], color = colors[i], linewidth = linewidhtStandard)

    plt.plot(xyDict[i][0][0], xyDict[i][1][0], color = colors[i], markersize = markersizeStandard, marker = 'o')
plt.subplot(2,2,2)
plt.title('z vs y')
for i in range(imax+1):
    plt.plot(yzDict[i][0], yzDict[i][1], color = colors[i], linewidth = linewidhtStandard)
    plt.plot(yzDict[i][0][0], yzDict[i][1][0], color = colors[i], markersize = markersizeStandard, marker = 'o')

plt.subplot(2,2,3)
plt.title('x vs z')
for i in range(imax+1):
    plt.plot(zxDict[i][0], zxDict[i][1], color = colors[i], linewidth = linewidhtStandard)
    plt.plot(zxDict[i][0][0], zxDict[i][1][0], color = colors[i], markersize = markersizeStandard, marker = 'o')

plt.subplot(2,2,4)
text =  r'$x _0 \in [$'+ str(int(xExamine[0])) +', ' + str(int(xExamine[-1])) +'] \n' + \
        r'$y _0 \in [$'+ str(int(yExamine[0])) +', ' + str(int(yExamine[-1])) +'] \n' + \
        r'$z _0 \in [$'+ str(int(zExamine[0])) +', ' + str(int(zExamine[-1])) +'] \n' + \
        r'$\bullet$ are starting points'

plt.text(0.25,0.25, text, fontsize=10)

plt.savefig('assets4/plot2.png', dpi = 300)
