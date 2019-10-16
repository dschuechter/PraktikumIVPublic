#!/bin/bash

#Mit diesem Skript lassen sich die Header und Footer Einträger
#in den Datensätzen von "SpectraSuite Data Files" schnell entfernen.
#Es wird eine files.txt Datei benötigt, die z.B. über "ls *.txt > files.txt" 
#generiert werden kann. Potentiell wird die files.txt selbst als Eintrag gelistet
#und muss demnach entfernt werden.

for f in $(cat files.txt); do
        tail -n +18 "$f" > "temp.txt"
        mv "temp.txt" "$f"
        sed -i '' -e '$ d' $f
done
