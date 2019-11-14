#Skript um sich alle möglichen Laueindices für einen Punkt anzeigen zu lassen. Diese müssen dann manuell ausgewählt werden.
from fractions import Fraction
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

#Imortiere Datensatz der mit KoordinatenConver.py erstellt wurde
data = genfromtxt('Koord.txt', delimiter=';')
x = np.array(data[1:, 3])
y = np.array(data[1:, 5])
z = np.array(data[1:, 7])

# l=[1,1,1,1,1,1,1,1]



for i in range(0, 8):
    j = np.linspace(1,10.1,1000)
    h = x[i]/z[i]*j
    k = y[i]/z[i]*j
    dif=np.abs(np.round(h,0)-h)+np.abs(np.round(k,0)-k)+np.abs(np.round(j,0)-j)
    plt.plot(j,dif, label=i+1)
    n = 1
    print('WWWWWWWWWWWWWWWWWWWWWWW')
    while j[n+1] < 10.:
        if dif[n-1]>dif[n] and dif[n+1]>dif[n]:
            l=j[n]
            a = x[i]/z[i]*l
            b = y[i]/z[i]*l
            if a<=10 and b<=10 and l<=10:
                print('%.2f %.2f %.2f' %(a,b,l))
            l = int(np.round(l))
            a = int(np.round(a))
            b = int(np.round(b))
            if a<=10 and b<=10 and l<=10:
                print(a,b,l)
                print('------------------')
            if (a==0):
                if((b+l)%2!=0):
                    a=2*a
                    b=2*b
                    l=2*l
            elif (b==0):
                if((a+l)%2!=0):
                    a=2*a
                    b=2*b
                    l=2*l
            elif (l==0):
                if((a+b)%2!=0):
                    a=2*a
                    b=2*b
                    l=2*l
            elif(a%2==0 and (b%2!=0 or l!=0) or b%2==0 and (l%2!=0 or a!=0) or l%2==0 and (a%2!=0 or b!=0)):
                    a=2*a
                    b=2*b
                    l=2*l
            if a<=10 and b<=10 and l<=10:
                # plt.text(x=j[n]-0.2, y=dif[n]-0.02, s="(%d %d %d)" % (a,b,l), fontsize=10)
                plt.plot(j[n], dif[n], 'x', label="(%d %d %d), (%.2f %.2f %.2f)" % (a,b,l, x[i]/z[i]*j[n], y[i]/z[i]*j[n], j[n]), ms=10)
        n += 1
    plt.legend(loc = 'upper right')
    plt.show()

#     l=j[np.where(dif == np.amin(dif))]
#     a = x[i]/z[i]*l
#     b = y[i]/z[i]*l
#     print(a,b,l)
#
# plt.show()
