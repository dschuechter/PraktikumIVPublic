#!/usr/bin/env python3

import sys
import argparse
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse
from scipy.optimize import curve_fit
from scipy import stats

#welche reihe an
row = sys.argv[1]
#anzahl einer anordnung (z.B. 1A,...,1D = 4)
amount = sys.argv[2]

def gauss(x, *p):
	a, b, c, d, f = p
	y = y = stats.skewnorm.pdf(x , a, b, c)*d+f

	return y

N = 600-150
plt.figure(dpi=150)

#trage für jede messung einen Plot in die Figure ein
j = int(amount)+1
i = 1
while i<j:
	#importiere die Daten der entsprechenden Messung (90 grad polarisation)
	#ersetze _90 durch _90 für 0 Grad polarisation
	file = chr(i+64)+row+"_90.txt"
	data = genfromtxt(file, delimiter='\t')
	x0 = data[150:600, 0]
	y0= data[150:600, 1]
	#plt.plot(x0, y0, '-', label=chr(i+64)+row)
	x_min = x0[1]
	y_min = y0[1]
	k = 2
	while k < N:
		if y_min > y0[k]:
			y_min = y0[k]
			x_min = x0[k]
		k += 1

	p_initial = [1, x_min, 10, y_min-100, 400]
	x = data[(int(x_min)-460):(int(x_min)-250), 0]
	y = data[(int(x_min)-460):(int(x_min)-250), 1]
	e = np.array([5 for _ in y])
	# Create our data sets. Perturb the y-data with randomness and
	# generate completely random data for the errors.
	# Use curve_fit to fit the gauss function to our data. Use the
	# unperturbed p_initial as our initial guess.
	popt, pcov = curve_fit(gauss, x, y, p0=p_initial, sigma=e)
	# Generate y-data based on the fit.
	y_fit = gauss(x, *popt)
	# Create a plot of our work, showing both the data and the fit.
	plt.plot(x, y_fit, color = 'black')
	a, b, c, d, f = popt
	g = gauss(b, *popt)
	plt.plot(x0, y0, '-', label=chr(i+64)+row+': $\lambda_{min}=$%.2f nm, $T=%.2f$'%(b,g)+'%')
	print(b)
	print(g)
	i += 1

plt.xlabel('$\lambda$/nm')
plt.ylabel('Transmision / %')
plt.legend(loc='lower left')
plt.xlim(500, 990)
plt.ylim(30, 110)
plt.savefig(row+"_plot_90_gauss.png")
plt.show()
