#!/usr/bin/env python3

import sys
import argparse

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse

def lin_func(p, x):
     m, c = p
     return m * x + c

file = sys.argv[1]
data = genfromtxt(file+'.csv', delimiter=',')
x = data[1:, 0]
x_err = data[1:, 1]
y = data[1:, 2]
y_err = data[1:, 3]

model = sodr.Model(lin_func)
fit_data = sodr.RealData(x, y, sx=x_err, sy=y_err)
odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
out = odr.run()

a = out.beta[0]
b = out.beta[1]
err_a = out.sd_beta[0]
err_b = out.sd_beta[1]


print("Fitergebnis:\n")
print("y = a * x + b mit\n")
print("a = {:.5f} +/- {:.5f}".format(a, err_a))
print("b = {:.5f} +/- {:.5f}".format(b, err_b))

y_fit = a * x + b

plt.figure(dpi=300)
plt.errorbar(x, y, xerr=x_err, yerr=y_err, lw=2, fmt='.')
plt.plot(x, y_fit, lw=2, label='$\lambda_{min}/r$ = (%.2f $\pm$ %.2f)' % (a,err_a) +' nm/nm')#\lambda_{min}
XAchse = sys.argv[2]
plt.xlabel(XAchse+' / nm')
plt.ylabel('$\lambda_{min}$ / nm')
plt.plot([], [], ' ', label='c = (%.2f $\pm$ %.2f) ' % (b,err_b)+'nm')
plt.legend(loc='upper left')
plt.savefig(file+".png")
#plt.show()
