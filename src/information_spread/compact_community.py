import snap
import LEXdfs, disjoint_set
import random, os, sys, time
import resource

def debug_sleep_a(tag, t):
    usage = resource.getrusage(resource.RUSAGE_SELF);
    print "START", tag, "MEMORY: %d" % (usage[2])
    sys.stdout.flush()
    time.sleep(t)
    return
    
def debug_sleep_b(tag, t):
    usage = resource.getrusage(resource.RUSAGE_SELF);
    print "DONE ", tag, "MEMORY: %d" % (usage[2])
    sys.stdout.flush()
    time.sleep(t)
    return

SCORE = "score"

def compact_community(graph, lexcount, maxiter=-1, maxsize=-1):
    """
    Find compact communities in graph.  Average
    edge scores of lexcount trials.  Stop building
    the clusters after maxiter iterations.
    
    The hierachical clustering algorithm from Algorithm 2 of 
    "Finding compact communities in large graphs"
    by Creusefond, Largillier and Peyronnet.
    http://dx.doi.org/10.1145/2808797.2808868 
    """

    #
    # score the edges
    #

    scores = {}

    # debug_sleep_a("initial-edge-attributes", 1)
    # set all scores to 0.0
    edge = graph.BegEI()
    while edge < graph.EndEI():
        key = (edge.GetSrcNId(), edge.GetDstNId())
        scores[key] = 0.0
        edge.Next()
    # debug_sleep_b("initial-edge-attributes", 1)

    # average scores over lexcount runs
    m = float(graph.GetEdges())
    for i in range(lexcount):
        attrs = LEXdfs.LEXdfs(graph, graph.GetNI(graph.GetRndNId()))
        
        # adding current score to average
        edge = graph.BegEI()
        while edge < graph.EndEI():
            key = (edge.GetSrcNId(), edge.GetDstNId())
            
            d = float(abs(attrs[LEXdfs.VISITED][key[0]] -
                          attrs[LEXdfs.VISITED][key[1]]))
            s = 1.0 - d/m
            scores[key] = (scores[key] * i + s) / (i+1)
            edge.Next()
        # done adding current score to average

    # done with edge scoring

    # construct list of edges ordered by SCORE
    edges = []
    edge = graph.BegEI()
    midscore = 0.0
    while edge < graph.EndEI():
        key = (edge.GetSrcNId(), edge.GetDstNId())
        midscore += scores[key]
        edges.append( ((edge.GetSrcNId(), edge.GetDstNId(), scores[key])) )
        edge.Next()

    midscore /= len(edges)
    
    # we leave in ascending order to make pop() give the next edge we want.
    edges.sort(key = lambda e: e[2])
    clusters = disjoint_set.DisjointSet(True)
    
    node = graph.BegNI()
    while node < graph.EndNI():
        clusters.makeset(node.GetId())
        node.Next()

    i = 0
    currsize = 0
    while len(edges) > 0 and \
          (i < maxiter or (maxiter < 0 and edges[-1][2] > midscore)) and \
          ((maxsize < 0) or (currsize < maxsize)):
        v1, v2, s = edges.pop()
        if clusters.get_set_size(v1) >= maxsize or \
           clusters.get_set_size(v2) >= maxsize:
            # don't merge, would make too large
            pass
        else:
            clusters.union(v1, v2)
            i += 1
            s = clusters.get_set_size(v2)
            if s > currsize:
                currsize = s

    return clusters



