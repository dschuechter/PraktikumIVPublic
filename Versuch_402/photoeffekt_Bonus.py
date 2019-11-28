#Erstelle "Bonus"-Plot -> Radius gegen Intensität
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
import scipy.odr as sodr
from uncertainties import ufloat
from scipy.optimize import curve_fit

def lin_func(p, x):
     m, c = p
     return m * x + c
plt.figure(dpi=300)
file = sys.argv[1]
data = genfromtxt(file, delimiter=',')
VF = 10**data[1,6]
lamda = data[1, 0]
lamda_error = 10
r = data[1:, 2]/2
r_error = data[1:, 3]/np.sqrt(2)
I_Ph = data[1:, 4]*VF
I_Ph_error = data[1:, 5]*VF
print(I_Ph*10**-data[1,6])

z = np.polyfit(r, I_Ph, 2)
f = np.poly1d(z)
x_new = np.linspace(r[0], r[-1], 1000)
y_new = f(x_new)

plt.plot(r, I_Ph, '.')
plt.errorbar(x=r, y=I_Ph, xerr=r_error, yerr=I_Ph_error, marker='.',linestyle = 'None')
plt.plot(x_new, y_new, label='$I_{Ph}(r)=%f\cdot r^2 + %f \cdot r  %.3f$' % (f[2]*1e10,f[1]*1e10,f[0]*1e10))
plt.xlabel('r / mm')
plt.ylabel('$I_{Ph} / A$')
plt.legend()
plt.savefig('../../pics/Photo_Bonus.png')
