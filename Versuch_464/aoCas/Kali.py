#Skript zum Plotten der Kalibrationsspektren inkl. der konvertierung in Wellenlänge
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

plt.figure(dpi=300)
def lin_func(p, x):
     m, c = p
     return m * x + c

def kali(file):
    spekfile = './data/'+file
    kalifile = './kali/'+file+'_kali'
    data = genfromtxt(kalifile, delimiter=';')
    data1=genfromtxt(spekfile, delimiter='\t')
    y = data[:, 0]/10 #Wellenlänge
    x = data[:, 1] #Pixelpos

    y_spek = data1[:,2]
    x_spek = data1[:, 0]

    xerr = [1]*len(x) #Pixelfehler
    yerr = [0.1]*len(y) #Wellenlängenfehler

    model = sodr.Model(lin_func)
    fit_data = sodr.RealData(x[0:], y[0:], sx=xerr[0:], sy=yerr[0:])
    odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
    out = odr.run()
    a = out.beta[0]
    b = out.beta[1]
    err_a = out.sd_beta[0]
    err_b = out.sd_beta[1]
    x_fit= np.linspace(x[0],x[-1],1000)
    xerr_fit = [3]*len(x) #Pixelfehler
    yerr_fit = [1]*len(y) #Wellenlängenfehler

    plt.plot(x_spek, y_spek, '-', label ='Messung: '+file)
    plt.xlabel('Pixelkoordinate / Pixel')
    plt.ylabel('Intensität')
    plt.legend()
    plt.savefig('../../../pics/'+file+'k')
    plt.clf()

    plt.errorbar(x, y, xerr=xerr_fit, yerr=yerr_fit, fmt='.')
    plt.plot(x_fit, a*x_fit+b, label = '$\lambda(x)=a\cdot x+b$\na=(%.4f$\pm$%.4f)nm/px\nb=(%.3f$\pm$%.3f)nm'%(a,err_a,b, err_b))
    plt.xlabel('Pixelkoordinate / Pixel')
    plt.ylabel('Wellenlänge $\lambda$ / nm')
    plt.legend()
    plt.savefig('../../../pics/'+file+'w')
    plt.clf()



kali('2017-10-14')
kali('2017-10-15A')
kali('2017-10-15B')
kali('2017-10-16A')
kali('2017-10-16B')
kali('2018-02-12')
kali('2018-02-13')
kali('2018-02-22')
kali('2018-08-22')
kali('2019-12-04')
