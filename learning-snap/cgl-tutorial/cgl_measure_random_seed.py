#!/usr/bin/env python
import snap
import sys, os, time
sys.path.append('../../src/information_spread')

import independent_cascade as IC
import random_seed as RS

def five_node_test():
    graph = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
    graph = snap.ConvertGraph(snap.PNEANet, graph)

    number_of_trials = 1000
    spread_probability = 0.25
    selector = RS.RandomSeedSelector()
    max_k = 10

    results = IC.measure_seed_sizes(graph, spread_probability, number_of_trials, selector, max_k)
    for r in results:
        print r
    
    return

def texas_road_test():
    filename = "roadNet-TX.txt"
    if not os.path.exists(filename):
        print "You must create %s.  Try unzipping the file from the networks/roads directory" % (filename, )
        return

    graph = snap.LoadEdgeList(snap.PNGraph, filename)
    graph = snap.ConvertGraph(snap.PNEANet, graph)

    number_of_trials = 1
    spread_probability = 0.25
    selector = RS.RandomSeedSelector()
    max_k = 30

    results = IC.measure_seed_sizes(graph, spread_probability, number_of_trials, selector, max_k)
    for r in results:
        print r

    return

def main():
    five_node_test()
    #texas_road_test()    
    return

if __name__ == "__main__":
    main()


