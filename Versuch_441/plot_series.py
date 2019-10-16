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

#Importiere darzustellende Reihe
row = sys.argv[1]
#anzahl einer Anordnung (z.B. 1A,...,1D = 4)
amount = sys.argv[2]


plt.figure()

#trage für jede messung einen Plot in die figure ein
j = int(amount)+1
i = 1
while i<j:
	#importiere die Daten der entsprechenden Messung (90 grad polarisation)
	#ersetze _90 durch _0 für 0 Grad polarisation
	file = chr(i+64)+row+"_90.txt"
	data = genfromtxt(file, delimiter='\t')
	x_0 = data[0:, 0]
	y_0 = data[0:, 1]
	plt.plot(x_0, y_0, '-', label=chr(i+64)+row)
	i += 1
#Generiere nun das Diagramm
plt.xlabel('$\lambda$/nm')
plt.ylabel('Transmision / %')
plt.legend(loc='lower left')
plt.xlim(500, 990)
plt.ylim(30, 110)
plt.savefig(row+"_plot_90.png")
