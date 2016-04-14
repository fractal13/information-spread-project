#
# Network - wcc distribution. G(100, 1000). Largest component has 1.000000 nodes (Sat Apr 02 19:01:44 2016)
#

set title "Network - wcc distribution. G(100, 1000). Largest component has 1.000000 nodes"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Size of weakly connected component"
set ylabel "Number of components"
set tics scale 2
set terminal png size 1000,800
set output 'wcc.example.png'
plot 	"wcc.example.tab" using 1:2 title "" with linespoints pt 6
