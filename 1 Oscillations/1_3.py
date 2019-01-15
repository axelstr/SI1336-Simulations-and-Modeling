# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 1.3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

# -------------------------- GLOBAL ------------------------------- #

t = 0.	             # start time
tmax = 4.
dt = 0.01
x = 1
v = 0
omega0 = 3
gammas = [0.5,1,2,3]
N = tmax/dt

m = 1
g = 9.82
L=g/(omega0**2)                # string length

## Functions

def a(x,v):
    return - omega0**2*x - gamma*v

def rungeKuttaStep():
    global a, v, x
    a1 = a(x,v)             * dt
    b1 = v                  * dt
    a2 = a(x+b1/2, v+a1/2)  * dt
    b2 = (v+a1/2)           * dt
    a3 = a(x+b2/2, v+a2/2)  * dt
    b3 = (v+a2/2)           * dt
    a4 = a(x+b3, v+a3)      * dt
    b4 = (v+a3)             * dt

    v +=    1/6 * (a1+2*a2+2*a3+a4)
    x +=    1/6 * (b1+2*b2+2*b3+b4)

def getTau(values,ts):
    """Takes value array and ts (time) array and then returns tau.
    tau:= smallest tau so that value(t) < 1/e forall t > tau."""
    tau = None
    assert len(values) == len(ts)
    for i in range(len(values)):
        if np.abs(values[i]) < 1/np.e and tau == None:
            tau = ts[i]
        elif np.abs(values[i]) >= 1/np.e:
            tau = None
    return tau

# ---------------------------------------- 1.3.a

xDict = {}
vDict = {}
EDict = {}
tArray = []

for gamma in gammas:
    gamma = gamma
    t = 0
    x = 1
    v = 0
    tArray = []
    xDict[gamma] = []
    vDict[gamma] = []
    EDict[gamma] = []
    while t < tmax:
        t += dt
        rungeKuttaStep()
        tArray.append(t)
        xDict[gamma].append(x)
        vDict[gamma].append(v)
        EDict[gamma].append(0.5*m*L**2*v**2 + 0.5*m*g*L*x**2)
linestyleDict = {
    0.5:    '-',
    1:      '--',
    2:      '-.',
    3:      ':',
}
for gamma in gammas:
    plt.plot([0],[0],'k', linestyle = linestyleDict[gamma])
for gamma in gammas:
    plt.plot(tArray, xDict[gamma], 'b', linestyle = linestyleDict[gamma], linewidth = 1)
    plt.plot(tArray, vDict[gamma], 'orange', linestyle = linestyleDict[gamma], linewidth = 1)
    plt.plot(tArray, EDict[gamma], 'g', linestyle = linestyleDict[gamma], linewidth = 1)
plt.xlabel('t')
plt.legend([r'$\gamma = 0.5$',r'$\gamma = 1$',r'$\gamma = 2$',r'$\gamma = 3$',r'$x(t)$',r'$\dot x(t)$',r'$E$'])
plt.title(r'Damped harmonic oscillator.')
plt.savefig('assets3/xvE-to-t.png', dpi = 300)

## get tau

tmax = 20
xDict = {}
vDict = {}
EDict = {}
tArray = []

for gamma in gammas:
    gamma = gamma
    t = 0
    x = 1
    v = 0
    tArray = []
    xDict[gamma] = []
    vDict[gamma] = []
    EDict[gamma] = []
    while t < tmax:
        t += dt
        rungeKuttaStep()
        tArray.append(t)
        xDict[gamma].append(x)
        vDict[gamma].append(v)
    tau = getTau(xDict[gamma], tArray)
    print('\\gamma = ' + str(gamma) +' & \\tau = ' + str(round(tau,2))+ '\\\\')


# ----------------------- 1.3.b
plt.clf()
gammas = np.linspace(0.5,4,201)
redGammas = [0.64, 0.9550000000000001, 1.83]
taus = []
tDict = {}
xDict = {}
plt.plot([0,5], [1/np.e,1/np.e], '--k', linewidth = 1)
plt.plot([0,5], [-1/np.e,-1/np.e], '--k', linewidth = 1)
plt.legend([r'$\pm \, 1/e$'])
splits = [0.635, 0.953, 1.839]
colors = pl.cm.viridis(np.linspace(0.1,0.9,201))
for i in range(len(gammas)):
    gamma = gammas[i]
    t = 0
    x = 1
    v = 0
    tArray = []
    xArray = []
    while t < tmax:
        t += dt
        rungeKuttaStep()
        tArray.append(t)
        xArray.append(x)
    tDict[gamma] = tArray
    xDict[gamma] = xArray
    taus.append(getTau(xArray, tArray))
    if i % 5 == 0:
        plt.plot(tArray[0:len(tArray)//4], xArray[0:len(tArray)//4], color=colors[i], linewidth = 1)
    if gamma in redGammas:
        plt.plot(tArray[0:len(tArray)//4], xArray[0:len(tArray)//4], color=[1,0.1,0.1], linewidth = 1)
plt.xlabel(r'$t$')
plt.ylabel(r'$x$')
plt.title(r'$x(t)$')
plt.savefig('assets3/gamma-scatter.png', dpi = 300)
plt.clf()

for i in range(0, len(gammas)-1, 5):
    plt.plot(gammas[i:i+6], taus[i:i+6], color = colors[i], zorder = 1, linewidth = 3)
for i in range(len(gammas)):
    if gammas[i] in redGammas:
        plt.scatter(gammas[i], taus[i], color=[1,0.1,0.1], s = 15, marker = 'o', zorder = 2)
plt.xlabel(r'$\gamma$')
plt.ylabel(r'$\tau$')
plt.title(r'$\tau( \gamma)$')
plt.savefig('assets3/tau-to-gamma.png', dpi = 300)

# ----------------------------------- 1.3.c

plt.clf()

gamma = 4
t = 0.	             # start time
tmax = 30
dt = 0.01
x = 1
v = 0
omega0 = 3
foundGammac = False

while not foundGammac:
    gamma += 0.01
    t = 0
    x = 1
    v = 0
    tArray = []
    xArray = []
    vArray = []
    ifGammacIsFoundThisIsTrueAtEndOfLoop = True
    while t < tmax:
        t += dt
        rungeKuttaStep()
        tArray.append(t)
        xArray.append(x)
        vArray.append(v)
        if x < 0:
            ifGammacIsFoundThisIsTrueAtEndOfLoop = False
            break
    if ifGammacIsFoundThisIsTrueAtEndOfLoop:
        foundGammac = True

plt.plot(tArray[0:len(tArray)//10], xArray[0:len(tArray)//10], linewidth = 1)
plt.plot(tArray[0:len(tArray)//10], vArray[0:len(tArray)//10], linewidth = 1)
plt.plot([0,tmax/10],[0,0],'--k', linewidth = 1)
plt.title(r'$\gamma_c = $' + str(round(gamma, 2)))
plt.legend(['x(t)', 'v(t)', 'x = 0'])
plt.xlabel('t')
# plt.show()
plt.savefig('assets3/gammac.png', dpi = 300)

# --------------- Colorbar0.5+4*i/100

plt.clf()
colors = pl.cm.viridis(np.linspace(0.1,0.9,100))

for i in range(100):
    x = [0.5+4*i/100, 0.5+3.5*(i+1)/100]
    y = [0,0]
    plt.plot(x, y, color=colors[i], linewidth=55, zorder = 1)
    plt.axis([0.5,4,0,0.1])
plt.plot([0.5,4.5], [0.01,0.01], 'k', zorder = 2, linewidth = 0.5)
plt.title(r'$\gamma$')
plt.xlabel(r'$\gamma$')
plt.savefig('assets3/colorbar.png', dpi = 300)
# plt.show()
