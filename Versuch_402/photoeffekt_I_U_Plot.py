#Plot zur Bestimmung der Grenzspannung U_0
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import genfromtxt
import scipy.odr as sodr
from uncertainties import ufloat

def lin_func(p, x):
     m, c = p
     return m * x + c
print('$\lambda$ / nm & $\Delta$$\lambda$ / nm & $U_0$ / V & $\Delta$ $U_0$/ V & $U_{0, exp} / V$ & $\Delta U_{0, exp} / V$')

def makeplot(wellenlaenge, messreihe, index):
    data = genfromtxt('Photoeffekt/'+str(wellenlaenge)+'nm_Messreihe_'+str(messreihe)+'-Table1.csv', delimiter=',')
    VF = 10**data[1,7]
    lamda = data[1, 0]
    lamda_error = 10
    I_0 = data[1, 1]*10*VF*1e-3
    I_0_error=0.5*VF*1e-3
    U_G = -data[1:, 3]
    U_G_error = data[1:, 4]
    I_Ph = data[1:, 5]*VF
    I_Ph_error = data[1:, 6]*VF
    #I_Ph_error = 0.03*VF
    U_0_manuel = data[1,2]
    U_0_manuel_error = 0.001

    x=U_G
    xerr=U_G_error
    y=np.sqrt(I_Ph-I_0)*1e6
    yerr=np.sqrt(I_Ph_error**2/(4*(I_Ph-I_0))+I_0_error**2/(4*(I_Ph-I_0)))*1e6


    model = sodr.Model(lin_func)
    fit_data = sodr.RealData(x[0:index], y[0:index], sx=xerr[0:index], sy=yerr[0:index])
    odr = sodr.ODR(fit_data, model, beta0=[0., 1.])
    out = odr.run()

    a = out.beta[0]
    b = out.beta[1]
    err_a = out.sd_beta[0]
    err_b = out.sd_beta[1]
    y_fit = a * U_G + b
    a=ufloat(a,err_a)
    b=ufloat(b,err_b)
    print(str(lamda)+'&10&'+str(-b/a)+'&%.3f&%.3f'%(-U_0_manuel, U_0_manuel_error))
    plt.figure(dpi=300)
    # plt.plot([x[0],x[-1]*1.05], [0,0], '-', color='black', alpha=0.5, zorder=0)
    # plt.plot([0,0], [y[0]*1.05,0], '-', color='black', alpha=0.5, zorder=0)
    plt.errorbar(x=x, y=y, xerr=xerr, yerr=yerr, marker=".", zorder=2)
    # plt.plot(x, y, '.')
    plt.plot(U_G, y_fit, label='$\sqrt{I_{Ph}-I_0}$ = ('+str(a)+')$\\frac{\sqrt{A}}{V}\cdot U_G$ + ('+str(b)+') $\sqrt{A}$\n $U_0$ = ('+str(-b/a)+') V', zorder=3)#, label='$\lambda_{min}/r$ =' a '+' b)#\lambda_{min}
    plt.xlabel('U$_G$ / V')
    plt.ylabel('$\sqrt{I_{Ph}-I_0}$ / $\sqrt{\mu A}$')
    plt.legend()
    plt.xlim(x[-1]*1.05,0)
    plt.ylim(0,y[0]*1.05)
    plt.savefig('../../pics/'+str(wellenlaenge)+'nm_Messreihe_'+str(messreihe)+'.png')
    plt.close()
    plt.show()



makeplot(365,1,7)
makeplot(365,2,5)
makeplot(365,3,19)
makeplot(405,1,7)
makeplot(405,2,4)
makeplot(436,1,6)
makeplot(436,2,4)
makeplot(546,1,4)
makeplot(546,2,6)
makeplot(578,1,4)
makeplot(578,2,4)
