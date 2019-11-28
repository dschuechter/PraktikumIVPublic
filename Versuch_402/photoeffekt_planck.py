#Skript zur Bestimmung des Planckschen Wirkungsquantums
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
import scipy.odr as sodr

def lin_func(p, x):
     m, c = p
     return m * x + c

c=299792458
e=1.602176634e-19


file = sys.argv[1]
data = genfromtxt(file, delimiter='&')
lamda= np.array([365,405,436,546,578])*1e-9
lamda_error=10*1e-9


x=1/lamda
xerr=1/lamda**2*lamda_error
y_in=-data[1:,2]
yerr_in=data[1:,3]
y = [0]*5
yerr = [0]*5
j=0
y[4]=(y_in[8]+y_in[9])/2
for i in range(0,5):
    y[i]=(y_in[i*2]+y_in[1+2*i])/2
    #print('y_in_1=%.3f, y_in_2=%.3f, y = %.3f'%(y_in[i],y_in[i+1],y[i]))
    yerr = 1/np.sqrt(2)*np.sqrt(yerr_in[2*i]**2+yerr_in[2*i+1]**2)


model = sodr.Model(lin_func)
fit_data = sodr.RealData(x, y, sx=xerr, sy=yerr)
odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
out = odr.run()
a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0]
err_b = out.sd_beta[1]
y_fit= a*x+b

plt.figure(dpi=300)
plt.errorbar(x=x, y=y, xerr=xerr, yerr=yerr, marker=".", ls="", zorder=2)
plt.plot(x, y_fit, zorder=3, label='$U_0(1/\lambda)=(%.3f\cdot10^{-6})$Vnm $\cdot 1/\lambda$ %.3f V \n$h=\\frac{a\cdot c}{e}$=(%.3f $\pm$ %.3f)$\cdot 10^{-34}$ Js\n$W_A=\\frac{b}{e}=$(%.3f $\pm$ %.3f) eV' % (a*1e6,b,a*e/c*1e34, e/c*err_a*1e34, b, err_b))
plt.xlabel('$1/\lambda$ / $nm^{-1}$')
plt.ylabel('$U_0$ / V')
plt.legend()
#plt.show()
plt.savefig('../../pics/planck.png')
print('a=(%.3f$\pm$%.3f)$\cdot 10^{-6}$'%(a*1e6, err_a*1e6))
print('b=(%.3f \pm %.3f)'%(b, err_b))
