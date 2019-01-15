# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 1.1

import numpy as np
import matplotlib.pyplot as plt

# -------------------------- GOBAL ------------------------------- #


t = 0.	             # start time
tmax = 30.	     # final time
dt_array = [0.01, 0.05, 0.1]           # time step
theta_array = [np.pi*0.1,np.pi*0.3,np.pi*0.5]     # initial position
dtheta = 0.          # initial velocity
g = 9.8              # gravitational acceleration
m = 1                # mass of the pendulum bob
c = 9                # c=g/L=9
L=g/c                # string length

# -------------------------- EXACT SOLUTION ------------------------- #

nameCounter = 0
xExactDict = {}
thetaExactDict = {}
dthetaExactDict = {}
energyExactDict = {}

for theta0 in theta_array:
    nameCounter += 1
    x_exact = np.linspace(t,tmax,501)
    theta_exact = theta0*np.cos(3*x_exact)
    dtheta_exact = -3*theta0*np.sin(3*x_exact)
    energy_exact = 0.5*m*L**2*dtheta_exact**2 + 0.5*m*g*L*theta_exact**2
    plt.clf()
    xExactDict[theta0] = x_exact
    thetaExactDict[theta0] = theta_exact
    dthetaExactDict[theta0] = dtheta_exact
    energyExactDict[theta0] = energy_exact
    plt.plot(xExactDict[theta0], thetaExactDict[theta0], 'b', linestyle = '--', linewidth=1)
    plt.plot(xExactDict[theta0], dthetaExactDict[theta0], 'orange', linestyle = '--', linewidth=1)
    plt.plot(xExactDict[theta0], energyExactDict[theta0], 'g', linestyle = '--', linewidth=1)
    plt.legend([r'$\theta(t)$',r'$\dot \theta(t)$',r'$E$'])
    plt.title(r'Harmonic oscillator exact solution.' + '\n' \
            + r'$\theta_0 = $' + str(theta0/np.pi) + r'$\pi$')
    plt.savefig('assets/1_1_plot_0_'+str(nameCounter)+'.png', dpi = 300)


# -------------------------- PENDULUM ------------------------------- #

def eulerStep():
    """Stepmethod Euler."""
    global accel, dtheta, theta
    accel = -c * np.sin(theta)     # pendulum
    #accel = -c * theta             # harmonic oscillator
    theta += dtheta * dt
    dtheta += accel * dt

def eulerChromerStep():
    """Stepmethod Euler-Chromer."""
    global accel, dtheta, theta
    accel = -c * np.sin(theta)     # pendulum
    #accel = -c * theta             # harmonic oscillator
    dtheta += accel * dt
    theta += dtheta * dt

def verletStep():
    global accel, dtheta, theta
    accel = -c * np.sin(theta)     # pendulum
    #accel = -c * theta             # harmonic oscillator
    theta += dtheta * dt + 1/2*accel * dt**2
    accel_new = -c * np.sin(theta)
    #accel_new = -c * theta             # harmonic oscillator
    dtheta += 1/2*(accel_new+accel) * dt

def rungeKuttaStep():
    global accel, dtheta, theta, pendulumBool
    def a(x):
        return -c*np.sin(x)         # pendulum
        # return -c*theta           # harmonic oscillator
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

# methods = ['Euler','Euler-Chromer', 'Verlet', 'Runge-Kutta']
methods = ['Euler-Chromer', 'Verlet', 'Runge-Kutta']
stepFunctions = {
    'Euler' : eulerStep,
    'Euler-Chromer': eulerChromerStep,
    'Verlet': verletStep,
    'Runge-Kutta': rungeKuttaStep
}

nameCounter = 0

for method in methods:
    methodFunction = stepFunctions[method]
    for theta0 in theta_array:
        for dt in dt_array:
            nameCounter += 1
            N = int(tmax/dt)         # number of steps
            theta = theta0
            t = 0.	             # start time
            dtheta = 0.          # initial velocity
            time = []            # list to store time
            pos = []             # list to store angular position
            vel = []             # list to store angular velocity
            energy = []          # list to store energy
            for i in range(N):
                t += dt
                methodFunction()
                time.append(t)
                pos.append(theta)
                vel.append(dtheta)
                energy.append( 0.5*m*L**2*dtheta**2 + m*g*L*(1.-np.cos(theta)) )     # pendulum
                # energy.append( 0.5*m*L**2*dtheta**2 + 0.5*m*g*L*theta**2 )            # harmonic oscillator

            plt.clf()
            plt.plot(time,pos, linewidth=1)
            plt.plot(time,vel, linewidth=1)
            plt.plot(time,energy, linewidth=1)
            title = r'Method: '+method+r'    (pendulum)'+'\n' \
                    + r' $\theta_0 = $' + str(theta0/np.pi) + r'$\pi$' + '\n' \
                    + 'dt = ' + str(dt)
            plt.title(title)
            plt.xlabel(r'time')
            plt.legend([r'$\theta(t)$',r'$\dot \theta(t)$', r'$E(t)$'])
            plt.plot(xExactDict[theta0], thetaExactDict[theta0], 'b', linestyle = '--', linewidth=1)
            plt.plot(xExactDict[theta0], dthetaExactDict[theta0], 'orange', linestyle = '--', linewidth=1)
            plt.plot(xExactDict[theta0], energyExactDict[theta0], 'g', linestyle = '--', linewidth=1)
            filename = 'plots/pendulum_' + str(nameCounter) \
                        + '_' + method \
                        + '_theta0-is-'+str(theta0/np.pi).replace('.','-')+'pi' \
                        + '_dt-is-'+str(dt).replace('.','-') +'.png'
                        # plt.savefig(filename, dpi=300)
            filename = 'assets/1_1_plot_' + str(2*nameCounter-1) + '.png'
            plt.savefig(filename, dpi=300)

# -------------------------- HARMONIC OSCILLATOR ---------------------------- #

def eulerStep():
    """Stepmethod Euler."""
    global accel, dtheta, theta
    # accel = -c * np.sin(theta)     # pendulum
    accel = -c * theta             # harmonic oscillator
    theta += dtheta * dt
    dtheta += accel * dt

def eulerChromerStep():
    """Stepmethod Euler-Chromer."""
    global accel, dtheta, theta
    # accel = -c * np.sin(theta)     # pendulum
    accel = -c * theta             # harmonic oscillator
    dtheta += accel * dt
    theta += dtheta * dt

def verletStep():
    global accel, dtheta, theta
    # accel = -c * np.sin(theta)     # pendulum
    accel = -c * theta             # harmonic oscillator
    theta += dtheta * dt + 1/2*accel * dt**2
    # accel_new = -c * np.sin(theta)    # pendulum
    accel_new = -c * theta             # harmonic oscillator
    dtheta += 1/2*(accel_new+accel) * dt

def rungeKuttaStep():
    global accel, dtheta, theta
    def a(x):
        # return -c*np.sin(x)         # pendulum
        return -c*x           # harmonic oscillator
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

# methods = ['Euler','Euler-Chromer', 'Verlet', 'Runge-Kutta']
methods = ['Euler-Chromer', 'Verlet', 'Runge-Kutta']
stepFunctions = {
    'Euler' : eulerStep,
    'Euler-Chromer': eulerChromerStep,
    'Verlet': verletStep,
    'Runge-Kutta': rungeKuttaStep
}

nameCounter = 0

for method in methods:
    methodFunction = stepFunctions[method]
    for theta0 in theta_array:
        for dt in dt_array:
            nameCounter += 1
            N = int(tmax/dt)         # number of steps
            theta = theta0
            t = 0.	             # start time
            dtheta = 0.          # initial velocity
            time = []            # list to store time
            pos = []             # list to store angular position
            vel = []             # list to store angular velocity
            energy = []          # list to store energy
            for i in range(N):
                t += dt
                methodFunction()
                time.append(t)
                pos.append(theta)
                vel.append(dtheta)
                # energy.append( 0.5*m*L**2*dtheta**2 + m*g*L*(1.-np.cos(theta)) )     # pendulum
                energy.append( 0.5*m*L**2*dtheta**2 + 0.5*m*g*L*theta**2 )            # harmonic oscillator

            plt.clf()
            plt.plot(time,pos, linewidth=1)
            plt.plot(time,vel, linewidth=1)
            plt.plot(time,energy, linewidth=1)
            title = r'Method: '+method+r'    (harmonic oscilltor)'+'\n' \
                    + r' $\theta_0 = $' + str(theta0/np.pi) + r'$\pi$' + '\n' \
                    + 'dt = ' + str(dt)
            plt.title(title)
            plt.xlabel(r'time')
            plt.legend([r'$\theta(t)$',r'$\dot \theta(t)$', r'$E(t)$'])
            plt.plot(xExactDict[theta0], thetaExactDict[theta0], 'b', linestyle = '--', linewidth=1)
            plt.plot(xExactDict[theta0], dthetaExactDict[theta0], 'orange', linestyle = '--', linewidth=1)
            plt.plot(xExactDict[theta0], energyExactDict[theta0], 'g', linestyle = '--', linewidth=1)
            filename = 'plots/harmonic_' + str(nameCounter) \
                        + '_' + method \
                        + '_theta0-is-'+str(theta0/np.pi).replace('.','-')+'pi' \
                        + '_dt-is-'+str(dt).replace('.','-') +'.png'
            plt.savefig(filename, dpi=300)
            filename = 'assets/1_1_plot_' + str(2*nameCounter) + '.png'
            plt.savefig(filename, dpi=300)


# -------------------------- PRINT FOR LATEX BEAMER -----------------------------#

for i in range(1,55):
    print('\\begin{frame}')
    print('\\frametitle{}')
    print('\\includegraphics[width=\\textwidth]{assets/1_1_plot_'+str(i)+'.png}')
    print('\\end{frame}')
    print('\n')
