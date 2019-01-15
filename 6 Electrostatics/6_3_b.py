# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 6.3 b)

# ------------------------- Import Libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.optimize import curve_fit
from pylab import cm as plcm            # colors for plotting
import pickle                           # for storing calculations and reading again while editing plot details

plt.rcParams.update({'font.size': 12})

# ------------------------- Set global values

nToExamine = [4]                    # assignment
tolerance = 0.001                    # max relatice error from exact solution

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
        v[i,n] = 1
    # Exact solution
    vExact = np.copy(v)
    for i in range(1,n):
        for j in range(1,n):
            vExact[i,j] = 1
    # Initial guess
    for i in range(1,n):
        for j in range(1,n):
            v[i,j] = 0*vExact[i,j]

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
    and then uses relax() until v is within tolerance.
    1. Iterate for n = 5, 10
    2. Iterate for the range of n in nArray"""
    global v, vNew, n, stepsToToleranceArray
    stepsToToleranceArray = []
    for n in nToExamine:
        print('Currently working with n = ', n)
        initiateVMatrixes()
        step = 0
        toleranceAcqurired = False
        while not toleranceAcqurired:
            print(v)
            step+=1
            relax_checker()
            # Controll accuracy
            toleranceAcqurired = True   # run through v and set false if not acquired
            for i in range(1,n):
                for j in range(1,n):
                    if np.abs( (v[i,j]-vExact[i,j])/vExact[i,j] ) > tolerance:
                        toleranceAcqurired = False
            if toleranceAcqurired:
                stepsToToleranceArray.append(step)
    print('n:', nToExamine,'\nstepsToTolerance:', stepsToToleranceArray)

# --------------------------- Main

calculate()
