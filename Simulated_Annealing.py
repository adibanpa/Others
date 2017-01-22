# PHY407 Lab 11 Question 1a
# Jenny Wu (1000565168), Parham Adiban (1000639446)

# Simulated annealing to solve the dimer problem
from __future__ import division, print_function
from matplotlib.pyplot import *
from random import random, randint
from numpy import zeros, exp

# Define Constants
L = 50			# Size of 'box'
grid = zeros([L, L], int) 
Tmax = 10.0		# Initial temperature
Tmin = 1e-3		# Final temperature
tau = 10000000	# Tau
energy = 0		# Initial energy
T = Tmax		
t = 0			# Calculate number of steps
count = 0		# Count used to set value to each grid point
energylist = []	# List to hold energy values at every step
dimers = {}		# Dictionary to store the position of dimers

# Run loop until temperature goes below our minimum value
while T>Tmin:
	t += 1
	T = Tmax*exp(-t/tau)	# Simulated annealing

	# Choose random grid point
	i = randint(0, L-1)		
	j = randint(0, L-1)
	
	# Give random initial value in order to start loop
	m, n = -1, -1

	while m > L-1 or m < 0 or n > L-1 or n < 0:

		# Set new coordinate points same as the old coordinates
		m, n = i, j

		# Randomly alter new coordinate to 1 position up, down, left, or right
		k = randint(0, 3)
		if k == 0:
			m+=1
		elif k == 1:
			m-=1
		elif k == 2:
			n+=1
		elif k == 3:
			n-=1

	# Check if both grid points are empty
	if grid[i][j] == 0 and grid[m][n] == 0:
		count += 1

		# Give grid points unique value
		grid[i][j] = count
		grid[m][n] = count

		# Add dimer to dictionary, add value with both key names to make sure dimers are recognized in all directions
		dimers[str([i, j, m, n])] = [i, m], [j, n]
		dimers[str([m, n, i, j])] = [i, m], [j, n]

		# Energy increases 1 with each dimer added
		energy += 1

	# If both grid points have the same unique value, then its one dimer
	elif grid[i][j] == grid[m][n]:

		# Check with probability -1/T. for f(e) ~ exp(-E/kT), E = 1 for each dimer, and k = 1 for simplicity
		if random() < exp(-1/T):

			# Delete dimer if probability passed
			if str([i, j, m, n]) in dimers:
				del dimers[str([i, j, m, n])]

			if str([m, n, i, j]) in dimers:
				del dimers[str([m, n, i, j])]

			# Grid point value set to 0 indicating empty
			grid[i][j] = 0
			grid[m][n] = 0

			# Energy decreases as a dimer is removed
			energy -= 1

	else:
		pass

	energylist.append(-1*energy)	# Energy values added to list

# All values of dictionary stored in 'coordinate'
coordinates = dimers.values()

# Plot dimers onto grid
for i in coordinates:
	ylim([-1, L])
	xlim([-1, L])
	figure(1)
	plot(i[0], i[1], 'o-', markersize = 5, linewidth = 2, color = 'k')
	pause(0.01)
	title('Tau = {0} and Energy = {1}'.format(tau, energylist[-1]))
# savefig('3tau={0}'.format(tau))
	
#Plot energy vs time
figure(2)
plot(energylist)
title('Energy of the system with tau = {0}'.format(tau))
xlabel('Time')
ylabel('Energy')
savefig('3energy_tau={0}'.format(tau))
show()








