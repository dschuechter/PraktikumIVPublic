#Skript zur Massenbestimmung aus Peakhöhen eines Probe und Referenzspektrums
import uncertainties.unumpy as unp
from uncertainties import ufloat

CH_0 = ufloat(5656,76)
CH = ufloat(3773,74)
Cp = 7.14

ZH_0 = ufloat(5337,72)
ZH = ufloat(3138,29)
Zp = 8.96

Ccu = (Cp*CH/CH_0)/((Cp*CH/CH_0+Zp*ZH/ZH_0))
Czn = (Zp*ZH/ZH_0)/((Cp*CH/CH_0+Zp*ZH/ZH_0))

print(Ccu)
print(Czn)
