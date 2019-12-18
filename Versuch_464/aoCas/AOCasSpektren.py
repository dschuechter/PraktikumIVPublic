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

plt.figure(dpi=300)

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
	#makegauss(file,data,left,right,erstens,zweitens,offset)
	plt.ylabel("Intensität")
	plt.xlabel("Wellenlänge $\lambda$ / nm")
	plt.plot([656.28,656.28],[offset*0.7,offset*1.5],color='red')
	plt.xlim(wellenlaengenconverter(left, *ab),wellenlaengenconverter(right, *ab))
	plt.title(file)
	#plt.show()
	plt.savefig('../../../pics/Spek_'+file+'.png');plt.clf()
	# plt.close()


plotten('2017-10-14',450,520,484,487,420)
plotten('2017-10-15A',450,505,478,484,210)
plotten('2017-10-15B',380,440,420,420,230)
plotten('2017-10-16A',400,430,414,425,120)
plotten('2017-10-16B',400,440,422,422,90)
plotten('2018-02-12',380,435,410,417,280)
plotten('2018-02-13',340,450,407,412,370)
plotten('2018-02-22',397,450,415,424,190)
plotten('2018-08-22',380,450,422,422,200)
plotten('2019-12-04',390,450,420,430,165)
