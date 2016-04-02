#!/usr/bin/env python
import snap
import sys, os
sys.path.append('../../src/information_spread')

import independent_cascade as IC
import random_seed as RS

def five_node_test():
    graph = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
    graph = snap.ConvertGraph(snap.PNEANet, graph)

    number_of_trials = 10000
    for k in range(1, 10):
        
        spread_probability = 0.25

        total = 0.
        for i in range(number_of_trials):
            active_set_0 = RS.select_random_seeds(graph, k)
            result = IC.independent_cascade(graph, active_set_0, spread_probability)
            total += len(result)
            
        result = total / float(number_of_trials)
        print k, result

    return

def texas_road_test():
    filename = "roadNet-TX.txt"
    if not os.path.exists(filename):
        print "You must create %s.  Try unzipping the file from the networks/roads directory" % (filename, )
        return

    graph = snap.LoadEdgeList(snap.PNGraph, filename)
    graph = snap.ConvertGraph(snap.PNEANet, graph)


    number_of_trials = 10
    for k in range(1, 30):
        
        spread_probability = 0.25

        total = 0.
        for i in range(number_of_trials):
            active_set_0 = RS.select_random_seeds(graph, k)
            result = IC.independent_cascade(graph, active_set_0, spread_probability)
            total += len(result)
            
        result = total / float(number_of_trials)
        print k, result
    
    return

def main():
    #five_node_test()
    texas_road_test()    
    return

if __name__ == "__main__":
    main()


