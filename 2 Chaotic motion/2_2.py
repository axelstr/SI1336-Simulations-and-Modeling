# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 2.2

#!/usr/bin/python

import pylab as pl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# matplotlib.rcParams.update({'font.size': 20})



# ----------------------- GLOBAL

plt.figure(figsize=(8,6))

## Variables

nx0 = 9             # number of x0 to examine
colors = pl.cm.viridis(np.linspace(0.1,0.9,nx0))
filenames = []

## Functions

def getLyapunov(x):
    """ Takes an array x and step size h and returns the Lyapunov exponent."""
    n = len(x)
    sum = 0
    for i in range(n-1):
        # if x[+1] != x[i]:
        sum += np.log(  np.abs( 4*r - 8*r*x[i] ) )
    return sum/n

def getLyapunovMaxWhenStable(rArray, lArray):
    """Given corresponding rArray and lArray. If rArray[k] > r_inf (unstable)
    this function returns max(lArray[0:k-1])."""
    assert len(rArray) == len(lArray)
    lExamine = []
    for i in range(len(rArray)):
        if rArray[i] > r_inf: break
        lExamine.append(lArray[i])
    return max(lExamine)

# ---------------------- part 1 lyaponov vs r get lyaponov when stable for one x

## variables

nsteps = 1000     # total number of steps

r_inf = 0.892486417967
rArray = np.linspace(0.76, 1, 101)
lArray = []
x0 = 0.5          # initial x (seed)

plot_start = 20   # start the plot at this step

## loop

for r in rArray:
    x = x0
    sArray = [ ]
    xArray = [ ]
    for step in range(0,nsteps):
        if step >= plot_start:
            sArray.append(step)
            xArray.append(x)
        x = 4*r*x*(1 - x)
    lyapunov = getLyapunov(xArray)
    lArray.append(lyapunov)


# lyapunovMaxWhenStable = getLyapunovMaxWhenStable(rArray, lArray)
lyapunovMaxWhenStable = 0

## plot

plt.plot(rArray, lArray, color = colors[3])
plt.plot([r_inf, r_inf], [min(lArray), max(lArray)], '--k')
plt.plot([min(rArray), max(rArray)], [lyapunovMaxWhenStable, lyapunovMaxWhenStable], ':k')

#
plt.xlabel(r'$r$')
plt.ylabel(r'$\lambda$')
plt.title(r'$\lambda(r)r$.')
plt.legend([
    r'$\lambda(r)$',
    r'$r = r_\infty \approx 0.892486417967$',
    r'$\lambda = $' + str(lyapunovMaxWhenStable)])
    # plt.tight_layout()
plt.savefig('assets2/lyapunov-vs-r.png', dpi = 300)
filenames.append('assets2/lyapunov-vs-r.png')
# plt.show()
# plt.clf()

# ---------------- Depends on x_0?

## variables

nsteps = 1000     # total number of steps


r_inf = 0.892486417967
x0Array = np.linspace(0.1,0.9,nx0)
rArray = np.linspace(0.76, 1, 101)
lDict = {}


plot_start = 20   # start the plot at this step

for x0 in x0Array:
    lDict[x0] = []
    for r in rArray:
        x = x0
        sArray = [ ]
        xArray = [ ]
        for step in range(0,nsteps):
            if step >= plot_start:
                sArray.append(step)
                xArray.append(x)
            x = 4*r*x*(1 - x)
        lyapunov = getLyapunov(xArray)
        lDict[x0].append(lyapunov)

# lyapunovMaxWhenStable = getLyapunovMaxWhenStable(rArray, lDict[0.5])
# lyapunovMaxWhenStable

## plot

plt.clf()

plt.plot([r_inf, r_inf], [-2, 0.5], '--k')
plt.plot([min(rArray), max(rArray)], [lyapunovMaxWhenStable, lyapunovMaxWhenStable], ':k')
legendArray = [
r'$r = r_\infty \approx 0.892$',
r'$\lambda = $' + str(round(lyapunovMaxWhenStable,6))
]
for i in range(len(x0Array)):
    x0 = x0Array[i]
    plt.plot(rArray, lDict[x0], color = colors[i])
    legendArray.append(r'$x_0 = $' + str(round(x0,1)))

box1x = [0.825, 0.840, 0.840, 0.825, 0.825]
box1y = [-0.550, -0.550, -0.375, -0.375, -0.550,]
box2x = [0.945, 0.960, 0.960, 0.945, 0.945]
box2y = [0.325, 0.325, 0.5, 0.5, 0.325]

plt.plot(box1x, box1y, 'r')
plt.plot(box2x, box2y, 'darkred')
plt.legend(legendArray)
plt.title(r'Dependece on $\lambda(r)$ from $x_0$.')
plt.xlabel(r'$r$')
plt.ylabel(r'$\lambda$')
# plt.tight_layout()

plt.savefig('assets2/x0-dependece-1.png', dpi = 300)
plt.axis([0.824, 0.841, -0.552, -0.373])
plt.title(r'Dependece on $\lambda(r)$ from $x_0$.' + '\n' + r'$r < r_\infty$')
plt.savefig('assets2/x0-dependece-2.png', dpi = 300)
plt.title(r'Dependece on $\lambda(r)$ from $x_0$.'+ '\n' + r'$r > r_\infty$')
plt.axis([0.944, 0.961, 0.323, 0.502])
plt.savefig('assets2/x0-dependece-3.png', dpi = 300)

filenames.append('assets2/x0-dependece-1.png')
filenames.append('assets2/x0-dependece-2.png')
filenames.append('assets2/x0-dependece-3.png')

# plt.show()


# --------------------- rounding

plt.clf()

## variables

nsteps = 1000     # total number of steps

r_inf = 0.892486417967
rArray = np.linspace(0.76, 1, 101)
lArrayRound = []
x0 = 0.5          # initial x (seed)

plot_start = 20   # start the plot at this step

## loop

for r in rArray:
    x = x0
    sArray = [ ]
    xArray = [ ]
    for step in range(0,nsteps):
        if step >= plot_start:
            sArray.append(step)
            xArray.append(x)
        x = round(4*r*x*(1 - x), 6)
    lyapunov = getLyapunov(xArray)
    lArrayRound.append(lyapunov)


# lyapunovMaxWhenStable = getLyapunovMaxWhenStable(rArray, lArray)
lyapunovMaxWhenStable = 0

## plot

plt.plot([r_inf, r_inf], [min(lArray), max(lArray)], '--k')
plt.plot([min(rArray), max(rArray)], [lyapunovMaxWhenStable, lyapunovMaxWhenStable], ':k')

plt.plot(rArray, lArray, color = colors[3])
plt.plot(rArray, lArrayRound, color = colors[7], linestyle = '--')

#
plt.xlabel(r'$r$')
plt.ylabel(r'$\lambda$')
plt.title(r'$\lambda(r)$, \quad $x_0=0.5$' + '\n with rounding.')
plt.legend([
    r'$r = r_\infty \approx 0.892486417967$',
    r'$\lambda = $' + str(lyapunovMaxWhenStable),
    r'$\lambda(r)$',
    r'$\lambda(r)$ with rounding'
])
plt.savefig('assets2/lyapunov-with-rounding.png', dpi = 300)
# plt.show()
# plt.clf()

filenames.append('assets2/lyapunov-with-rounding.png')


# ------------------------- print for latex

print('\n\tFor latex (beamer):\n')
for i in range(len(filenames)):
    print('{\\centering\n\\includegraphics<'+str(i+1)+'>[height=0.9\\textheight]{'+filenames[i]+'}\n}')
