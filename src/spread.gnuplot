#!/usr/bin/env gnuplot

set xlabel "k (number of seeds)"
set ylabel "<active size> (average size of final active set)"
plot "< ./print_result_file.py -i fbc-degree-k30-trials10-rate05-csize0.json" using 1:2 with lines title "Degree", \
     "< ./print_result_file.py -i fbc-compact-30-10-05.json" using 1:2 with lines title "Compact", \
     "< ./print_result_file.py -i fbc-compactdegree-30-10-05.json" using 1:2 with lines title "Compact-Degree", \
     "< ./print_result_file.py -i fbc-compactdistance-30-10-05.json" using 1:2 with lines title "Compact-Distance", \
     "< ./print_result_file.py -i fbc-random-k30-trials10-rate05-csize0.json" using 1:2 with lines title "Random", \
     "< ./print_result_file.py -i fbc-greedy-30-10-05.json" using 1:2 with lines title "Distance"

pause -1
