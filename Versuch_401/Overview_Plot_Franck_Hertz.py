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

data = genfromtxt('165T_1V_gegen.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
plt.plot(x0, y0, '-', ms=2, label='T=$165^{\circ}C$, $U_{gegen}=1.0V$', color='indigo')

data = genfromtxt('165T_1_5V_gegen.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
plt.plot(x0, y0, '-', ms=2, label='T=$165^{\circ}C$, $U_{gegen}=1.5V$')

data = genfromtxt('165T_2V_gegen.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
plt.plot(x0, y0, '-', ms=2, label='T=$165^{\circ}C$, $U_{gegen}=2.0V$', color='chocolate')

data = genfromtxt('165T_2_5V_gegen.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
plt.plot(x0, y0, '-', ms=2, label='T=$165^{\circ}C$, $U_{gegen}=2.5V$')

for i in [3,4]:
    data = genfromtxt('165T_'+str(i)+'V_gegen.txt', delimiter=';')
    x0 = data[:, 0]
    y0= data[:, 1]
    plt.plot(x0, y0, '-', ms=2, label='T=$165^{\circ}C, U_{gegen}=%.1f V$' % (i))


for i in [172,175,180,185,190,195]:
    data = genfromtxt(str(i)+'T_2V_gegen.txt', delimiter=';')
    x0 = data[:, 0]
    y0= data[:, 1]
    plt.plot(x0, y0, '-', ms=2, label='$T=%d^{\circ}C, U_{gegen}=2.0V$' % (i))

data = genfromtxt('200T_2V_gegen.txt', delimiter=';')
x0 = data[:, 0]
y0= data[:, 1]
plt.plot(x0, y0, '-', ms=2, label='T=$200^{\circ}C$, $U_{gegen}=2.0V$', color='tomato')

plt.xlabel('$U_B / V$')
plt.ylabel('$U_A / V$')
plt.legend()
plt.savefig('Bilder/Overview.png')
