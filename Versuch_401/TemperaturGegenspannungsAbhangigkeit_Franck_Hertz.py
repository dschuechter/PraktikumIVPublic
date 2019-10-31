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
data = genfromtxt(file, delimiter=',')
data2 = genfromtxt('Temp_Gegenspannungs_Abhaengigkeit/peaksTemp.txt', delimiter=';')
x0 = data[1:, 0]
y1 = data[1:, 2]
y0 = data2[:,11]
plt.plot(x0,y1, '.')

z = np.polyfit(x0, y1, 2)
f = np.poly1d(z)
print(f)
x_new = np.linspace(x0[0], x0[-1], 1000)
y_new = f(x_new)
plt.plot(x_new, y_new, '-', color='red', label='$U_{A, max}(T)=%.5f T^3$\n$ %.3f T^2+%.3f T+%.3f$' % (f[3],f[2],f[1],f[0]))


plt.legend()
plt.xlabel('$T / ^\circ C$')
plt.ylabel('$U_{Breite} / V$')
plt.savefig("Temp_Gegenspannungs_Abhaengigkeit/penis.png")
