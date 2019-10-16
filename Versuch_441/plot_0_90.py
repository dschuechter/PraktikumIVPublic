#!/usr/bin/env python3

#Importiere notwendige Pakete
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse

#Welche Olimere dargestellt werden sollen
cell = sys.argv[1]
file_0 = cell+"_0.txt"
file_90 = cell+"_90.txt"

#Importiere Datensatz und erstelle Vektoren
#Hier bei einer 0 Grad Polarisation
data_0 = genfromtxt(file_0, delimiter='\t')
x_0 = data_0[0:, 0]
y_0 = data_0[0:, 1]

#Hier bei einer 90 Grad Polarisation
data_90 = genfromtxt(file_90, delimiter='\t')
x_90 = data_90[0:, 0]
y_90 = data_90[0:, 1]

#Darstellung der Datensätze der jeweiligen Probe mit beiden
#Polarisationen in einem Diagramm
plt.figure()
plt.plot(x_0, y_0, '-', label='$0^{\circ}$ Polarisation')
plt.plot(x_90, y_90, '-', label='$90^{\circ}$  Polarisation')
plt.xlabel('$\lambda$ / nm')
plt.ylabel('Transmision / %')
plt.legend(loc='lower left')
plt.xlim(500, 1000)
plt.ylim(30, 110)
plt.grid()
plt.savefig(cell+"_plot.png")
