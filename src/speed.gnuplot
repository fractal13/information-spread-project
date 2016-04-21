#!/usr/bin/env gnuplot

set xlabel "k (number of seeds)"
set ylabel "<t> (average time to select k seeds)"
set logscale y
plot "< ./print_result_file.py -i fbc-degree-30-10-05.json" using 1:3 with lines title "Degree", \
     "< ./print_result_file.py -i fbc-compact-30-10-05.json" using 1:3 with lines title "Compact", \
     "< ./print_result_file.py -i fbc-compactdegree-30-10-05.json" using 1:3 with lines title "Compact-Degree", \
     "< ./print_result_file.py -i fbc-compactdistance-30-10-05.json" using 1:3 with lines title "Compact-Distance", \
     "< ./print_result_file.py -i fbc-random-30-10-05.json" using 1:3 with lines title "Random", \
     "< ./print_result_file.py -i fbc-greedy-30-10-05.json" using 1:3 with lines title "Greedy"

pause -1
