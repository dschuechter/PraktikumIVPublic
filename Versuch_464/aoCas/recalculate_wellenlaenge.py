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
import uncertainties.unumpy as unp
from uncertainties import ufloat

def formel(v):
    s = 656.28
    c=300000
    return s*np.sqrt((c+v)/(c-v))

def formel2(x,y):
    s = 656.28
    c=300000
    return x/(-(4 * c * s**2 * y)/(s**2 + y**2)**2)

def speed(y):
    s = 656.28
    # s = 656.45377
    c = 300000
    # return (halpha/y-1)*c
    return c*(s*s-y*y)/(s*s+y*y)

file = 'AOCass_tab.txt'
data = genfromtxt(file, delimiter=';')
v1=data[:,4]
dv1=data[:,5]
v2=data[:,6]
dv2=data[:,7]
y1=np.round(formel(v1),2)
dy1=np.round(formel2(dv1,v1),2)
y2=np.round(formel(v2),2)
dy2=np.round(formel2(dv2,v2),2)
for i in range(0,len(v1)):
    print(y1[i],abs(dy1[i]),y2[i],dy2[i])
y1=unp.uarray(y1,abs(dy1))
y2=unp.uarray(y2,abs(dy2))

# print(speed(656.66))
# print(speed(655.84))
# x = np.linspace(0,100,num=1000)
# y_fit=formel2(x, v1[1])
# plt.plot(x, y_fit, color='black',zorder=3)
# plt.show()
