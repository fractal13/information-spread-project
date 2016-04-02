#!/usr/bin/env python

import snap
import random, os

def independent_cascade(graph, active_set_0, spread_probability):
    """
    graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
    active_set_0 is a Python set of node ids from graph that are initially active
    spread_probability is the probability that any node u, will activate node v if there is an edge (u, v)

    returns a Python set of the active node ids from the graph after the system has stabilized

    Implemented using description from section 2.2 of Kempe, Kleinberg and Tardos
    """

    final_active = set()
    newly_active = set()
    for a in active_set_0:
        final_active.add(a)
        newly_active.add(a)

    # Continue as long as there was propagation in the previous iteration
    while len(newly_active) > 0:
        
        previously_active = newly_active
        newly_active = set()
        
        # previously_active is the set of newly activated node ids from previous iteration
        # newly_active is the set of newly activated node ids from this iteration

        # give each previously activated node a chance to activate its neighbors
        for u_id in previously_active:
            u = graph.GetNI(u_id)
            # loop over the outgoing edges of u to try to activate neighbors
            for i in range(u.GetOutDeg()):
                v_id = u.GetOutNId(i)
                if v_id not in final_active:
                    if random.random() <= spread_probability:
                        newly_active.add(v_id)
                        final_active.add(v_id)
        
    return final_active

def independent_cascade_average_influence(graph, active_set_0, spread_probability, number_of_trials):
    """
    graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
    active_set_0 is a Python set of node ids from graph that are initially active
    spread_probability is the probability that any node u, will activate node v if there is an edge (u, v)
    number_of_trials is the number of runs to average influence over

    returns a number, the average number of activated nodes
    """

    total = 0.
    for i in range(number_of_trials):
        result = independent_cascade(graph, active_set_0, spread_probability)
        total += len(result)

    return total / float(number_of_trials)

def five_node_test():
    graph = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
    graph = snap.ConvertGraph(snap.PNEANet, graph)

    runs = 10000
    node = graph.BegNI()
    while node < graph.EndNI():
        
        active_set_0 = set([node.GetId()])
        spread_probability = 0.25
        result = independent_cascade_average_influence(graph, active_set_0, spread_probability, runs)
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
        result = independent_cascade_average_influence(graph, active_set_0, spread_probability, runs)
        if result > best:
            best = result
            best_id = node.GetId()
            print node.GetId(), " = ", result

        node.Next()

    
    return

def main():
    #five_node_test()
    texas_road_test()    
    return

if __name__ == "__main__":
    main()


