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
import chart_studio.plotly as py

plt.figure(dpi=300)
file = sys.argv[1]
data = genfromtxt(file, delimiter=',')
data2 = genfromtxt('Temp_Gegenspannungs_Abhaengigkeit/peaksTemp.txt', delimiter=';')
x0 = data[1:, 0]
y1 = data[1:, 2]
y0 = data2[:,11]
plt.plot(x0,y1, '.')
p=[1,-1,1,1]
def gerade(x, *p):
	a,b,c,d = p
	y=a*np.exp(x*b+c)+d
	return y
popt, pcov = curve_fit(gerade, x0, y1, p0=p)
x_new = np.linspace(x0[0], x0[-1], 1000)
y_new = gerade(x_new, *popt)
z = gerade(x_new, *popt)
#f = np.poly1d(z)
#print(f)

plt.plot(x_new, y_new, '-', color='red', label='$U_{Breite}(U_{gegen})=%.2f\cdot \exp(%.2f\cdot U_{gegen}+%.2f)+%.2f$'%(popt[0],popt[1],popt[2],popt[3]))


plt.legend()
plt.xlabel('$U_{gegen} / V$')
plt.ylabel('$U_{Breite} / V$')
plt.savefig("Temp_Gegenspannungs_Abhaengigkeit/penis.png")
