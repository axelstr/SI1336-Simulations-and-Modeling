# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 1.2

import numpy as np
import matplotlib.pyplot as plt

# -------------------------- GLOBAL ------------------------------- #

t = 0.	             # start time
dt = 0.001
theta0_array_divpi = np.linspace(0.1 , 0.9, 101)
theta0_array = np.pi*theta0_array_divpi     # initial position
dtheta = 0.          # initial velocity
c = 9    # c = g/L

## Storage

THarmonic_array = []      # store T  corresponding to theta_array
TPendulum_array = []      # store T corresponding to theta_array
TSeries_array = []


# ------------------------ HARMONIC OSCILLATOR ------------------- #

for theta0 in theta0_array:
    THarmonic_array.append(2*np.pi*np.sqrt(1/c))

# ------------------------ PENDULUM ----------------------------- #

def rungeKuttaStep():
    global accel, dtheta, theta, periodCounter
    def a(x):
        return -c*np.sin(x)         # pendulum
    x = theta
    v = dtheta
    a1 = a(x)           * dt
    b1 = v              * dt
    a2 = a(x+b1/2)      * dt
    b2 = (v+a1/2)       * dt
    a3 = a(x + b2/2)    * dt
    b3 = (v+a2/2)       * dt
    a4 = a(x + b3)      * dt
    b4 = (v+a3)         * dt

    dtheta +=   1/6 * (a1+2*a2+2*a3+a4)
    theta +=    1/6 * (b1+2*b2+2*b3+b4)

    if v > 0 and dtheta <= 0: periodCounter +=1

## Plot example

periodCounter = 0
t = 0.	             # start time
theta = 0.3 * np.pi  # initial position
dtheta = 0.          # initial velocity
time = []            # list to store time
pos = []             # list to store angular position
vel = []             # list to store angular velocity
while periodCounter < 10:
    t += dt
    rungeKuttaStep()
    time.append(t)
    pos.append(theta)
    vel.append(dtheta)
plt.plot(time,pos)
plt.plot(time,vel)
tstr = str(round(t,1))
Tstr = str(round(t/10,2))
plt.legend([r'$\theta(t)$',r'$\dot \theta (t)$'])
plt.xlabel(r'$t$')
plt.ylabel('Amplitude')
plt.title(r'$\theta_0 = 0.3 \pi$' + '\n' + r'T = ' + tstr + '/10 = '+ Tstr + 's' + '\n' + r'$g/l = 9$')
plt.savefig('assets2/example.png', dpi=300)

## Run for all theta0

for theta0 in theta0_array:
    periodCounter = 0
    theta = theta0
    t = 0.	             # start time
    dtheta = 0.          # initial velocity
    while periodCounter < 10:
        t += dt
        rungeKuttaStep()
    TPendulum_array.append(t/10)

# -------------------------- T SERIES ---------------------------- #

def T(th0):
    return 2*np.pi*np.sqrt(1/c) * (1 + 1/16*th0**2+11/3072*th0**4 + 173/737280*th0**6)

for theta0 in theta0_array:
    TSeries_array.append(T(theta0))

# -------------------------- PLOT -----------------------------#

plt.clf()
plt.plot(theta0_array_divpi, THarmonic_array)
plt.plot(theta0_array_divpi, TPendulum_array)
plt.plot(theta0_array_divpi, TSeries_array)
plt.legend(['harmonic oscillator', 'pendulum', 'peturbation series'])
plt.xlabel(r'$\theta_0 / \pi$')
plt.ylabel(r'period time, $T$')
plt.savefig('assets2/t_to_theta0.png', dpi = 300)
