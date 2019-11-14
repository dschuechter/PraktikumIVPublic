# Versuch 428: Röntgenstrahlung und Materialanalyse
In diesem Repository befinden sich sämtliche Programme und Datensätze die zur Auswertung des Versuchs 428 verwendet wurden.
Diese dienen ausschließlich zur Orientierung und nicht als eigens zu verwendende Datensätze.

Sämtliche Skripte sind in Python geschrieben und führen ihre Namensgebende Funktion aus.
Folgende Skripte gehören zu folgenden Teilversuchen und sollten nacheinander ausgeführt werden:
⋅⋅* **Bragg-Reflektion**: Schwerpunkte_40min.py, Schwerpunkte_12h.py
⋅⋅* **Materialanalyse**: Referenz.py, Masse.py
⋅⋅* **Laue-Aufnahme**: KoordinatenConverter.py, MillerShowAll.py, GenFromMiller.py, LauePlot.py

Alle Skripte außer Masse.py und KoordinatenConver.py sind zur Erstellung der Plots und deren Fits zuständig. Die meisten Skripte geben
die Resultate direkt als weiterverwendbaren Printout aus. Diese können dann kopiert oder direkt in text Dateien geschrieben werden.
Dies geschieht nach dem Schema 'python3 SkriptName.py > Ergebnisse.txt'

Die jeweiligen Skripte müssen in den Ordnern der Datensätze liegen oder der Dateipfad muss angegeben werden. Für mehr Details und Kommentare bitte in Versuch [441: Weißlichspektroskopie](https://github.com/dschuechter/PraktikumIVPublic/tree/master/Versuch_441) nachschauen. 
