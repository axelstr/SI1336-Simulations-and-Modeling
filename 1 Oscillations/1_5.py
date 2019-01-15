# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 1.5

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

# -------------------------- GLOBAL ------------------------------- #

t = 0.	             # start time
tmax = 1000.
dt = 0.1
x0 = 1
v0 = 0
c = 9                # c=g/L=9

g = 9.8              # gravitational acceleration
m = 1                # mass of the pendulum bob
L=g/c                # string length

## Functions

def a(x):
    return - c*x

def verletStep():
    global accel, v, x
    x_old = x
    v_old = v

    accel_old = a(x_old)
    x_new = x_old + v_old * dt + 1/2*accel_old * dt**2
    accel_new = a(x_new)
    v_new = v_old + 1/2 * ( accel_new + accel_old ) * dt

    x = x_new
    v = v_new

def leapFrog_vStep():
    global accel, v, x
    v = v + a(x) * dt

def leapFrog_xStep():
    global accel, v, x
    x = x + v * dt

def getAvarageEnergies(xArray, vArray):
    """This function finds the avarage potential, kenitic and total energies
    x(t) and v(t) in a pendlum."""
    avarageEk, avarageEp, avarageEtot = 0, 0, 0

    for x in xArray:
        avarageEp += 0.5*m*g*L*x**2
    avarageEp /= len(xArray)

    for v in vArray:
        avarageEk += 0.5*m*L**2*v**2
    avarageEk /= len(vArray)

    avarageEtot = avarageEk + avarageEp

    return avarageEp, avarageEk, avarageEtot

tArray = []
thetaArray = []
dthetaArray = []

# ------------------------ verlet

t = 0.	             # start time
x = x0
v = v0

tVerlet = [t]
xVerlet = [x]
vVerlet = [v]
eVerlet = [0.5*m*L**2*v**2 + 0.5*m*g*L*x**2]

while t < tmax:
    t += dt
    verletStep()
    tVerlet.append(t)
    xVerlet.append(x)
    vVerlet.append(v)
    eVerlet.append(0.5*m*L**2*v**2 + 0.5*m*g*L*x**2)

avarageEpVerlet, avarageEkVerlet, avarageEtotVerlet = getAvarageEnergies(xVerlet, vVerlet)

# ------------------------ leapfrog

t = 0.
x = x0
tLeapFrog_x, xLeapFrog = [t], [x]
t = t + dt/2
v = v0 + a(x)*dt/2
tLeapFrog_v, vLeapFrog = [t], [v]
eLeapFrog = [0.5*m*L**2*v0**2 + 0.5*m*g*L*x**2]

while t < tmax:
    t += dt/2
    x = x + v * dt
    xLeapFrog.append(x)
    tLeapFrog_x.append(t)

    t += dt/2
    v = v + a(x) * dt
    tLeapFrog_v.append(t)
    vLeapFrog.append(v)

    vStepAvarage = (vLeapFrog[-1] + vLeapFrog[-2])/2
    eLeapFrog.append(0.5*m*L**2*vStepAvarage**2 + 0.5*m*g*L*x**2)

avarageEpLeapFrog, avarageEkLeapFrog, avarageEtotLeapFrog = getAvarageEnergies(xLeapFrog, vLeapFrog)

# -------------------- Exact

sqc = np.sqrt(c)
tExact = np.linspace(0,tmax, int(tmax/dt))
xExact = x0*np.cos(sqc*tExact)
vExact = -sqc*x0*np.sin(sqc*tExact)
eExact = 0.5*m*L**2*vExact**2 + 0.5*m*g*L*xExact**2

avarageEpExact, avarageEkExact, avarageEtotExact = getAvarageEnergies(xExact, vExact)

# -------------------------- Plot

blue = pl.cm.Blues(0.7)
orange = pl.cm.Oranges(0.5)
green = pl.cm.Greens(0.7)
purple = pl.cm.Purples(0.7)

endIndex = len(tVerlet)//100

plt.plot([0],[0], 'k', linestyle = '-')
plt.plot([0],[0], 'k', linestyle = '--')
plt.plot([0],[0], 'k', linestyle = ':')

plt.plot(tVerlet[0:endIndex], xVerlet[0:endIndex], color = blue, linestyle = '-', linewidth = 1)
plt.plot(tVerlet[0:endIndex], vVerlet[0:endIndex], color = orange, linestyle = '-', linewidth = 1)
plt.plot(tVerlet[0:endIndex], eVerlet[0:endIndex], color = green, linestyle = '-', linewidth = 1)

plt.plot(tLeapFrog_x[0:endIndex], xLeapFrog[0:endIndex], color = blue, linestyle = '--', linewidth = 1.8)
plt.plot(tLeapFrog_v[0:endIndex], vLeapFrog[0:endIndex], color = orange, linestyle = '--', linewidth = 1.8)
plt.plot(tLeapFrog_x[0:endIndex], eLeapFrog[0:endIndex], color = green, linestyle = '--', linewidth = 1.8)

plt.plot(tExact[0:endIndex], xExact[0:endIndex], color = blue, linestyle = ':', linewidth = 1)
plt.plot(tExact[0:endIndex], vExact[0:endIndex], color = orange, linestyle = ':', linewidth = 1)
plt.plot(tExact[0:endIndex], eExact[0:endIndex], color = green, linestyle = ':', linewidth = 1)

plt.title('Verlet and Leap-frog methods \n dt = ' + str(dt))
plt.xlabel('t')
plt.legend([
    'verlet',
    'leap-frog',
    'analytical solution',
    r'$x(t)$',
    r'$\dot x (t)$',
    r'$E$'
])
plt.savefig('assets5/verletandleapfrog.png', dpi=300)
# plt.show()

## Only energies plot

plt.clf()
endIndex = len(tVerlet)//100

plt.plot([0],[5.25], 'k', linestyle = '-')
plt.plot([0],[5.25], 'k', linestyle = '--')
plt.plot([0],[5.25], 'k', linestyle = ':')
plt.plot([0],[5.25], color = green, linestyle = '-')
plt.plot([0],[5.25], color = purple, linestyle = '-')

plt.plot(tVerlet[0:endIndex], eVerlet[0:endIndex], color = green, linestyle = '-', linewidth = 1)
plt.plot(tLeapFrog_x[0:endIndex], eLeapFrog[0:endIndex], color = green, linestyle = '--', linewidth = 1.8)
plt.plot(tExact[0:endIndex], eExact[0:endIndex], color = green, linestyle = ':', linewidth = 1)

plt.plot([0, 10], [avarageEtotVerlet, avarageEtotVerlet], color = purple, linestyle = '-', linewidth = 1)
plt.plot([0, 10], [avarageEtotLeapFrog, avarageEtotLeapFrog], color = purple, linestyle = '--', linewidth = 1.8)
plt.plot([0, 10], [avarageEtotExact, avarageEtotExact], color = purple, linestyle = ':', linewidth = 1)


plt.title('Verlet and Leap-frog methods \n Energies')
plt.xlabel('t')
plt.legend([
    'verlet',
    'leap-frog',
    'analytical solution',
    r'$E$',
    r'$E_{avarage}$',
])
plt.savefig('assets5/verletandleapfrog-energies.png', dpi=300)
# plt.show()

# ------------------- Print outs

print('Avarage energies (print for latex):')
print('\\begin{tabular}{c|c|c|c}')
print(' & $E_p$ & $E_k$ & $E_\\text{tot}$ \\\\ ')
print('\\hline')
print('Verlet & ' + str(round(avarageEpVerlet, 3)) +'&'+ str(round(avarageEkVerlet, 3)) +'&' + str(round(avarageEtotVerlet, 3)) + '\\\\')
print('\\hline')
print('Leap-frog & ' + str(round(avarageEpLeapFrog, 3)) +'&'+ str(round(avarageEkLeapFrog, 3)) +'&' + str(round(avarageEtotLeapFrog, 3)) + '\\\\')
print('\\hline')
print('Analytical & ' + str(round(avarageEpExact, 3)) +'&'+ str(round(avarageEkExact, 3)) +'&' + str(round(avarageEtotExact, 3)))
print('\\end{tabular}')
