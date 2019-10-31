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

plt.figure(dpi=300)
x = np.linspace(1,3000)
y = np.exp(10.55-3333/x-0.85*np.log(x))
plt.plot(x, y, '-', label='$p(T)=\exp(10.55-3333/T-0.85\cdot\log(T))$')

plt.xlabel('T / K')
plt.ylabel('p(T) / Torr')
plt.legend()
plt.savefig("dampfdruckkurve.png")
#plt.show()
