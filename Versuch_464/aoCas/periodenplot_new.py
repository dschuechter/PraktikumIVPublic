#!/usr/bin/env python3

import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
from scipy import stats
import scipy
import scipy.odr as sodr
import datetime, time
import uncertainties.unumpy as unp
from uncertainties import ufloat

plt.figure(dpi=300)
T=3.52348
def sinus(x, *p):
    K, c, d = p
    if abs(c) < abs(K*0.1):
        return K*np.sin(2.*np.pi*x+d)+c
    return 1e30

def getphase(x):
    while x>T:
        x = x-T
    return x/T

def speed(y):
    #s = 656.28
    s = 656.45377
    c = 300000
    # return (halpha/y-1)*c
    return c*(s*s-y*y)/(s*s+y*y)

file = 'speed.txt'# sys.argv[1]
data = genfromtxt(file, delimiter=';')
time = data[:,0]
timeerr = data[:,1]
phi = np.zeros(len(time))
phierr = np.zeros(len(time))
for i in range(0,len(phi)):
    phi[i] = getphase(time[i])
    # print(phi,'; ')
    phierr[i] = getphase(timeerr[i]/60/60/24)
# print(phi, phierr)

N=10
speed1 = data[:,2]
errspeed1 = data[:,3]
speed2 = data[:,4]
errspeed2 = data[:,5]
plt.errorbar(phi[0:N],speed1[0:N],yerr=errspeed1,marker='x',ls='')
plt.errorbar(phi[0:N],speed2[0:N],yerr=errspeed2,marker='x',ls='')

p=[270,-1,0]
p=[186.39269462, -18.6392693,   -1.25291425]
# b=[[0,600],[0,np.inf],[-100,100]]
x = np.linspace(0,1,num=1000)
y_fit=sinus(x, *p)
# plt.plot(x, y_fit, color='peachpuff',zorder=3)
popt, pcov = curve_fit(sinus, phi[0:N], speed1[0:N], p0=p, sigma=errspeed1[0:N])#, bounds=b)
perr = np.sqrt(np.diag(pcov))
y_fit=sinus(x, *popt)
#print(popt)
# print(popt[1],perr[1])
K1=ufloat(abs(popt[0]),perr[0])
plt.plot(x, y_fit, color='green',zorder=3)

p=[-200,-18,-1.3]
x = np.linspace(0,1,num=1000)
y_fit=sinus(x, *p)
# plt.plot(x, y_fit, color='deepskyblue',zorder=3)
popt, pcov = curve_fit(sinus, phi[0:N], speed2[0:N], p0=p, sigma=errspeed2[0:N])#, bounds=b)
perr = np.sqrt(np.diag(pcov))
y_fit=sinus(x, *popt)
#print(popt)
print(popt[1],perr[1])
K2=ufloat(abs(popt[0]),perr[0])
plt.plot(x, y_fit, color='deepskyblue',zorder=3)
plt.ylabel("Geschwindigkeit $v_i$ /km $s^{-1}$")
plt.xlabel('Phase $\\varphi$ des Systems')
plt.savefig('AOCass.png')
plt.savefig('../../../pics/AOCass.png')
# for i in range(0,len(phi)):
#     plt.plot([phi[i],phi[i]], [-200,200])

# A = phi
# B = np.linspace(-200,200,num=len(phi))
# i=1
# for xy in zip(A, B):                                       # <--
#     plt.annotate(i, xy=xy,xytext=(-6,0), textcoords='offset points', ha='center')
#     i+=1

# plt.plot(phi, y1, '+')
# plt.plot(phi, y2, 'x')


data_time = genfromtxt('time_delimiter.txt', delimiter=';')
year = data_time[1:,0]
mounth = data_time[1:,1]
day = data_time[1:,2]
hour = data_time[1:,3]
min = data_time[1:,4]
sek = data_time[1:,5]
reldays = data_time[1:,6]
print('\n')
print('Messung & Datum & Uhrzeit & t / Tage & $\phi$ & $v_1$ / km$s^{-1}$& $v_2$ / km$s^{-1}$\\\\')
print('\\hline')
for i in range(0, len(data_time)-1):
    print('%d & %d.%.d.%.d & %d:%d:%d & %.3f & %.3f & %.3f $\pm$ %.3f & %.3f $\pm$ %.3f\\\\'%(i+1,day[i],mounth[i],year[i], hour[i],min[i],sek[i], reldays[i], phi[i], speed1[i],errspeed1[i], speed2[i], errspeed2[i]))
    #print(data_time)

#print(date)


print('\nMasse K usw.')
print(K1,K2)
K=(K1+K2)
print(K)
K=K*1e3
i=1.032013
# i=65.7
G=6.67430e-11
P=T*24*60*60
M=P*K**3/(2*np.pi*G)/np.sin(i)**3
print('Masse / kg: ',M)
print('Masse / Sonnenmasse: ',M/2e30)
M1=np.power((P*M**2/(2*np.pi*G)),1/3)/unp.sin(i)*K2*1e3
M2=np.power((P*M**2/(2*np.pi*G)),1/3)/unp.sin(i)*K1*1e3
print(M1/2e30,M2/2e30)
print(M1/2e30+M2/2e30)
