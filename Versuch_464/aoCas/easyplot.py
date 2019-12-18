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


def lin_func(p, x):
     m, c = p
     return m * x + c

def wellenlaengenconverterfit(file):
    kalifile = './kali/'+file+'_kali'
    data = genfromtxt(kalifile, delimiter=';')
    y = data[:, 0] #Wellenlänge
    x = data[:, 1] #Pixelpos
    xerr = [1]*len(x) #Pixelfehler
    yerr = [0.1]*len(y) #Wellenlängenfehler

    model = sodr.Model(lin_func)
    fit_data = sodr.RealData(x[0:], y[0:], sx=xerr[0:], sy=yerr[0:])
    odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
    out = odr.run()
    a = out.beta[0]
    b = out.beta[1]
    return a,b

def wellenlaengenconverter(x, *p):
	a,b=p
	return (a*x+b)/10

def speed(y):
    s = 656.28
    # s = 656.45377
    c = 300000
    # return (halpha/y-1)*c
    return c*(s*s-y*y)/(s*s+y*y)

file = sys.argv[1]
fig, ax = plt.subplots(dpi=200)
data = genfromtxt('./data/'+file, delimiter='\t')
x = data[0:, 0]
y= data[0:, 1]
ab = wellenlaengenconverterfit(file)
x=wellenlaengenconverter(x,*ab)
ax.plot(x, y, '-')
# y= (data[0:, 2]-1000)/10
# plt.plot(x, y, '-')
ax.plot([656.28,656.28],[00,600],color='red')
plt.xlim(647,665)

eins = 0
zwei = 0

def onclick(event):
    # global eins, zwei
    # if event.button==1:
    #     eins = speed(event.xdata)
    if event.button==3:
    #     zwei = speed(event.xdata)
    # print('eins=',eins,',   zwei=', zwei, '\n delta=', abs(eins-zwei),'\n---------')
        plt.savefig("./pics_no_gauss/"+file+".png")
fig.canvas.mpl_connect('button_press_event', onclick)



plt.ylabel("Intensität")
plt.xlabel("Wellenlänge $\lambda$ / nm")
# plt.title(file)
plt.show()
