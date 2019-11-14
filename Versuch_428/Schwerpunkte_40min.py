#!/usr/bin/env python3
#Skript zur Erstellung des Spektrums der 40min Messung inklusive Gaussfit
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

plt.figure(dpi=300)

def wellenlänge(x):
    d=5.6402/2*1e-10
    y= 2*d*np.sin(np.radians(x))#*1e12
    return y

def gauss(x, *p):
	b, c, d,f = p
	y =  stats.skewnorm.pdf(x , 0, b, c)*d+f
	return y

file = sys.argv[1]
data = genfromtxt(file, delimiter=';')
x = data[80:150, 0]
y= data[80:150, 1]
plt.plot(wellenlänge(x)*1e12, y, 'x', ms=3)

def makegauss(min1, min2, max):
    x = data[min1:min2, 0]
    #x=wellenlänge(x)
    y = data[min1:min2, 1]
    p_initial = [max,1,4000,500]
    #e = np.array([5 for _ in y])
    popt, pcov = curve_fit(gauss, x, y, p0=p_initial)
    x = np.linspace(x[0],x[-1],num=100)
    y_fit = gauss(x, *popt)
    plt.plot(wellenlänge(x)*1e12, y_fit, color='black')
    perr = np.sqrt(np.diag(pcov))
    print('%.4f;%.4f' %(wellenlänge(popt[0])*1e12, wellenlänge(perr[0])*1e12))
    return wellenlänge(popt[0]), wellenlänge(perr[0])
    return popt[0], perr[0]

def deltawellenlänge(x):
    d=2.7e-10
    y= np.abs(2*d*np.cos(np.radians(x))*np.radians(0.1))
    return y

print('lambda')

a,b=makegauss(87,97,11)
b=deltawellenlänge(a)
Ky=ufloat(a,b)
a,b=makegauss(102,120,13)
b=deltawellenlänge(a)
Kß=ufloat(a,b)
a,b=makegauss(125,140, 15)
b=deltawellenlänge(a)
Ka=ufloat(a,b)



Zy=unp.sqrt(1/(1-1/4**2)*h*c/E_R/Ky)
Zß=unp.sqrt(1/(1-1/3**2)*h*c/E_R/Kß)
Za=unp.sqrt(1/(1-1/2**2)*h*c/E_R/Ka)
Z=(Za+Zß+Zy)*1/3
print("Z")
print(Ka*1e12)
print(Kß*1e12)
print(Ky*1e12)
#print(Z)

def energie(Z,n):
    e=Z*Z*E_R*(1/4-(1/n**2.))*6.2415096471204e18
    return e

# print(energie(65,3))
# print(energie(65,4))
# print(energie(65,5))
Ea=heV*c/Ka
Eß=heV*c/Kß
Ey=heV*c/Ky
print('{:.2f}'.format(Ea))
print('{:.2f}'.format(Eß))
print('{:.2f}'.format(Ey))



def mouse_move(event):
    x, y = event.xdata, event.ydata
    print(x, y)

#plt.connect('motion_notify_event', mouse_move)
#plt.axis('equal')
plt.ylabel('# / s$^{-1}$')
plt.xlabel('$\lambda$ / pm')
plt.savefig('bild.jpg')
plt.savefig('unbekannteAnode.svg')
#plt.show()
