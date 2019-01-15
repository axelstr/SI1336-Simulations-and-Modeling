# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 6.3 c)

# ------------------------- Import Libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.optimize import curve_fit
from pylab import cm as plcm            # colors for plotting
import pickle                           # for storing calculations and reading again while editing plot details

plt.rcParams.update({'font.size': 12})

# ------------------------- Set global values

tolerance = 0.01                    # max relatice error from exact solution
nMax = 100

# storage
nArray = []
stepsToToleranceArray = []

# ------------------------- Define functions

def initiateVMatrixes():
    """Initiates potential matrixes.
    - v has boundary values and initial guess of 9 everywhere else
    - vNew is a copy of v
    - vExact is the exact analytical solution, 10 everywhere"""
    global v, vExact
    # Initialize the grid to 0
    v = np.zeros((n+1, n+1))        # matrix of v, index are i: row, j:column
    # Set the boundary conditions
    for i in range(1,n):
        v[0,i] = 1
        v[n,i] = 1
        v[i,0] = 1
        v[i,n] = 0.5
    v[0,0] = 1
    v[n,0] = 1

def generateFinerGrid():
    global v, n
    vCoarse = np.copy(v)
    n = n*2
    initiateVMatrixes()
    for i in range(1,n//2):
        for j in range(1,n//2):
            v[2*i,2*j] = vCoarse[i,j]

def relax_multigrid():
    """One checker-relax iteration. v[i,j] is set as the avarage of its neighbours."""
    global v
    for i in range(1,n):        # first sweep
        for j in range(1,n):
            if i % 2 == 1:
                if j % 2 == 0:
                    v[i,j] =  (v[i-1,j]+v[i+1,j]) * 1/2
            if i % 2 == 0:
                if j % 2 == 1:
                    v[i,j] =  (v[i,j-1]+v[i,j+1]) * 1/2
    for i in range(1,n):        # second sweep
        for j in range(1,n):
            if i % 2 == 1:
                if j % 2 == 1:
                    v[i,j] = (v[i-1,j]+v[i+1,j]+v[i,j-1]+v[i,j+1]) * 1/4
            if i % 2 == 0:
                if j % 2 == 0:
                    v[i,j] = (v[i-1,j]+v[i+1,j]+v[i,j-1]+v[i,j+1]) * 1/4

def relax_checker():
    """One checker-relax iteration. v[i,j] is set as the avarage of its neighbours."""
    checker = 2
    global v, vNew, n
    for check in range(0,2):
        for x in range(1,n):
            for y in range(1,n):
                if (x*(n+1) + y) % 2 == check:
                    v[x,y] = (v[x-1][y] + v[x+1][y] + v[x][y-1] + v[x][y+1])*0.25

def calculate():
    """Main calculation function that first initalizes with initiateVMatrixes()
    and then uses relax() until v is within tolerance."""
    global v, vNew, n, stepsToToleranceArray
    step = 0
    n = 2
    initiateVMatrixes()
    v[1,1] = (v[0,1]+v[2,1]+v[1,0]+v[1,2]) * 1/4
    step += 1
    while n < nMax:
        print('Currently working with n = ', n)
        generateFinerGrid()
        relax_multigrid()
        step += 1
        toleranceAcqurired = False
        while not toleranceAcqurired:
            if step%100==0:print('v =',v,'\nstep =',step)
            vOld = np.copy(v)
            relax_checker()
            step += 1
            # Controll accuracy
            toleranceAcqurired = True   # run through v and set false if not acquired
            for i in range(1,n):
                for j in range(1,n):
                    if np.abs( (v[i,j]-vOld[i,j])/vOld[i,j] ) > tolerance:
                        toleranceAcqurired = False
        nArray.append(n)
        stepsToToleranceArray.append(step)

# ----------------------- Main

calculate()         # comment to obly load data

# ----------------------- Plot

# common plot values
commonLinewidth = 2

fig, axs = plt.subplots(1,2)    # one subplot for each boundary conditions
fig.set_size_inches(8,5)
[ax1, ax2] = axs

ax1.set_title('Steps required to meet tolerance')
ax2.set_title('V(x,y)')


# calculate regression
def f(x,k,m):
    return k*np.log(x)/np.log(2)+m
[k,m], _ = curve_fit(f, nArray, stepsToToleranceArray)
nSpace = np.linspace( nArray[0], nArray[-1], 1001 )
ax1.plot(nSpace, [f(x,k,m) for x in nSpace],
        linewidth = commonLinewidth,
        linestyle = '--',
        zorder = 3,
        color = 'r')
# plot steps required
ax1.plot(nArray, stepsToToleranceArray,
        linewidth = commonLinewidth,
        linestyle = '-',
        marker = '.',
        markersize = 8,
        color = 'b',
        zorder = 2)

ax1.legend([
        r'$%s \, \log_{2}(n) - %s$'%(round(k,3), round(np.abs(m),3))
        ],
        fancybox = True)
ax1.set_xlabel('n')
ax1.set_ylabel('steps')


# plot V
# 1 plot potential with colormap
im2 = ax2.imshow(v,            # plot first result
        cmap='bone',
        interpolation='bicubic')
fig.colorbar(im2, ax = axs,     # add colorbar below plots
        orientation='horizontal',
        fraction=.1,
        label='V(x,y)')
# 2 add contour
cs2 = ax2.contour(v,           # add first contour
        levels=np.arange(0, 1.05, 0.05),
        colors='red',
        alpha=0.3)    # transparency
# 3 add countour labels
plt.clabel(cs2, inline=1, fontsize=10)  # add labels for second contour

# save
plt.savefig('assets3/c.png', dpi=300)
plt.show()
