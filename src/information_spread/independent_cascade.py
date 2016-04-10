import snap
import random, os, time, sys

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

def measure_seed_sizes(graph, spread_probability, number_of_trials, selector, max_k):
    """
    graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
    spread_probability is the probability that any node u, will activate node v if there is an edge (u, v)
    number_of_trials is the number of runs to average influence and run time over
    selector is a object derived from SeedSelector, to generate seed sets
    max_k is an integer, the maximum desired number of seed nodes

    returns a Python list of triples.  The values are: k, average influence, average selector run time
    """

    results = []
    
    for k in range(1, max_k+1):
        print "k = %d - %s" % (k, time.asctime())
        active_set_0s = []
        t0 = time.clock()
        for i in range(number_of_trials):
            print "k = %d - trial = %d/%d - %s" % (k, i, number_of_trials, time.asctime())
            active_set_0s.append( selector.select_seeds(graph, k) )
            sections = "trail-loop"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";
        selection_time = time.clock() - t0
        print "k = %d - %s - selection time %f" % (k, time.asctime(), selection_time)
        
        total = 0.
        for i in range(number_of_trials):
            print "k = %d - trial = %d  - %s" % (k, i, time.asctime())
            active_set_0 = active_set_0s[i]
            result = independent_cascade(graph, active_set_0, spread_probability)
            total += len(result)
            
        result = total / float(number_of_trials)
        avg_selection_time = selection_time / float(number_of_trials)
        print "k = %d  result = %f  ast = %f  - %s" % (k, result, avg_selection_time, time.asctime())
        results.append( (k, result, avg_selection_time) )
        
    return results

