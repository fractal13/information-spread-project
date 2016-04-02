#!/usr/bin/env python
import snap
import sys
sys.path.append('../../src/information_spread')

import independent_cascade

def five_node_test():
    graph = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
    graph = snap.ConvertGraph(snap.PNEANet, graph)

    runs = 10000
    node = graph.BegNI()
    while node < graph.EndNI():
        
        active_set_0 = set([node.GetId()])
        spread_probability = 0.25
        result = independent_cascade.independent_cascade_average_influence(graph, active_set_0, spread_probability, runs)
        print node.GetId(), " = ", result

        node.Next()

    return

def texas_road_test():
    filename = "roadNet-TX.txt"
    if not os.path.exists(filename):
        print "You must create %s.  Try unzipping the file from the networks/roads directory" % (filename, )
        return

    graph = snap.LoadEdgeList(snap.PNGraph, filename)
    graph = snap.ConvertGraph(snap.PNEANet, graph)
        
    runs = 10
    node = graph.BegNI()
    best = 0.
    best_id = 0
    while node < graph.EndNI():
        
        active_set_0 = set([node.GetId()])
        spread_probability = 0.25
        result = independent_cascade.independent_cascade_average_influence(graph, active_set_0, spread_probability, runs)
        if result > best:
            best = result
            best_id = node.GetId()
            print node.GetId(), " = ", result

        node.Next()

    
    return

def main():
    five_node_test()
    #texas_road_test()    
    return

if __name__ == "__main__":
    main()


