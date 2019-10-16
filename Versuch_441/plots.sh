#!/bin/bash

#führe für alle Oligamere plot_0_90.py aus
for f in $(cat cells.txt); do
        python3 plot_0_90.py $f
done
