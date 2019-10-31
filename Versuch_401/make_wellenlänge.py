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
from scipy import stats

file = ['5_5A','6_0A','6_5A','7_0A','7_3A','7_5A','8_0A','8_5A','8_7A','9_1A','9_3A']

# center die msswerte
for f in [0,1,2,3,4,5,6,7,8,9,10]:
    data = genfromtxt(file[f]+'.txt', delimiter=';')
    x0 = data[0:, 0]
    y0 = data[0:, 1]
    x = x0-0.013624114364866935
    f = open(file[f]+"_c.txt", "wt")
    for i in range(0,2048):
        pr=str(x[i])+';'+str(y0[i])
        print(pr, file=f)
    f.close()
