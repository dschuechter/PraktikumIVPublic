# Versuch 441: Weißlichspektropskopie an Gold-Nano-Strukturen
In dieser Repository werden die verwendeten Datensätze und Programme zur Auswertung des Versuchs 441 angeführt.
Die Datensätze dürfen nicht für eigene Protokolle verwendet werden, dienen jedoch als Orientierung. Die Programme sollen
eine schnelle Auswertung ermöglichen.

## Verwendung
### Allgemeiner Hinweis
Alle Dateien müssen mit in den Ordner mit den Datensätzen kopiert oder die Dateipfade in den einzelnen Scripten angepasst werden!
Wird das nicht gemacht, funktionieren die Scripte nicht richtig.

### Aufbereitung der Datensätze
Um die Dazensätze aufzubereiten, das heißt, die Header und Footer Einträge von "Spectra Suite" zu entfernen muss das Shell Script
"remove.sh" in den betreffenden Ordner ausgeführt wernde. Anschließend befinden sich in diesem Ordner nur noch die bearbeiteten Datensätze.


### Generierung der Plots
Um die Plots zu generieren werden zwei Hilfsdateien benötigt. Zum einen die Datei "files.txt", die über den Befehl "ls *.txt > files.txt"
erzeugt werden kann (Achtung: in dieser Datei kann auch die Datei selbst aufgelistet werden. Diesen Eintrag vorher entfernen). Zum anderen
wird die Datei "cells.txt" benötigt, die die Probenbezeichnungen enthält.

Über das Shell-Script "plots.sh" wird das Python3 Script "plot_0_90.py" für alle Datensätze aufgerufen. Es werden nun für alle Datensätze
in einen Plot die 0 bzw. 90 Grad Polarisation dargestellt.

### Generierung von Übersichtsplots
Um eine Messreihe (z.B. A1-A5) zu generieren muss das Python3 Script "plot_series.py" mit dem Befehl "python3 plot_series.py $Messreihe $AnzahlDerEinträge"
($Messreihe und $AnzahlDerEinträge durch entsprechende Zahlen ersetzen) aufgerufen werden.
