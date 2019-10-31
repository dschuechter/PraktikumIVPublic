 #!/bin/bash

#führe für alle Oligamere plot_0_90.py aus
for f in $(cat messungen.txt); do
        tac backup/$f > $f
done
