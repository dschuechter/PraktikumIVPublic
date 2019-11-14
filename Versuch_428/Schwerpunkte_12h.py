#!/usr/bin/env python3
#Skript zur Erstellung des Spektrums der 12h Messung inklusive Gaussfit
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
import scipy
from scipy import stats
import uncertainties.unumpy as unp
from uncertainties import ufloat

heV = 4.135667696e-15
h = 6.62607017e-34
cpm = 299792458e12
c = 299792458
E_R=2.179e-18

#plt.figure(dpi=300)

def wellenlänge(x):
    d=5.6402/2*1e-10
    y= 2*d*np.sin(np.radians(x))/4#*1e12
    return y

def gauss(x, *p):
	b, c, d,f = p
	y =  stats.skewnorm.pdf(x , 0, b, c)*d+f
	return y

file = sys.argv[1]
data = genfromtxt(file, delimiter=';')
x = data[130:210, 0]
y= data[130:210, 1]
# x = data[1:, 0]
# y= data[1:, 1]
plt.plot(wellenlänge(x)*1e12, y, 'x', ms=3)
#plt.plot(x, y, 'x')


def makegauss(min1, min2, max):
    x = data[min1:min2, 0]
    #x=wellenlänge(x)
    y = data[min1:min2, 1]
    p_initial = [max,1,1,1]
    #e = np.array([5 for _ in y])
    popt, pcov = curve_fit(gauss, x, y, p0=p_initial)
    x = np.linspace(x[0],x[-1],num=100)
    y_fit = gauss(x, *popt)
    #plt.plot(x, y_fit, color='black')
    plt.plot(wellenlänge(x)*1e12, y_fit, color='black')
    perr = np.sqrt(np.diag(pcov))
    print('%.4f;%.4f' %(wellenlänge(popt[0])*1e12, wellenlänge(perr[0])*1e12))
    return wellenlänge(popt[0]), wellenlänge(perr[0])
    return popt[0], perr[0]

def deltawellenlänge(x):
    d=2.7e-10
    y= np.abs(2*d*np.cos(np.radians(x))*np.radians(0.01))
    return y

print('lambda')

a,b=makegauss(151,171,30.1)
b=deltawellenlänge(a)
Ka1=ufloat(a,b)
a,b=makegauss(172,189,30.32)
b=deltawellenlänge(a)
Ka2=ufloat(a,b)


# print(energie(65,3))
# print(energie(65,4))
# print(energie(65,5))
Ea1=heV*c/Ka1
Ea2=heV*c/Ka2
print(Ka1)
print(Ka2)
E_delta=Ka1-Ka2
#print(E_delta*1e12)
print('{:.2f}'.format(E_delta*1e12))
print('{:.2f}'.format(Ea1))
print('{:.2f}'.format(Ea2))



def mouse_move(event):
    x, y = event.xdata, event.ydata
    print(x, y)

#plt.connect('motion_notify_event', mouse_move)
#plt.axis('equal')
plt.ylabel('# / s$^{-1}$')
plt.xlabel('$\lambda$ / pm')
plt.savefig('bild.jpg')
plt.savefig('feinstruktur.svg')
# plt.show()
