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


# Zum verständniss siehe MultiplegaussWellenlänge_single_Zeeman.py
# der unterschied besteht darin dass die messkurven nun alle in ein Diagramm eingetragen werden,
# dafür dann aber um '5%' versetzt (offset), so dass man noch etwas erkennt

data = genfromtxt('Magnetfeldbestimmung.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
z = np.polyfit(x0, y0, 5)
print(z)

def magnetfeld(x):
	return z[0]*x**5+z[1]*x**4++z[2]*x**3+z[3]*x**2+z[4]*x++z[5]

def wellenlaenge(x):
	n=1.457
	k=18105.
	d=0.004
	return (2*d*np.sqrt(n*n-np.power(np.sin(np.radians(x-0.013624114364866935)),2))/(k-1))*1e9

def gauss(x, *p):
	b, b1, b2, c, c1, c2, d, d1, d2, f = p
	y =  stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+stats.skewnorm.pdf(x , 0, b2, c2)*d2+f
	return y

plt.figure(dpi=300, figsize=(10, 14))
file = ['5_5A','6_0A','6_5A','7_0A','7_3A','7_5A','8_0A','8_5A','8_7A','9_1A','9_3A']
strom = [5.5,6,6.5,7,7.3,7.5,8,8.5,8.7,9.1,9.3]
offset = 0

for f in [0,1,2,3,4,5,6,7,8,9,10]:
	left =-1.11
	right = -0.7
	epsilon = 8

	data = genfromtxt(file[f]+'.txt', delimiter=';')
	x0 = data[:1020, 0]
	y0= data[:1020, 1]+offset
	plt.plot(wellenlaenge(x0), y0, '.', ms=5, label='B = %.1f mT ' %(magnetfeld(strom[f])))#  Offset = %.d, offset)+'%')

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

	x = data[min1:min2, 0]
	y = data[min1:min2, 1]+offset
	e = np.array([5 for _ in y])
	p_initial = [x0[x_max[0]], x0[x_max[1]], x0[x_max[2]], 0.1, 0.1, 0.1, 10, 10, 10, 10]
	try:
		popt, pcov = curve_fit(gauss, x, y, p0=p_initial, sigma=e)
		y_fit = gauss(x, *popt)
		print(file[f]+';%.1f;%.5f;%.2f;%.5f;%.2f;%.5f;%.2f;Offset=%.d' %(magnetfeld(strom[f]),wellenlaenge(popt[0]),gauss(popt[0], *popt)-offset, wellenlaenge(popt[1]),gauss(popt[1], *popt)-offset, wellenlaenge(popt[2]),gauss(popt[2], *popt)-offset,offset)+'%')
		plt.plot(wellenlaenge(x), y_fit, color='black')
	except RuntimeError:
		print("Error - curve_fit failed")

	offset += 5



plt.xlabel('Wellenlänge $\lambda$ / nm')
plt.ylabel('Intensität / %')
#plt.legend()#loc='lower left')
plt.xlim(wellenlaenge(left), wellenlaenge(right))
plt.ylim(0, 93)
plt.grid()
plt.savefig("bild.png")
#plt.show()
