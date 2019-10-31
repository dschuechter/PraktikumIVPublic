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

# fitte eine funktion zur B-feld bestimmung aus dem gemsessenen Strom
data = genfromtxt('Magnetfeldbestimmung.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
z = np.polyfit(x0, y0, 5)
print(z)

# funktion zur Magnetfeldbestimmung
def magnetfeld(x):
	return z[0]*x**5+z[1]*x**4++z[2]*x**3+z[3]*x**2+z[4]*x++z[5]

# Bestimmme Wellenlänge aus winkel (in nm)
def wellenlaenge(x):
	n=1.457
	k=18105.
	d=0.004
	return (2*d*np.sqrt(n*n-np.power(np.sin(np.radians(x-0.013624114364866935)),2))/(k-1))*1e9

# dreifache Gaussfunktion
def gauss(x, *p):
	b, b1, b2, c, c1, c2, d, d1, d2, f = p
	y =  stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+stats.skewnorm.pdf(x , 0, b2, c2)*d2+f
	return y


# dateinamen (ohne .txt) und der entsprechende Strom dazu
file = ['5_5A','6_0A','6_5A','7_0A','7_3A','7_5A','8_0A','8_5A','8_7A','9_1A','9_3A']
strom = [5.5,6,6.5,7,7.3,7.5,8,8.5,8.7,9.1,9.3]
offset = 0
left =-1.11
right = -0.7


def makegauss(f):
	# anfangsparameter (offset ist unnötig da dieser bei 0 bleib)
	offset = 0
	# linke und rechte Grenze des zu verarbeitenden peaks
	left =-1.11
	right = -0.7
	#left = 0.7
	# right = 1.12
	epsilon = 8

	data = genfromtxt(file[f]+'.txt', delimiter=';')
	x0 = data[:1020, 0]
	y0= data[:1020, 1]+offset
	#plt.plot(wellenlaenge(x0), y0, '.', ms=5, label='B = %.1f mT ' %(magnetfeld(strom[f])))#  Offset = %.d, offset)+'%')

	# finde arrayposition zu lefz und right
	i=0
	left_a = 0
	right_a = 0
	while x0[i]<left:
		left_a = i
		i += 1
	while x0[i]<right:
		right_a = i
		i+= 1
	i = left_a+2

	# finde die drei maxima zu den peaks
	x_max = [100, 100, 100]
	j=0
	while i < right_a:
		x_max[j] = i
		if y0[i]>((y0[i+1]+y0[i+2])/2):
			if y0[i]>((y0[i-1]+y0[i-2])/2):
				#print('%.d, %.2f' %(j, x0[x_max[j]]))
				j += 1
				i += 5
		i += 1
		if j==3: break

	# finde die minima links und rechts von dem PeakTriplett
	i=x_max[0]-5
	min1=100
	while y0[i]>((y0[i-1]+y0[i-2])/2):
		min1=i
		i -= 1
	i=x_max[2]+5
	min2=100
	while y0[i]>((y0[i+1]+y0[i+2])/2):
		min2=i
		i += 1
	#print('%.2f, %.2f, %.2f, %.2f, %.2f' %(x0[min1], x0[x_max[0]], x0[x_max[1]], x0[x_max[2]], x0[min2]))
	# finde eine funktion, welche an das PeakTriplett passt
	x = data[min1:min2, 0]
	y = data[min1:min2, 1]+offset
	# anfangsparameter
	p_initial = [x0[x_max[0]], x0[x_max[1]], x0[x_max[2]], 0.1, 0.1, 0.1, 10, 10, 10, 10]
	try:
		popt, pcov = curve_fit(gauss, x, y, p0=p_initial)
		y_fit = gauss(x, *popt)
		print(file[f]+';%.1f;%.5f;%.2f;%.5f;%.2f;%.5f;%.2f;Offset=%.d' %(magnetfeld(strom[f]),wellenlaenge(popt[0]),gauss(popt[0], *popt)-offset, wellenlaenge(popt[1]),gauss(popt[1], *popt)-offset, wellenlaenge(popt[2]),gauss(popt[2], *popt)-offset,offset)+'%')
		plt.plot(wellenlaenge(x), y_fit, color='black')
	except RuntimeError:
		print("Error - curve_fit failed")
	plt.plot(wellenlaenge(x0), y0, '.', ms=5, label='B = %.1f mT  $\lambda_-$ = %.4f  $\lambda_0$ = %.4f  $\lambda_+$ = %.4f' %(magnetfeld(strom[f]),wellenlaenge(popt[0]),wellenlaenge(popt[1]),wellenlaenge(popt[2])))
	#offset += 0

# fitte für alle messungen eine funktion
for f in [0,1,2,3,4,5,6,7,8,9,10]:
	plt.figure(dpi=300)
	makegauss(f)
	plt.xlabel('Wellenlänge $\lambda$ / nm')
	plt.ylabel('Intensität / %')
	plt.legend(loc='lower center')
	plt.xlim(wellenlaenge(left), wellenlaenge(right))
	#plt.ylim(30, 110)
	plt.grid()
	plt.savefig('Gaussbilder/'+file[f]+".png")






#plt.show()
