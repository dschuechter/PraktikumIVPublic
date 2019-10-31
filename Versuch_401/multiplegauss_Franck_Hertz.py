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

def gauss(x, *p):
	b, c, d, f, b1, c1, d1, f1, b2, c2, d2, f2 ,b3, c3, d3, f3,b4, c4, d4, f4 = p
	y =  stats.skewnorm.pdf(x , 0, b, c)*d+f+stats.skewnorm.pdf(x , 0, b1, c1)*d1+f1+stats.skewnorm.pdf(x , 0, b2, c2)*d2+f2+stats.skewnorm.pdf(x , 0, b3, c3)*d3+f3+stats.skewnorm.pdf(x , 0, b4, c4)*d4+f4
	return y

plt.figure(dpi=300)

#welche reihe an
file = sys.argv[1]
#anzahl einer anordnung (z.B. 1A,...,1D = 4)
left = 5.
right = 35.
epsilon = 7

data = genfromtxt(file+'.txt', delimiter=';')
x0 = data[:, 0]
y0 = data[:, 1]
plt.plot(x0, y0, '+')


i=0
left_a = 0
right_a = 0
while x0[i]<left:
	left_a = i
	i += 1

while x0[i]<right:
	right_a = i
	i+= 1

x_max=[10,10,10,10,10]

def findmax():
	i = right_a
	j=0
	while i > left_a:
		x_max[j] = i
		if y0[i]>((y0[i+1]+y0[i+2])/2):
			if y0[i]>((y0[i-1]+y0[i-2])/2):
				#print('%.d, %.2f' %(j, x0[x_max[j]]))
				j += 1
				i -= 5
		i -= 1
		if j==5: break

def makegauss():
	x = data[x_max[4]-epsilon-15:x_max[0]+epsilon, 0]
	y = data[x_max[4]-epsilon-15:x_max[0]+epsilon, 1]
	# 	#print(x)
	e = np.array([5 for _ in y])
	p=[x0[x_max[4]],1,0.1,0,x0[x_max[3]],1,10,0,x0[x_max[2]],1,10,0,x0[x_max[1]],1,10,0,x0[x_max[0]],1,10,0]
	popt, pcov = curve_fit(gauss, x, y, p0=p, sigma=e)
	y_fit = gauss(x, *popt)
	print(file+';%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f' %(popt[0],gauss(popt[0], *popt), popt[4],gauss(popt[4], *popt), popt[8],gauss(popt[8], *popt), popt[12],gauss(popt[12], *popt), popt[16], gauss(popt[16], *popt)))
	# Create a plot of our work, showing both the data and the fit.
	plt.plot(x, y_fit, color='black')

	A = popt[0], popt[4], popt[8], popt[12], popt[16]
	B = gauss(popt[0], *popt),gauss(popt[4], *popt),gauss(popt[8], *popt),gauss(popt[12], *popt), gauss(popt[16], *popt)
	for xy in zip(A, B):                                       # <--
	    plt.annotate('(%.3f, %.3f)' % xy, xy=xy,xytext=(-33, 7), textcoords='offset points', ha='center')
findmax()
makegauss()

plt.ylabel('$U_A$ / V')
plt.xlabel('$U_B$ / V')
#plt.legend(loc='lower left')
plt.xlim(left, right)
#plt.ylim(0, 2)
plt.savefig("Bilder/"+file+".png")
#plt.show()
