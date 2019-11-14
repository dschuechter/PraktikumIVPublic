#Skript zu darstellung eines Symmetrischen Bildes aus Datensatz inklusive der ermittelten Miller Indizes
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.odr as sodr
from numpy import genfromtxt
import argparse
from scipy.optimize import curve_fit
plt.figure(dpi=300)
dataKoord = genfromtxt('Koord.txt', delimiter=';')
dataLaue = genfromtxt('LaueIndices.txt', delimiter=';')
x = np.array(dataKoord[1:, 3])
y = np.array(dataKoord[1:, 5])
x_error = np.array(dataKoord[1:, 4])
y_error = np.array(dataKoord[1:, 6])
h = np.array(dataLaue[1:, 0])
k = np.array(dataLaue[1:, 1])
l = np.array(dataLaue[1:, 2])
N=32
x_new=[0] * N
x_new_error =[0] * N
y_new=[0] * N
y_new_error=[0] * N
h_new = [0] * N
k_new = [0] * N
l_new = [0] * N
for i in range(0,4):
    for j in range(0,8):
        if(i==0):
            x_new[j]=x[j]
            y_new[j]=y[j]
            x_new_error[j]=x_error[j]
            y_new_error[j]=y_error[j]
            h_new[j]=h[j]
            k_new[j]=k[j]
            l_new[j]=l[j]
        if(i==1):
            x_new[j+i*8]=-x[j]
            y_new[j+i*8]=y[j]
            x_new_error[j+i*8]=x_error[j]
            y_new_error[j+i*8]=y_error[j]
            h_new[j+i*8]=-h[j]
            k_new[j+i*8]=k[j]
            l_new[j+i*8]=l[j]
        if(i==2):
            x_new[j+8*i]=x[j]
            y_new[j+8*i]=-y[j]
            x_new_error[j+8*i]=x_error[j]
            y_new_error[j+8*i]=y_error[j]
            h_new[j+i*8]=h[j]
            k_new[j+i*8]=-k[j]
            l_new[j+i*8]=l[j]
        if(i==3):
            x_new[j+8*i]=-x[j]
            y_new[j+8*i]=-y[j]
            x_new_error[j+8*i]=x_error[j]
            y_new_error[j+8*i]=y_error[j]
            h_new[j+i*8]=-h[j]
            k_new[j+i*8]=-k[j]
            l_new[j+i*8]=l[j]
M=8
Q=15
K=21
L=29
del x_new[M], y_new[M],x_new_error[M], y_new_error[M], h_new[M], k_new[M], l_new[M]
del x_new[Q], y_new[Q],x_new_error[Q], y_new_error[Q], h_new[Q], k_new[Q], l_new[Q]
del x_new[L], y_new[L],x_new_error[L], y_new_error[L], h_new[L], k_new[L], l_new[L]
del x_new[K], y_new[K],x_new_error[K], y_new_error[K], h_new[K], k_new[K], l_new[K]
plt.errorbar(x_new, y_new, xerr=x_new_error, yerr=y_new_error,
                 lw=2, fmt='.', ms=0)
print(l_new)
for i in range(0,len(x_new)):
    plt.text(x=x_new[i]-0.1, y=y_new[i]+0.03, s="(%d %d %d)" % (h_new[i],k_new[i],l_new[i]), fontsize=10)

plt.xlabel('x / cm')
plt.ylabel('y / cm')
#plt.plot(x_new,y_new, '.',ms=100)
plt.savefig('test.png')
