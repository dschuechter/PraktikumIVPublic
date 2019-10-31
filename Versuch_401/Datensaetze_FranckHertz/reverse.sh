 #!/bin/bash

#führe für alle Oligamere plot_0_90.py aus
for f in $(cat messungen.txt); do
        python3 multiplegauss3.py $f >> new_file.txt
done
