#Skript zur Berechnung der Rydbergkonstante und des Planckschen Wirnkungsquantums
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



file = sys.argv[1]
data = genfromtxt(file, delimiter=',')
Farbe = ['Rot','Orange','Grün 1','Grün 2','Türkis','Violette 1','Violette 2','Violette_new_1','Violette_new_2','Violette_new_3']
w_B=unp.uarray(data[1:, 0],[1]*10)
w_G=unp.uarray(data[1:, 1],[1]*10)
w_B_value = unp.nominal_values(w_B)
w_B_error = unp.std_devs(w_B)
w_G_value = unp.nominal_values(w_G)
w_G_error = unp.std_devs(w_G)

d = unp.uarray([403.609], [9.666])*1e-9
a = unp.uarray(data[1:,3],[0.05])
a_value = unp.nominal_values(a)
a_error = unp.std_devs(a)
f = unp.uarray(300, 10)
lamda = d* (unp.sin(unp.radians(w_G))-unp.sin(unp.radians(w_G)+unp.radians(w_B)))
lamda_value = unp.nominal_values(lamda)
lamda_error = unp.std_devs(lamda)
delta_beta = a/f

delta_beta_value = unp.nominal_values(delta_beta)
delta_beta_error = unp.std_devs(delta_beta)
delta_lamda = d*unp.cos(unp.radians(w_G)+unp.radians(w_B))*delta_beta
delta_lamda_value = unp.nominal_values(delta_lamda)
delta_lamda_error = unp.std_devs(delta_lamda)
print('\nFarbe & $\lambda$ / nm & Abstand a / mm &$\Delta \beta$ / 10^{-3}^{\circ}$ & $\Delta \lambda$ / nm\\\\')
for i in range(0, len(w_B)):
    print('%s & %.3f\pm%.3f & %.1f\pm %.1f & %.3f\pm%.3f & %.3f\pm%.3f\\\\' % (Farbe[i], lamda_value[i]*1e9, lamda_error[i]*1e9, a_value[i],a_error[i], delta_beta_value[i]*1e3, delta_beta_error[i]*1e3, -delta_lamda_value[i]*1e9, delta_lamda_error[i]*1e9))

print('\nFarbe & $w_B$ / $^\circ$ & $w_G$ / $^\circ$ & Abstand a / mm\\\\')
for i in range(0, len(w_B)):
    print('%s & %.1f\pm %.1f & %.1f\pm %.1f & %.1f\pm%.1f\\\\' % (Farbe[i], w_B_value[i], w_B_error[i], w_G_value[i], w_G_error[i], a_value[i],a_error[i]))


####
# Berechne Rydbergkonstante
####
def lin_func(p, x):
     m, c = p
     return m * x + c

plt.figure(dpi=300)
n = 1/np.array([3,4,5,6,7])
lamda_H = 1/unp.uarray([lamda_value[0],lamda_value[4],lamda_value[7],lamda_value[8],lamda_value[9]],[lamda_error[1],lamda_error[4], lamda_error[7],lamda_error[8],lamda_error[9]])
lamda_H_value = unp.nominal_values(lamda_H)
lamda_H_error = unp.std_devs(lamda_H)
plt.errorbar(x=n**2, y=lamda_H_value*1e-5, xerr=0, yerr=lamda_H_error*1e-5, marker='.',linestyle = 'None')

x_fit = np.linspace(n[0]**2,n[-1]**2,num=100)
model = sodr.Model(lin_func)
fit_data = sodr.RealData(n**2, lamda_H_value, sy=lamda_H_error)
odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
out = odr.run()
a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0]
err_b = out.sd_beta[1]
print(a)
print(err_a)
y_fit= a*x_fit+b
plt.plot(x_fit, y_fit*1e-5, '-',label='$\\frac{1}{\lambda}(n)=R_{\infty}\\left(\\frac{1}{2^2}-\\frac{1}{n^2}\\right)$\n $R_\infty=(%.3f+%.3f)m^{-1}$'%(abs(a),err_a))
plt.legend()
plt.xlabel('$\\frac{1}{n^2}}$')
plt.ylabel('$\\frac{1}{\lambda}}$ / $10^5 $m$^{-1}$')
plt.savefig('../../pics/Rydberg.png')


####
# Berechnen des Plancksche Wirkungsquantums
####

R = unp.uarray([-a],[err_a])
m_p = 1.67262192369*10**(-27)
m_e = 9.1093837015*10**(-31)
m_red_1=(1*m_p*m_e)/(1*m_p+m_e)
m_red = (2*m_p*m_e)/(2*m_p+m_e)
e = 1.602176*10**(-19)
epsilon_0 = 8.854187128*10**(-12)
c = 299792458
h=(m_red_1*e**4/(8*R*epsilon_0**2*c))**(1/3)
h_red=(m_red*e**4/(8*R*epsilon_0**2*c))**(1/3)
print('\n Planck')
print(h)
print(h_red)
