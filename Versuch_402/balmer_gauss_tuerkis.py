#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
import scipy
from scipy import stats
from uncertainties import unumpy
import uncertainties.unumpy as unp
from uncertainties import ufloat
import scipy.odr as sodr

plt.figure(dpi=300)
file = 'data/Türkis_64.txt'
data = genfromtxt(file, delimiter=';')
i_min=1011
i_max=1041
x = data[i_min:i_max, 0]
y = data[i_min:i_max, 1]
plt.plot(x, y, 'x', alpha = 0.5)

def gauss(x, *p):
	b,c,d,b1,c1,d1,f = p
	y =  stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+f
	return y

def halbwertsbreite(max_x,x, y, p, z):
	print('x_max=%.3f'%max_x)
	y_max = gauss(max_x, *p)
	y_halb = 1/2*(gauss(max_x, *p)-gauss(z, *p))+gauss(z, *p)
	print('y_max = %.3f, y_halb=%.3f'% (y_max,y_halb))
	i=0
	x_found = [1,1]
	found = 0
	print('x0=%.3f, x-1=%.3f'%(x[0],x[-1]))
	while found != 1:
		y_found = gauss(x[i], *p)
		if (y_found<=y_halb*(2-epsilon) and y_found>=y_halb*epsilon):
			x_found[found]=x[i]
			print('x_found=%.3f'%x_found[found])
			found = found +1
		i=i+1
	j = len(x)-1
	print(j)
	while found != 2:
		y_found = gauss(x[j], *p)
		if (y_found<=y_halb*(2-epsilon) and y_found>=y_halb*epsilon):
			x_found[found]=x[j]
			print('x_found=%.3f'%x_found[found])
			found = found +1
		j=j-1

	print('finished')
	return x_found[0], x_found[1]

p_initial = [-0.005,0.005,0.2,0.013,0.005,0.05,0]
popt, pcov = curve_fit(gauss, x, y, p0=p_initial)
x_fit = np.linspace(x[0],x[-1],num=1000)
y_fit = gauss(x_fit, *popt)
plt.plot(x_fit,y_fit,color='cyan')
popt_error=np.sqrt(np.diag(pcov))

epsilon=0.99
x_fit_1 = np.linspace(x[1024-i_min],x[1036-i_min],num=1000)
x_fit_2 = np.linspace(x[1015-i_min],x[1022-i_min],num=1000)
y_fit_1 = gauss(x_fit_1, *popt)
y_fit_2 = gauss(x_fit_2, *popt)
a_x_0, a_x_1=halbwertsbreite(popt[0], x_fit_1,y_fit_1,popt, x[-1])
#plt.plot([a_x_0,a_x_0], [0,20])
#plt.plot([a_x_1,a_x_1], [0,20])
b_x_0, b_x_1=halbwertsbreite(popt[3], x_fit_2,y_fit_2,popt, x[-1])
#plt.plot([b_x_0,b_x_0], [0,20])
#plt.plot([b_x_1,b_x_1], [0,20])

plt.plot(popt[0],gauss(popt[0], *popt), color='green', marker='+', ms = 10, label='$\\alpha_{H_\\beta,0}$=(%.5f $\pm$ %.5f)$^\circ$\n$\Delta\\alpha=(%.5f\pm%.5f)^\circ$'%(popt[0],popt_error[0],a_x_0-a_x_1, (a_x_0-a_x_1)*0.01))
plt.plot(popt[3],gauss(popt[3], *popt), color='black', marker='+', ms = 10, label='$\\alpha_{H_\\beta,1}$=(%.5f $\pm$ %.5f)$^\circ$\n$\Delta\\alpha=(%.5f\pm%.5f)^\circ$'%(popt[3],popt_error[3],b_x_0-b_x_1, (b_x_0-b_x_1)*0.01))

plt.legend()
plt.xlabel('$\\alpha$ / $^\circ$')
plt.ylabel('relative Intensität')
plt.savefig('../../pics/tuerkis.png')

d = unp.uarray([403.609], [9.666])*1e-9
w_B = unp.uarray([135],[1])
w_G = unp.uarray([64],[1])
alpha_1 = unp.uarray([popt[0]],[popt_error[0]])
alpha_2 = unp.uarray([popt[3]],[popt_error[3]])
delta_beta = -alpha_2+alpha_1
print(delta_beta)
delta_beta_value = unp.nominal_values(delta_beta)
delta_beta_error = unp.std_devs(delta_beta)
delta_lamda = d*unp.cos(unp.radians(w_B)+unp.radians(w_G)-np.radians(180))*unp.radians(delta_beta)
print('\n delta lambda')
print(delta_lamda)

delta_alpha_a = unp.uarray(a_x_0-a_x_1, (a_x_0-a_x_1)*0.01)
delta_alpha_b = unp.uarray(b_x_0-b_x_1, (b_x_0-b_x_1)*0.01)
delta_doppler_a = d*unp.cos(unp.radians(w_B)+unp.radians(w_G)-np.radians(180))*unp.radians(delta_alpha_a)
delta_doppler_b = d*unp.cos(unp.radians(w_B)+unp.radians(w_G)-np.radians(180))*unp.radians(delta_alpha_b)
print('\nDoppler')
print(delta_doppler_a)
print(delta_doppler_b)
