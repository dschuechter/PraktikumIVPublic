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
file = 'data/violett_new.txt'
data = genfromtxt(file, delimiter=';')
i_min=1
i_max=2049
#i_min=0
#i_max=2049
x = data[i_min:i_max, 0]
y = data[i_min:i_max, 1]
plt.plot(x, y, 'x', ms=4, alpha=0.5)

def gauss(x, *p):
	b,c,d,e = p
	y =  stats.skewnorm.pdf(x, 0, b, c)*d+e
	return y

epsilon = 0.99

def halbwertsbreite(max_x,x, y, p):
	print('x_max=%.3f'%max_x)
	y_max = gauss(max_x, *p)
	y_halb = 1/2*(gauss(max_x, *p)-gauss(x[0], *p))+gauss(x[0], *p)
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

p_initial_1 = [0.8,1.0,0.9,2]
p_initial_2 = [0.01,1,100,2]
p_initial_3 = [0.5,0.5,0.7,3.6]

x_fit_1 = np.linspace(x[1715],x[1790],num=1000)
x_fit_2 = np.linspace(x[1591],x[1630],num=1000)
x_fit_3 = np.linspace(x[0],x[645],num=1000)
popt_1, pcov_1 = curve_fit(gauss, x[1711:1775], y[1711:1775], p0=p_initial_1)
popt_2, pcov_2 = curve_fit(gauss, x[1591:1631], y[1591:1631], p0=p_initial_2)
popt_3, pcov_3 = curve_fit(gauss, x[0:645], y[0:645], p0=p_initial_3)
y_fit_1 = gauss(x_fit_1, *popt_1)
y_fit_2 = gauss(x_fit_2, *popt_2)
y_fit_3 = gauss(x_fit_3, *popt_3)

plt.plot(x_fit_1,y_fit_1,color='darkviolet')
plt.plot(x_fit_2,y_fit_2,color='darkviolet')
plt.plot(x_fit_3,y_fit_3,color='darkviolet')

popt_error_1=np.sqrt(np.diag(pcov_1))
popt_error_2=np.sqrt(np.diag(pcov_2))
popt_error_3=np.sqrt(np.diag(pcov_3))

a_x_0, a_x_1=halbwertsbreite(popt_1[0], x_fit_1,y_fit_1,popt_1)
#plt.plot([a_x_0,a_x_0], [3,7])
#plt.plot([a_x_1,a_x_1], [3,7])

b_x_0, b_x_1=halbwertsbreite(popt_2[0], x_fit_2,y_fit_2,popt_2)
#plt.plot([b_x_0,b_x_0], [3,7])
#plt.plot([b_x_1,b_x_1], [3,7])

c_x_0, c_x_1=halbwertsbreite(popt_3[0], x_fit_3,y_fit_3,popt_3)
#plt.plot([c_x_0,c_x_0], [3,7])
#plt.plot([c_x_1,c_x_1], [3,7])

plt.plot(popt_1[0],gauss(popt_1[0], *popt_1), color='green', marker='+', ms = 10, label='$\\alpha_{\gamma}$=(%.5f $\pm$ %.5f)$^\circ$\n$\Delta\\alpha=(%.5f\pm%.5f)^\circ$'%(popt_1[0],popt_error_1[0], a_x_0-a_x_1, (a_x_0-a_x_1)*0.01))
plt.plot(popt_2[0],gauss(popt_2[0], *popt_2), color='black', marker='+', ms = 10, label='$\\alpha_{\delta}$=(%.5f $\pm$ %.5f)$^\circ$\n$\Delta\\alpha=(%.5f\pm%.5f)^\circ$'%(popt_2[0],popt_error_2[0], b_x_0-b_x_1,(b_x_0-b_x_1)*0.01))
plt.plot(popt_3[0],gauss(popt_3[0], *popt_3), color='red', marker='+', ms = 10, label='$\\alpha_{?}$=(%.5f $\pm$ %.5f)$^\circ$\n$\Delta\\alpha=(%.5f\pm%.5f)^\circ$ '%(popt_3[0],popt_error_3[0], c_x_0-c_x_1,(c_x_0-c_x_1)*0.01))


plt.legend()
plt.xlabel('$\\alpha$ / $^\circ$')
plt.ylabel('relative Intensität')
plt.savefig('../../pics/violett_1_2_3.png')

####
# Rechne Linienbreite in nm um
####
d = unp.uarray([403.609], [9.666])*1e-9
w_B_1 = unp.uarray([131.5],[1])
w_G_1 = unp.uarray([60],[1])
w_B_2 = unp.uarray([131.3],[1])
w_G_2 = unp.uarray([60],[1])
w_B_3 = unp.uarray([128.3],[1])
w_G_3 = unp.uarray([60],[1])

delta_alpha_a = unp.uarray(a_x_0-a_x_1, (a_x_0-a_x_1)*0.01)
delta_alpha_b = unp.uarray(b_x_0-b_x_1, (b_x_0-b_x_1)*0.01)
delta_alpha_c = unp.uarray(c_x_0-c_x_1, (c_x_0-c_x_1)*0.01)
delta_doppler_a = d*unp.cos(unp.radians(w_B_1)+unp.radians(w_G_1)-np.radians(180))*unp.radians(delta_alpha_a)
delta_doppler_b = d*unp.cos(unp.radians(w_B_2)+unp.radians(w_G_2)-np.radians(180))*unp.radians(delta_alpha_b)
delta_doppler_c = d*unp.cos(unp.radians(w_B_3)+unp.radians(w_G_3)-np.radians(180))*unp.radians(delta_alpha_c)
print('\nDoppler')
print(delta_doppler_a)
print(delta_doppler_b)
print(delta_doppler_c)
