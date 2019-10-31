#!/usr/bin/env python3

import sys
import argparse
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse
from scipy.optimize import curve_fit
import chart_studio.plotly as py

plt.figure(dpi=300)
file = sys.argv[1]
data = genfromtxt(file, delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
z = np.polyfit(x0, y0, 5)
f = np.poly1d(z)
print(f)
x_new = np.linspace(x0[0], x0[-1], 1000)
y_new = f(x_new)
plt.plot(x0,y0,'.', ms=5)
plt.plot(x_new, y_new, '-', color='red', label='$B(I)=%.3f I^5 %.3f I^4+%.3f I^3$\n$ %.3f I^2+%.3f I+%.3f$' % (f[5],f[4],f[3],f[2],f[1],f[0]))
plt.legend()
plt.xlabel('I / A')
plt.ylabel('B / mT')
plt.savefig("B_Feld_Fit.png")
