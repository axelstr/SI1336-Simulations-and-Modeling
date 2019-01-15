# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 6.3 a)

# ------------------------- Import Libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.optimize import curve_fit
from pylab import cm as plcm            # colors for plotting
import pickle                           # for storing calculations and reading again while editing plot details

plt.rcParams.update({'font.size': 12})

# ------------------------- Set global values

nToExamine = [5,10]                 # assignmet
nArray = [n for n in range(2,51)]   # range to find dependence on n
tolerance = 0.01                    # max relatice error from exact solution
nMax = 4

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
        v[0,i] = 10
        v[n,i] = 10
        v[i,0] = 10
        v[i,n] = 10

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

def calculate():
    """Main calculation function that first initalizes with initiateVMatrixes()
    and then uses relax() until v is within tolerance."""
    global v, vNew, n, stepsToToleranceArray
    n = 2
    initiateVMatrixes()
    v[1,1] = (v[0,1]+v[2,1]+v[1,0]+v[1,2]) * 1/4
    print(v)
    while n < nMax:
        print('Currently working with n = ', n)
        generateFinerGrid()
        relax_multigrid()
        print(v)

def loadDataFromFile():
    """Imports stored data from file from previos calculation. Useful when
    fixing the plot. Obs, obly works when running the exact same iteartion,
    change nArray or nToExamine and you need to calculate again. Imports
    variables:
    - stepsToToleranceArray"""
    global stepsToToleranceArray, stepsToToleranceArray_a, stepsToToleranceArray_1a
    with open('assets3/a.pkl', 'rb') as file:
        stepsToToleranceArray = pickle.load(file)

def storeDataToFile():
    """Stores data to file from current calculation. Stores variables:
    - stepsToToleranceArray"""
    global stepsToToleranceArray
    with open('assets3/a.pkl', 'wb') as file:
        pickle.dump(stepsToToleranceArray, file)

# ----------------------- Main

calculate()

# ----------------------- Plot

# common plot values
commonLinewidth = 2

plt.subplot(2,1,1) # linear plot
plt.plot(nArray, stepsToToleranceArray,
        linewidth = commonLinewidth,
        linestyle = '--',
        marker = '.',
        markersize = 8,
        color = 'm',
        zorder = 2)
plt.plot(nArray, stepsToToleranceArray_a,
        linewidth = commonLinewidth,
        linestyle = '-',
        marker = 'x',
        markersize = 8,
        color = 'b',
        zorder = 1)
plt.plot(nArray, stepsToToleranceArray_1a,
        linewidth = commonLinewidth,
        marker = '.',
        markersize = 8,
        color = 'c',
        zorder = 0)
plt.title(r'Steps required to reach tolerance')
plt.legend(['2. b) - Checker relaxation', '2. a) - Gauss-Seidel', '1. a) - first numerical method'])
plt.ylabel(r'steps')

plt.subplot(2,1,2) # loglog plot
# calculate regression from n = 10 and up
log_nArray = [np.log(n) for n in nArray]
log_stepsToToleranceArray = [np.log(steps) for steps in stepsToToleranceArray]
def f(x,k,m):
    return k*x+m
[k,m], _ = curve_fit(f, log_nArray[10:], log_stepsToToleranceArray[10:])
# plot loglog with regression
plt.loglog(nArray, [np.e**f(x,k,m) for x in log_nArray],
        linewidth = commonLinewidth,
        linestyle = '--',
        zorder = 3,
        color = 'r')
plt.loglog(nArray, stepsToToleranceArray,
        linewidth = commonLinewidth,
        color = 'm',
        marker = '.',
        markersize = 8)
plt.legend([r'log(steps)$ = %s \, \log(n) - %s$'%(round(k,3), round(np.abs(m),3))],
        fancybox = True)
plt.xlabel(r'$n$')
plt.ylabel(r'steps')
plt.savefig('assets2/b.png', dpi = 300)
plt.show()
