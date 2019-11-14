#Skript zur Umwandlung von Koordinaten in pixeln zu Koordinaten in cm
#Zum direkten speichern der Ergebnisse 'python3 KoordinatenConverter.py > Koord.txt' ausführen
import numpy as np
from numpy import genfromtxt
#Importiere Koordinaten in Pixeln
data = genfromtxt('Koordinaten.txt', delimiter=';')
x_px = data[1:, 1]
y_px= data[1:, 2]
x_cm = [0,0,0,0,0,0,0,0]
y_cm = [0,0,0,0,0,0,0,0]
x_cm_error = [0,0,0,0,0,0,0,0]
y_cm_error = [0,0,0,0,0,0,0,0]
z_cm = [0,0,0,0,0,0,0,0]
z_cm_error = [0,0,0,0,0,0,0,0]
L=1.5
L_error = 0.1
#Ermittelter Umrechnungsfaktor
s = 0.002143
s_error = 0.000023
px_error = 3
for i in range(0, len(x_px)):
    x_cm[i] = x_px[i]*s
    y_cm[i] = y_px[i]*s
    x_cm_error[i] = np.sqrt((px_error*s)**2.+(s_error*x_px[i])**2.)
    y_cm_error[i] = np.sqrt((px_error*s)**2+(s_error*y_px[i])**2)
    z_cm[i] = np.sqrt(x_cm[i]**2+y_cm[i]**2+L**2)-L
    z_cm_error[i] = np.sqrt((x_cm[i]/(np.sqrt(x_cm[i]**2.+y_cm[i]**2.+L**2.))*x_cm_error[i])**2.+(y_cm[i]/np.sqrt(x_cm[i]**2+y_cm[i]**2+L**2)*y_cm_error[i])**2+(L*(1/np.sqrt(x_cm[i]**2+y_cm[i]**2+L**2)-1)*L_error)**2)
#Gebe alle Koordinaten inklusive Fehlern in CSV-kompatibler Syntax aus.
print('Nummer; x/px; y/px; x/cm; $\Delta$ x / cm; y / cm; $\Delta$ y / cm; z / cm; $\Delta$ z / cm ')
for i in range(0, len(x_px)):
    print('%d;%.d;%.d;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f' %(i+1,x_px[i], y_px[i], x_cm[i], x_cm_error[i], y_cm[i], y_cm_error[i], z_cm[i], z_cm_error[i]))
