#Mit diesem Skript lassen sich aus eingelesenen Miller Indizes die zugehörigen Gitterabstände,
#Glanzwinkel und Wellenlängen bestimmen.

from fractions import Fraction
import numpy as np
from numpy import genfromtxt
import uncertainties.unumpy as unp
from uncertainties import ufloat

dataMiller = genfromtxt('LaueIndices.txt', delimiter=';')
h = np.array(dataMiller[1:, 0], dtype='int')
k = np.array(dataMiller[1:, 1], dtype='int')
l = np.array(dataMiller[1:, 2], dtype='int')

dataKoord = genfromtxt('Koord.txt', delimiter=';')
x = unp.uarray(dataKoord[1:, 3],dataKoord[1:, 4])
y = unp.uarray(dataKoord[1:, 5],dataKoord[1:, 6])
z = unp.uarray(dataKoord[1:, 7],dataKoord[1:, 8])

a=564.02e-12 #Gitterkonstante https://de.wikipedia.org/wiki/Natriumchlorid

d = a/(unp.sqrt(h**2+k**2+l**2))
teta = unp.arctan(l/unp.sqrt(h**2+k**2))
tetaKoord = unp.arctan(z/unp.sqrt(x**2+y**2))
lamda = 2*d*unp.sin(teta)

print('Abstand d / pm; $\\teta / ^\circ$; $\lambda$ / pm')
for i in range(0,8):
    print('%.3f'%(d[i]*1e12),180/np.pi*teta[i],lamda[i]*1e12, tetaKoord[i])
