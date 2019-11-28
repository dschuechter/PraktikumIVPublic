#Berechne für Literaturwerte die Dopplerverbreiterung
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
import scipy
from scipy import stats
from uncertainties import unumpy
import uncertainties.unumpy as unp
from uncertainties import ufloat
import scipy.odr as sodr

k_B=1.380649*1e-23
T = 1000
m = 1.00784*1.660*1e-27
lamda = np.array([656.279,486.133,434.047,410.173,397.008])
c = 299792458
delta_lamda = lamda/c*np.sqrt((8*k_B*T*np.log(2))/(m))

print(delta_lamda)
