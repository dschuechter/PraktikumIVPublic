#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
from scipy import stats
import scipy
import scipy.odr as sodr

T=3.52348
def sinus(x, *p):
    K, c, d = p
    return K*abs(np.sin(2.*np.pi*x+d))+c

def getphase(x):
    while x>T:
        x = x-T
    return x/T

def speed(y):
    #s = 656.28
    s = 656.45377
    c = 300000
    # return (halpha/y-1)*c
    return c*(s*s-y*y)/(s*s+y*y)

file = 'wellenlaengen.txt'# sys.argv[1]
data = genfromtxt(file, delimiter=';')
x = data[0:, 5]
errx =  data[:,6]
y1 = speed(data[0:, 1])
erry1 = data[:,2]
y2 = speed(data[:,3])
erry2 = data[:,4]
phi = np.zeros(len(x))
y_abs= np.abs(y1-y2)
print(y_abs)
for i in range(0,len(x)):
    phi[i] = getphase(x[i])
phi=phi-phi[0]
errphi = errx/T

p=[200,1,1]
x = np.linspace(0,1,num=1000)
y_fit=sinus(x, *p)
plt.plot(x, y_fit, color='black',zorder=3)
popt, pcov = curve_fit(sinus, phi, y_abs, p0=p)
perr = np.sqrt(np.diag(pcov))


#y_fit=sinus(x, *popt)
plt.plot(x, y_fit, color='red',zorder=3)
plt.plot(phi, y_abs, 'x')
plt.xlim(0,1)
plt.show()

A = phi
B = y1
i=0
for xy in zip(A, B):                                       # <--
    plt.annotate(i, xy=xy,xytext=(-6,0), textcoords='offset points', ha='center')
    i+=1
B = y2
i=0
for xy in zip(A, B):                                       # <--
    plt.annotate(i, xy=xy,xytext=(-6,0), textcoords='offset points', ha='center')
    i+=1

plt.plot(phi, y1, '+')
plt.plot(phi, y2, 'x')
plt.show()
