#!/usr/bin/env python3
#Tool für einfache Plots
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt

file = sys.argv[1]
data = genfromtxt(file, delimiter=';')
x = data[1:, 0]
y= data[1:, 1]
plt.plot(x, y, 'x')

plt.show()
