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

plt.figure(dpi=300)

def gauss(x, *p):
	b, c, d, b1, c1, d1 = p#,return stats.skewnorm.pdf(x , 0, b, c)*(-np.absolute(d))+stats.skewnorm.pdf(x , 0, b1, c1)*np.absolute(d1)+180.01371
    # y =  stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+f
    # return stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+f
	return -np.absolute(d)*np.exp(-1/2*((x-b)/c)**2)+np.absolute(d1)*np.exp(-1/2*((x-b1)/c1)**2)+180.01371
def gaussneg(x, *p):
	b, c, d = p#;return stats.skewnorm.pdf(x , 0, b, c)*(-np.absolute(d))+180.01371
	return -np.absolute(d)*unp.exp(-1/2*((x-b)/c)**2)+180.01371
def gausspos(x, *p):
	b, c, d = p#;return stats.skewnorm.pdf(x , 0, b, c)*np.absolute(d)+180.01371
	return d*unp.exp(-1/2*((x-b)/c)**2)+180.01371
def lin_func(p, x):
     m, c = p
     return m * x + c

def wellenlaengenconverterfit():
    kalifile = file+'_kali'
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

def wellenerr(x, *p):
	a,b=p
	return x*a

def makegauss():
	x = data[250:510,0]
	y = data[250:510,1]
	# anfangsparrameter
	p=[370,50,100,400,50,100]
	#y_fit = gauss(x, *p)
	#plt.plot(wellenlaengenconverter(x, *ab), y_fit, color='red',zorder=1)
	# finde eine Passende funktion die an die Messwerte passt.
	popt, pcov = curve_fit(gauss, x, y, p0=p)
	perr = np.sqrt(np.diag(pcov))
	y_fit = gauss(x, *popt)
	y_fit_neg = gaussneg(x, *popt[0:3])
	y_fit_pos = gausspos(x, *popt[3:6])
	ab = wellenlaengenconverterfit()
	x = wellenlaengenconverter(x, *ab)
	# print(perr[0])
	#x_min = unp.uarray([popt[0]],[perr[0]])
	# print(x_min)
	# x_max = unp.uarray([popt[3]],[perr[3]])
	# y_min = gaussneg(x_min, *popt[0:3])
	# y_max = gausspos(x_max, *popt[3:6])
	# print(y_min)

	popt1 = wellenlaengenconverter(popt, *ab)
	#popt = wellenerr(popt, *ab)
	perr = wellenerr(perr, *ab)
	plt.plot(x, y_fit, color='black',zorder=3, label = 'Anpassung Datensatz')
	plt.plot(x, y_fit_neg, '--', color='red',zorder=3, label='Anpassung Absorption')
	plt.plot(x, y_fit_pos, '--', color='green',zorder=3, label='Anpassung Emissions')

	x_min = ufloat(popt1[0],perr[0])
	x_max = ufloat(popt1[3],perr[3])
	print(x_min,x_max)
	print(popt)
	sigma_1 = ufloat(wellenerr(popt[1], *ab),perr[1])/10
	print(unp.sqrt(sigma_1))
	print(sigma_1)
	lamda_b=x_min-unp.sqrt(2*np.log(2))*sigma_1
	print('\n lambda')
	print(lamda_b)
	lamda_s=x_max
	print(lamda_s)
	#print(lamda_b, lamda_s)
	v=299792458/1000*(lamda_s**2-lamda_b**2)/(lamda_s**2+lamda_b**2)
	lamda_b= x_min
	v_1=299792458/1000*(lamda_s**2-lamda_b**2)/(lamda_s**2+lamda_b**2)
	print('& Absorption i=1 & Emsission i=2')
	print('$\mu_i$ / nm & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f'%(popt1[0], perr[0], popt1[3], perr[3]))
	print('$\sigma_i$ / nm & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f'%(popt[1]/10, perr[1]/10, popt[4]/10, perr[4]/10))
	#print('$\a_i$ & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f'%()
	print(v)
	print(v_1)
	return x, y_fit_neg, y_fit_pos


file = sys.argv[1]
data = genfromtxt(file, delimiter='\t')
x = data[0:, 0]
y = data[0:, 1]
# p = ab
# x = wellenlaengenconverter(x, *p)
ab = wellenlaengenconverterfit()
x = wellenlaengenconverter(x, *ab)
plt.plot(x, y, '-',zorder=2)
y= (data[0:, 2])/100
#plt.plot(x, y, '-',zorder=1)
makegauss()
# x, y_fit_neg, y_fit_pos = makegauss()
plt.ylabel("Intensität")
plt.xlabel("Wellenlänge $\lambda$ / nm")
#plt.xlim(520, 610)
plt.legend()
plt.savefig('../../../pics/WR.png')#'../../../pics/'
plt.show()
