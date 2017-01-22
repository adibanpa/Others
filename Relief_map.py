# Lab 3 Q3
# Jenny Wu(1000565168) and Parham Adiban (1000639446)

'''
Program is used to take data files from the SRTM to create relief maps of the 
GTA. The absolute heights and intensity of light (shining from the west) 
were both plotted as a grayscale density plot.
'''
from __future__ import division, print_function
import struct
import numpy as np
import pylab as plt

#________________________________Part B_________________________________________
''' 
Reading the file and storing the data in a two dimensional array. 
Taking the derivative of w(x, y) and calculating the intenisty of illumination.
'''
# Define function for intensity
def I(x, y):
    phi = np.pi # Set the angle phi as pi
    cosine = np.cos(phi)
    sine = np.sin(phi)
    return (-1)*(cosine*x + sine*y)/(np.sqrt(x**2 + y**2 + 1))

filename = 'N43W080.hgt' # Set filename as the name of the file to be uploaded
f = open(filename, 'rb') # Open file

# Set constants
h = 420         # distance between grid points for derivation (420m)
size = 1201     # the length of the axes

# Zero arrays
w = np.zeros((size, size))		# w(x, y)
dwx = np.zeros((size, size))		# Derivate of w in terms of x
dwy = np.zeros((size, size))		# Derivative of w in terms of y

# Loop to save each data file in a 2D array.
for row in range(size):
    for col in range(size):
        buf = f.read(2)
        val = struct.unpack('>h', buf)
        w[row][col] = val[0]

# Looping through w(x,y) and taking the x and y derivative of each point
for row in range(size):
    for col in range(size):
        # If statement to use forward difference derivation on the first term
        if row == 0:
            dy = (w[row + 1][col] - w[row][col])/h

        # If statement to use backward difference derivation on the last term
        elif row == size - 1:
            dy = (w[row][col] - w[row - 1][col])/h

        # If statement to use central difference derivation on all the middle terms
        else:
            dy = (w[row + 1][col] - w[row - 1][col])/(2*h)

        # Similar for columns
        if col == 0:
            dx = (w[row][col + 1] - w[row][col])/h
        elif col == size - 1:
            dx = (w[row][col] - w[row][col - 1])/h
        else:
            dx = (w[row][col + 1] - w[row][col - 1])/(2*h)
            
        dwx[row][col] = dx
        dwy[row][col] = dy

I_values = I(dwx, dwy) # Array of values for intensity of illumination

#________________________________Part C_________________________________________
''' 
Create plots for height as a function of (x,y), and intensity of illumination.
'''
# Plot the height function w(x,y) on a density plot
# Limits of vmin and vmax required because incomplete data files include 
# extremely high values as a placeholder
plt.figure()
plt.imshow(w, vmin = 50, vmax = 350, extent=[0. , 1200. , 0., 1200.]) 
plt.title('Relief Map of the GTA', fontsize = 20)
plt.gray()
plt.colorbar(label = 'Height (m)')
plt.savefig('Relief_Map')

# Plot the intensity of illumination on a density plot
plt.figure()
plt.imshow(I_values, vmin = -0.005, vmax = 0.007, extent=[0. , 1200. , 0., 1200.])
plt.title('Intensity of Illumination: GTA', fontsize = 20)
plt.gray()
plt.colorbar(label = 'Intensity (Unknown Units)')
plt.savefig('Relief_Map_with_I')
plt.show()