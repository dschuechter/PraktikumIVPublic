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


def gerade(x, *p):
	a,b,c,d,e = p
	y=a+b*x+c*x*x+d*x*x*x+e*x**4#+f*x**5
	return y

file = sys.argv[1]
data = genfromtxt(file, delimiter=';')
x = data[:, 0]
y= data[:, 1]
p=[1,1,1,1,1]
popt, pcov = curve_fit(gerade, x, y, p0=p)
x_new = np.linspace(x[0], x[-1], 1000)
y_fit = gerade(x_new, *popt)
plt.plot(x_new, y_fit, color='black')

plt.plot(x, y, '+')

x0 = data[:, 0]
y0= data[:, 1]
z = np.polyfit(x0, y0, 10)
f = np.poly1d(z)
print(f[1])
x_new = np.linspace(x0[0], x0[-1], 1000)
y_new = f(x_new)
plt.plot(x_new, y_new, 'r-', label=f)
plt.show()
