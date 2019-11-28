#Skript zur Berechnung der Gitterkonstante d
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

file = sys.argv[1]
data = genfromtxt(file, delimiter=';')
w_B = unumpy.uarray(data[1:, 0],[1,1,1,1,1,1,1,1,1,1,1,1,1])
w_G = unumpy.uarray(data[1:, 1],[1,1,1,1,1,1,1,1,1,1,1,1,1])
w_B_value = unp.nominal_values(w_B)
w_G_value = unp.nominal_values(w_G)

lamda = np.array([600.752,671.643,623.440,579.066,576.960,546.074,491.607,435.833,434.749,433.922,410.805,407.783,404.656])*1e-9

d = lamda/(unp.sin(unp.radians(w_G))-unp.sin(unp.radians(w_G)+unp.radians(w_B)))
d_no_error=unp.nominal_values(d)
d_error = unumpy.std_devs(d)
d_avarage=np.sum(d_no_error)/len(d_no_error)
d_avarage_error=1/np.sqrt(len(d_error))*np.sqrt(np.sum(d_error*d_error))
print('$\lambda$ / nm & $w_G$ / $^\circ$ & $w_B$ / $^\circ$ & d / nm & $\Delta$ d / nm')
for i in range(0,len(lamda)):
    print('%.3f & %.3f \pm %.3f& %.3f \pm %.3f& %.3f \pm %.3f \\\\'%(lamda[i]*1e9,w_G_value[i],1, w_B_value[i], 1, d_no_error[i]*1e9, d_error[i]*1e9))
print('d=(%.3f \pm %.3f)\cdot 10^{-9}m'%(d_avarage*1e9,d_avarage_error*1e9))
