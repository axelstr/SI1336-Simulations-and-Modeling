# Axel Stromberg
# axelstr@kth.se
# SI1336
# Project 6.1 c)

# ------------------------- Import Libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.optimize import curve_fit
from pylab import cm as plcm            # colors for plotting
import pickle                           # for storing calculations and reading again while editing plot details

plt.rcParams.update({'font.size': 12})

# ------------------------- Set global values

n = 101
tolerance = 0.000001

# ------------------------- Define functions

def initiateVMatrixes_1():
    """Initiates potential matrixes with first boundary value: V = 10 on
    two opposing sides and 5 on the other two sides.
    - v has boundary values and initial guess of 9 everywhere else
    - vNew is a copy of v
    - vExact is the exact analytical solution, 10 everywhere"""
    global v, vNew
    # Initialize the grid to 0
    v = np.zeros((n+1, n+1))        # matrix of v, index are i: row, j:column
    # Set the boundary conditions
    for i in range(1,n):
        v[0,i] = 10
        v[n,i] = 10
        v[i,0] = 5
        v[i,n] = 5
    # Initial guess
    for i in range(1,n):
        for j in range(1,n):
            v[i,j] = 7.5
    vNew = np.copy(v)

    v = np.copy(v1)
    vNew = np.copy(v1)


def initiateVMatrixes_2():
    """Initiates potential matrixes with second boundary conditions: V = 10 on
    three sides and 0 on the fourth.
    - v has boundary values and initial guess of 9 everywhere else
    - vNew is a copy of v
    - vExact is the exact analytical solution, 10 everywhere"""
    global v, vNew
    # Initialize the grid to 0
    v = np.zeros((n+1, n+1))        # matrix of v, index are i: row, j:column
    # Set the boundary conditions
    for i in range(1,n):
        v[0,i] = 10
        v[n,i] = 10
        v[i,0] = 10
        v[i,n] = 0
    v[0,0]=10; v[n,0]=10
    # Initial guess
    for i in range(1,n):
        for j in range(1,n):
            v[i,j] = 10-(j/(n-1))*10
    vNew = np.copy(v)

    v = np.copy(v2)
    vNew = np.copy(v2)

def relax():
    """One relax iteration. v[i,j] is set as the avarage of its neighbours."""
    global v, vNew, n
    for x in range(1,n):
        for y in range(1,n):
            vNew[x,y] = (v[x-1][y] + v[x+1][y] + v[x][y-1] + v[x][y+1])*0.25
    for x in range(1,n):
        for y in range(1,n):
            v[x,y] = vNew[x,y]

def calculate():
    """Main calculation function that first initalizes with initiateVMatrixes()
    and then uses relax() until v is within tolerance.
    1. First boundary coditions
    2. Second boundary conditions"""
    global v, vNew, n, v1, v2

    # First bondary conditions
    initiateVMatrixes_1()
    step = 0
    toleranceAcqurired = False
    while not toleranceAcqurired:
        if step%100==0:print('v =',v,'\nstep =',step)
        step+=1
        vOld = np.copy(v)
        relax()
        # Controll accuracy
        toleranceAcqurired = True   # run through v and set false if not acquired
        for i in range(1,n):
            for j in range(1,n):
                if np.abs( (v[i,j]-vOld[i,j])/vOld[i,j] ) > tolerance:
                    toleranceAcqurired = False
    print('Tolerance for n =', n, 'was met after', step, 'steps with first boundary conditions.')
    v1 = np.copy(v)

    # Second boundary conditions
    initiateVMatrixes_2()
    step = 0
    toleranceAcqurired = False
    while not toleranceAcqurired:
        if step%100==0:print('v =',v,'\nstep =',step)
        step+=1
        vOld = np.copy(v)
        relax()
        # Controll accuracy
        toleranceAcqurired = True   # run through v and set false if not acquired
        for i in range(1,n):
            for j in range(1,n):
                if np.abs( (v[i,j]-vOld[i,j])/vOld[i,j] ) > tolerance:
                    toleranceAcqurired = False
    print('Tolerance for n =', n, 'was met after', step, 'steps with second boundary conditions.')
    v2 = np.copy(v)

def loadDataFromFile():
    """Imports stored data from file from previos calculation. Useful when
    fixing the plot. Obs, obly works when running the exact same iteartion,
    change n and you need to calculate again. Imports variables:
    - v1 (first bondary conditions)
    - v2 (second boundary conditions)"""
    global v1, v2
    with open('assets1/c.pkl', 'rb') as file:
        v1 = pickle.load(file)
        v2 = pickle.load(file)

def storeDataToFile():
    """Stores data to file from current calculation. Stores variables:
    - v1 (first bondary conditions)
    - v2 (second boundary conditions)"""
    global stepsToToleranceArray
    with open('assets1/c.pkl', 'wb') as file:
        pickle.dump(v1, file)
        pickle.dump(v2, file)

# ------------------------ Main

if input('1. Run calculation\n2. Import data\n') in ['1','1.']:
    calculate()         # comment to obly load data
    storeDataToFile()   # comment to only load data
loadDataFromFile()

# ----------------------- Plot

commonColormap = 'bone'         # alternatives: inferno, plasma, Greys, Blues, BuPu, bone, afmhot
commonInterpolation = 'bicubic' # alternatives: nearest


fig, axs = plt.subplots(1,2)    # one subplot for each boundary conditions
[ax1, ax2] = axs
fig.set_size_inches(8,5)
# 1 plot potential with colormap
im1 = ax1.imshow(v1,            # plot first result
        cmap='bone',
        interpolation=commonInterpolation)
im2 = ax2.imshow(v2,            # plot second result
        cmap=commonColormap,
        interpolation=commonInterpolation)
fig.colorbar(im1, ax = axs,     # add colorbar below plots
        orientation='horizontal',
        fraction=.1,
        label='V(x,y)')
plt.savefig('assets1/c1.png', dpi=300)
# 2 add contour
cs1 = ax1.contour(v1,           # add first contour
        levels=np.arange(0, 11, 0.5),
        colors='red',
        alpha=0.3)    # transparency
cs2 = ax2.contour(v2,           # add secound contour
        levels=np.arange(0, 11, 0.5),
        colors='red',
        alpha=0.3)    # transparency
plt.savefig('assets1/c2.png', dpi=300)
# 3 add countour labels
plt.clabel(cs1, inline=1, fontsize=10)  # add labels for first contour
plt.clabel(cs2, inline=1, fontsize=10)  # add labels for second contour
plt.savefig('assets1/c3.png', dpi=300)
plt.show()
