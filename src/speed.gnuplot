#!/usr/bin/env gnuplot

set xlabel "k (number of seeds)"
set ylabel "<t> (average time to select k seeds)"
set logscale y
plot "< ./print_result_file.py -i fbc-degree-k30-trials10-rate05-csize0.json" using 1:3 with lines title "Degree", \
     "< ./print_result_file.py -i fbc-random-k30-trials10-rate05-csize0.json" using 1:3 with lines title "Random", \
     "< ./print_result_file.py -i fbc-distance-k30-trials10-rate05-csize0.json" using 1:3 with lines title "Distance", \
     "< ./print_result_file.py -i fbc-compactdegree-k30-trials10-rate05-csize100.json" using 1:3 with lines title "Compact Deg 100", \
     "< ./print_result_file.py -i fbc-compactdegree-k30-trials10-rate05-csize200.json" using 1:3 with lines title "Compact Deg 200", \
     "< ./print_result_file.py -i fbc-compactdegree-k30-trials10-rate05-csize400.json" using 1:3 with lines title "Compact Deg 400", \
     "< ./print_result_file.py -i fbc-compactdistance-k30-trials10-rate05-csize100.json" using 1:3 with lines title "Compact Dist 100", \
     "< ./print_result_file.py -i fbc-compactdistance-k30-trials10-rate05-csize200.json" using 1:3 with lines title "Compact Dist 200", \
     "< ./print_result_file.py -i fbc-compactdistance-k30-trials10-rate05-csize400.json" using 1:3 with lines title "Compact Dist 400"

pause -1
