#Skript zur Erstellung der Referenzspektren inklusive angepassten Gaussfit
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.optimize import curve_fit
import scipy
from scipy import stats
import uncertainties.unumpy as unp
from uncertainties import ufloat

def energy(x):
	return x*69.72877-769.24188

def gauss(x, *p):
	b, c, d = p
	y = np.exp(-np.power(x - b, 2.) / (2 * np.power(c, 2.)))*d#+f
	#y =  stats.skewnorm.pdf(x , 0, b, c)*d+f
	return y

#probe=sys.argv[1]
plt.figure()#dpi=300)
g=1

def makespektrum(trans,dicke):
	print(probe+';')
	#plt.figure(0)
	data = genfromtxt(probe+'.txt', delimiter=';')
	x0 = data[1:, 0]
	y0 = data[1:, 1]
	plt.plot(energy(x0),y0, trans, label=probe, lw=dicke)
	# plt.figure(1)
	# plt.plot(x0,y0,'-')
	# plt.figure(0)

def makegauss(min1, min2, max):
	g=test
	data = genfromtxt(probe+'.txt', delimiter=';')
	x0 = data[1:, 0]
	y0 = data[1:, 1]
	i=0
	l=0
	while min1>=x0[l]:
		l += 1
	r=l
	while min2>=x0[r]:
		r += 1
	# l=min1
	# r=min2
	x = data[l:r, 0]
	#x=wellenlänge(x)
	y = data[l:r, 1]
	p_initial = [max,5,5000]
	#e = np.array([5 for _ in y])
	try:
		popt, pcov = curve_fit(gauss, x, y, p0=p_initial)
		x = np.linspace(x[0],x[-1],num=100)
		y_fit = gauss(x, *popt)
		#plt.plot(x, y_fit, color='black')
		perr = np.sqrt(np.diag(pcov))
		#print('%.4f;%.4f' %(popt[0],perr[0]))
		b = ufloat(popt[0], perr[0])
		c = ufloat(popt[1], perr[1])
		d = ufloat(popt[2], perr[2])
		#f = ufloat(popt[3], perr[3])
		h1 = unp.exp(-1/ (2 * np.power(b, 2.)))*d#+f
		# plt.figure(0)
		#plt.plot(energy(x), y_fit, '-.', color='black', alpha=0.3)
		x_pos = ufloat(popt[0], perr[0])
		x_pos = energy(x_pos)
		#plt.text(x=energy(popt[0])-200, y=gauss(popt[0], *popt)+100, s=g)
		g += 1
		#plt.plot(energy(popt[0]), gauss(popt[0], *popt), 'x')#, label='E = {:.0f}\n'.format(x_pos)+'$H_0$ = {:.1f}'.format(h1))
		print('{:.1f}'.format(x_pos)+'; {:.1f}'.format(h1))
		# plt.figure(1)
		# plt.plot(x, y_fit, color='black')
	except RuntimeError:
		print("Error - curve_fit failed")
	#test = g
	return g

print('E; $H_0$')
g=1
test=1
trans='--'
dicke=1
probe = 'Fe'
makespektrum(trans,dicke)
test = makegauss(95, 110, 103)

#########
# Darzustellende Proben ein bzw. auszukommentieren
#########

# probe = 'Ag'
# makespektrum(trans,dicke)
# test = makegauss(42, 65, 55)
# test = makegauss(125, 134, 127)
# test = makegauss(135, 147, 140)
# test = makegauss(318, 334, 325)
# test = makegauss(355, 375, 363)
# probe = 'Au'
# makespektrum(trans,dicke)
# test = makegauss(122, 140, 129)
# test = makegauss(145, 159, 151)
# test = makegauss(170, 185, 177)
# test = makegauss(196, 212, 204)
probe = 'Cu'
makespektrum(trans,dicke)
test = makegauss(122, 133, 127)
# probe = 'In'
# makespektrum(trans,dicke)
# test = makegauss(122, 137, 127)
# test = makegauss(50,70,60)
# test = makegauss(345, 359, 352)
# test = makegauss(384,407,395)
# probe = 'Mo'
# makespektrum(trans,dicke)
# test = makegauss(120,140,130)
# test = makegauss(254,268,260)
# test = makegauss(283,300,290)
# probe = 'Ni'
# makespektrum(trans,dicke)
# test = makegauss(113,126,119)
# probe = 'Pb'
# makespektrum(trans,dicke)
# test = makegauss(123,134,128)
# test = makegauss(138,148,142)
# test = makegauss(158,171,164)
# test = makegauss(188,200,192)
# test = makegauss(216,234,223)
# probe = 'Sn'
# makespektrum(trans,dicke)
# test = makegauss(53,70,61)
# test = makegauss(123,134,128)
# test = makegauss(360,375,366)
# probe = 'Ti'
# makespektrum(trans,dicke)
# test = makegauss(68,86,76)
# probe = 'W'
# makespektrum(trans,dicke)
# test = makegauss(130,143,133)
# test = makegauss(146,157,152)
# test = makegauss(169,183,175)
probe = 'Zn'
makespektrum(trans,dicke)
test = makegauss(130,143,133)
test = makegauss(146,157,152)
# probe = 'Zr'
# makespektrum(trans,dicke)
# test = makegauss(122,135,127)
# test = makegauss(232,243,237)
# test = makegauss(257,270,264)
trans='-'
dicke=1
# probe = 'Probe_1'
# makespektrum(trans,dicke)
# test = makegauss(83,92,87)
# test = makegauss(97,110,103)
# probe = 'Probe_2'
# makespektrum(trans,dicke)
# test = makegauss(120,132,127)
# test = makegauss(132,140,134)
probe = 'Probe_3'
makespektrum(trans,dicke)
test = makegauss(95,115,105)
test = makegauss(123,132,127)
test = makegauss(133,140,134)
# probe = 'Probe_4'
# makespektrum(trans,dicke)
# test = makegauss(83,99,91)
# test = makegauss(106,118,111)
# test = makegauss(134,147,150)


liml=00
limr=400

# plt.grid()
# plt.xlabel('Kanal / eV')
# plt.ylabel('Intensität')
# #plt.legend()
# plt.xlim(liml,limr)
# plt.savefig('test.png')

# plt.figure(0)
plt.grid()
plt.xlabel('Energie / eV')
plt.ylabel('Intensität')
plt.legend(labelspacing=0.2)#loc='upper center')
plt.xlim(energy(liml),energy(limr))
#plt.savefig(probe+'_material.png')
plt.savefig('test.png')
plt.show()
#plt.close()

# if sys.argv[2] == 'True':
# 	plt.figure(1)
# 	plt.show()

# x=[6397.3,8627.35]
# y=[h1.n,h2.n]
# yerr=[h1.s,h2.s]
