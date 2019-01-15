# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 1.4

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

# -------------------------- GLOBAL ------------------------------- #

t = 0.	             # start time
tmax = 30.
dt = 0.01
theta = np.pi/2
dtheta = 0

## Functions

def a(theta,dtheta):
    return - 9*np.sin(theta) - 1*dtheta

def rungeKuttaStep():
    global theta, dtheta
    x = theta
    v = dtheta

    a1 = a(x,v)             * dt
    b1 = v                  * dt
    a2 = a(x+b1/2, v+a1/2)  * dt
    b2 = (v+a1/2)           * dt
    a3 = a(x+b2/2, v+a2/2)  * dt
    b3 = (v+a2/2)           * dt
    a4 = a(x+b3, v+a3)      * dt
    b4 = (v+a3)             * dt

    dtheta +=    1/6 * (a1+2*a2+2*a3+a4)
    theta  +=    1/6 * (b1+2*b2+2*b3+b4)


tArray = []
thetaArray = []
dthetaArray = []

while t < tmax:
    t += dt
    rungeKuttaStep()
    tArray.append(t)
    thetaArray.append(theta)
    dthetaArray.append(dtheta)

plt.plot(tArray[0:len(tArray)//4], thetaArray[0:len(tArray)//4], linewidth = 1)
plt.plot(tArray[0:len(tArray)//4], dthetaArray[0:len(tArray)//4], linewidth = 1)
plt.plot([0,tmax/4],[0,0], '--k', linewidth = 1)
plt.xlabel('t')
plt.legend([r'$\theta(t)$',r'$\dot \theta (t)$'])
plt.title(r'Damped pendulum')
plt.savefig('assets4/thetadtheta-to-t.png', dpi = 300)
# plt.show()

plt.clf()
plt.plot(thetaArray, dthetaArray, linewidth = 1)
plt.arrow(thetaArray[3], dthetaArray[3], thetaArray[3]-thetaArray[1], dthetaArray[2]-dthetaArray[1], head_width=1/10, color='C0')
plt.plot([-1.5, 2],[0,0], '--k', linewidth = 1)
plt.plot([0,0],[-3.5, 2.0], '--k', linewidth = 1)
plt.xlabel(r'$\theta$')
plt.ylabel(r'$\dot \theta$')
plt.axis('equal')
plt.title(r'$\dot \theta$ vs $\theta$')
plt.savefig('assets4/dtheta-to-theta.png', dpi = 300)
# plt.show()
