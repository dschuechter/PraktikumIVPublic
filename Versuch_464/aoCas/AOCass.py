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

def gauss(x, *p):
	b, c, d, b1, c1, d1, f = p;return stats.skewnorm.pdf(x , 0, b, c)*(-np.absolute(d))+stats.skewnorm.pdf(x , 0, b1, c1)*(-np.absolute(d1))+f
    # y =  stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+f
    # return stats.skewnorm.pdf(x , 0, b, c)*d+stats.skewnorm.pdf(x , 0, b1, c1)*d1+f

def gaussneg(x, b, c, d, f):
	return stats.skewnorm.pdf(x , 0, b, c)*(-np.absolute(d))+f

def lin_func(p, x):
     m, c = p
     return m * x + c

def wellenlaengenconverterfit(file):
    kalifile = './kali/'+file+'_kali'
    data = genfromtxt(kalifile, delimiter=';')
    y = data[:, 0] #Wellenlänge
    x = data[:, 1] #Pixelpos
    xerr = [1]*len(x) #Pixelfehler
    yerr = [0.1]*len(y) #Wellenlängenfehler

    model = sodr.Model(lin_func)
    fit_data = sodr.RealData(x[0:], y[0:], sx=xerr[0:], sy=yerr[0:])
    odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
    out = odr.run()
    a = out.beta[0]
    b = out.beta[1]
    return a,b

def wellenlaengenconverter(x, *p):
	a,b=p
	return (a*x+b)/10

def antiwellenlaengenconverter(x, *p):
	a,b=p
	return (x-b)/a

def wellenerr(x, *p):
	a,b=p
	return x*a

def makegauss(file,data,left,right,erstens,zweitens,offset):
	x = data[left:right,0]
	y = data[left:right,1]
	# anfangsparrameter
	p=[erstens,5,50,zweitens,5,50,offset]
	# finde eine Passende funktion die an die Messwerte passt.
	popt, pcov = curve_fit(gauss, x, y, p0=p)
	perr = np.sqrt(np.diag(pcov))
	x = np.linspace(x[0],x[-1],num=1000)
	y_fit = gauss(x, *popt)
	# print(popt)
	# print(perr)
	a,b,c=popt[0:3]
	y_fit_1 = gaussneg(x, a,b,c,popt[6])
	a,b,c=popt[3:6]
	y_fit_2 = gaussneg(x, a,b,c,popt[6])
	ab=wellenlaengenconverterfit(file)
	x = wellenlaengenconverter(x, *ab)
	erstens = wellenlaengenconverter(popt[0], *ab)
	errerstens = wellenerr(perr[0], *ab)
	# print(perr[0])
	# print(errerstens)
	zweitens = wellenlaengenconverter(popt[3], *ab)
	errzweitens = wellenerr(perr[3], *ab)
	print(file,np.round(erstens,3),np.round(errerstens,3),np.round(zweitens,3),np.round(errzweitens,3))
	plt.plot(x, y_fit, color='black',zorder=3)#,alpha=0.6)
	plt.plot(x, y_fit_1, '--', color='black',zorder=3)#,alpha=0.4)
	plt.plot(x, y_fit_2, '--', color='black',zorder=3)#,alpha=0.4)


def plotten(file,left,right,erstens,zweitens,offset):
	#file = sys.argv[1]
	data = genfromtxt('./data/'+file, delimiter='\t')
	x = data[0:, 0]
	y = data[0:, 1]
	# p = wellenlaengenconverterfit()
	# x = wellenlaengenconverter(x, *p)
	ab=wellenlaengenconverterfit(file)
	x = wellenlaengenconverter(x, *ab)
	plt.plot(x, y, '-',zorder=4,lw=2)
	# y= (data[0:, 2])-1000
	# plt.plot(x, y, '-',zorder=1)
	makegauss(file,data,left,right,erstens,zweitens,offset)
	plt.ylabel("Intensität")
	plt.xlabel("Wellenlänge $\lambda$ / nm")
	plt.plot([656.28,656.28],[offset*0.7,offset*1.05],color='red')
	plt.xlim(wellenlaengenconverter(left, *ab),wellenlaengenconverter(right, *ab))
	plt.title(file)
	plt.show()
	# plt.savefig(file+'.png')
	# plt.close()

def simplegauss(x, *p):
	b, c, d, f = p;return stats.skewnorm.pdf(x , 0, b, c)*(-np.absolute(d))+f

def makesimplegauss(file,data,left,right,erstens,zweitens,offset):
	x = data[left:right,0]
	y = data[left:right,1]
	# anfangsparrameter
	p=[erstens,5,100,offset]#,zweitens,1,100,offset]
	# finde eine Passende funktion die an die Messwerte passt.
	popt, pcov = curve_fit(simplegauss, x, y, p0=p)
	perr = np.sqrt(np.diag(pcov))
	x = np.linspace(x[0],x[-1],num=1000)
	y_fit = simplegauss(x, *popt)
	# print(popt)
	a,b,c=popt[0:3]
	y_fit_1 = gaussneg(x, a,b,c,popt[3])
	# a,b,c=popt[3:6]
	# y_fit_2 = gaussneg(x, a,b,c,popt[6])
	ab=wellenlaengenconverterfit(file)
	x = wellenlaengenconverter(x, *ab)
	minimum = wellenlaengenconverter(popt[0], *ab)
	errminimum = wellenerr(perr[0], *ab)
	print(file,np.round(minimum,3),np.round(errminimum,3))
	plt.plot(x, y_fit, color='black',zorder=3)#,alpha=0.6)
	plt.plot(x, y_fit_1, '--', color='black',zorder=3)#,alpha=0.4)

def simpleplotten(file,left,right,erstens,zweitens,offset):
	#file = sys.argv[1]
	data = genfromtxt('./data/'+file, delimiter='\t')
	x = data[0:, 0]
	y = data[0:, 1]
	# p = wellenlaengenconverterfit()
	# x = wellenlaengenconverter(x, *p)
	ab=wellenlaengenconverterfit(file)
	x = wellenlaengenconverter(x, *ab)
	plt.plot(x, y, '-',zorder=4,lw=2)
	# y= (data[0:, 2])-1000
	# plt.plot(x, y, '-',zorder=1)
	makesimplegauss(file,data,left,right,erstens,zweitens,offset)
	plt.ylabel("Intensität")
	plt.xlabel("Wellenlänge $\lambda$ / nm")
	plt.plot([656.28,656.28],[offset*0.7,offset*1.05],color='red')
	plt.xlim(wellenlaengenconverter(left, *ab),wellenlaengenconverter(right, *ab))
	plt.title(file)
	plt.show()
	# plt.savefig(file+'.png')
	# plt.close()

# plotten(file,left,right,erstens,zweitens,offset)
plotten('2017-10-14',450,520,484,487,420)
plotten('2017-10-15A',450,505,478,484,210)
plotten('2017-10-15B',380,440,420,420,230)
plotten('2017-10-16A',400,430,414,425,120)
simpleplotten('2017-10-16B',400,440,422,422,90)
plotten('2018-02-12',380,435,410,417,280)
plotten('2018-02-13',340,450,407,412,370)
plotten('2018-02-22',397,450,415,424,190)
simpleplotten('2018-08-22',380,450,422,422,200)
plotten('2019-12-04',390,450,420,430,165)
