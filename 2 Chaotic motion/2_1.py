# Axel Stromberg
# axelstr@kth.se
# SI1136
# Project 2.1

#!/usr/bin/python

from pylab import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# matplotlib.rcParams.update({'font.size': 20})

plt.figure(figsize=(8,6))

# ----------------------------- r > r_\infty

nsteps = 201      # total number of steps

r = 0.91         # the parameter
x = 0.5          # initial x (seed)

plot_start = 0   # start the plot at this step

vs = [ ]
vx = [ ]

for step in range(0,nsteps):
    if step >= plot_start:
        vs.append(step)
        vx.append(x)

    x = 4*r*x*(1 - x)

r = 0.91         # the parameter
x = 0.5          # initial x (seed)

vsRound = [ ]
vxRound = [ ]

for step in range(0,nsteps):
    if step >= plot_start:
        vsRound.append(step)
        vxRound.append(x)

    x = round(4*r*x*(1 - x),6)



plt.ylim(0,1)
plt.scatter(vs, vx, c='b', s=2)
plt.scatter(vsRound, vxRound, c='r', s=2)

plt.xlabel(r'$n$')
plt.ylabel(r'$x_n$')
plt.title(r'Population model $x_{n+1} = f(x_n)$' + '\n' + r'$f(x_n) = 4\cdot0.91x_n(1-x_n)$')
plt.legend([r'$x_{n+1} = f(x_n)$', r'$x_{n+1} = $round($f(x_n)$, 6)'])
plt.tight_layout()
plt.savefig('assets1/plot1.png', dpi = 300)
plt.show()

# ----------------------- r < r_\infty

nsteps = 201      # total number of steps
plot_start = 0   # start the plot at this step



r = 0.87         # the parameter
x = 0.5          # initial x (seed)
vs = [ ]
vx = [ ]

for step in range(0,nsteps):
    if step >= plot_start:
        vs.append(step)
        vx.append(x)

    x = 4*r*x*(1 - x)

r = 0.87         # the parameter
x = 0.5          # initial x (seed)
vsRound = [ ]
vxRound = [ ]

for step in range(0,nsteps):
    if step >= plot_start:
        vsRound.append(step)
        vxRound.append(x)

    x = round(4*r*x*(1 - x),6)

plt.clf()
plt.ylim(0,1)
plt.scatter(vs, vx, c='b', s=2)
plt.scatter(vsRound, vxRound, c='r', s=2)

plt.xlabel(r'$n$')
plt.ylabel(r'$x_n$')
plt.title(r'Population model $x_{n+1} = f(x_n)$' + '\n' + r'$f(x_n) = 4\cdot0.87x_n(1-x_n)$')
plt.legend([r'$x_{n+1} = f(x_n)$', r'$x_{n+1} = $round($f(x_n)$, 6)'])
plt.tight_layout()
plt.savefig('assets1/plot2.png', dpi = 300)
plt.show()
