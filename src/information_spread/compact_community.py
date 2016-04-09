import snap
import LEXdfs, disjoint_set
import time

SCORE = "score"

def compact_community(graph, lexcount, maxiter):
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

    # set all scores to 0.0
    graph.AddFltAttrE(SCORE, 0.0)
    edge = graph.BegEI()
    while edge < graph.EndEI():
        graph.AddFltAttrDatE(edge, 0.0, SCORE)
        edge.Next()

    # average scores over lexcount runs
    m = float(graph.GetEdges())
    for i in range(lexcount):
        print "LEXdfs:", i, time.time()
        LEXdfs.LEXdfs(graph, graph.GetNI(graph.GetRndNId()))
        
        # adding current score to average
        edge = graph.BegEI()
        while edge < graph.EndEI():
            d = float(abs(graph.GetIntAttrDatN(edge.GetSrcNId(), LEXdfs.VISITED) -
                          graph.GetIntAttrDatN(edge.GetDstNId(), LEXdfs.VISITED)))
            s = 1.0 - d/m
            score = (graph.GetFltAttrDatE(edge, SCORE) * i + s) / (i+1)
            graph.AddFltAttrDatE(edge, s, SCORE)
            edge.Next()
        # done adding current score to average

    # done with edge scoring

    # construct list of edges ordered by SCORE
    edges = []
    edge = graph.BegEI()
    while edge < graph.EndEI():
        score = graph.GetFltAttrDatE(edge, SCORE)
        edges.append( ((edge.GetSrcNId(), edge.GetDstNId(), score)) )
        print "%d - %d : %f" % edges[-1]
        edge.Next()

    # we leave in ascending order to make pop() give the next edge we want.
    edges.sort(key = lambda e: e[2])

    print
    print
    print "Sorted"
    print
    for e in edges:
        print "%d - %d : %f" % e

    clusters = disjoint_set.DisjointSet(True)
    
    node = graph.BegNI()
    while node < graph.EndNI():
        clusters.makeset(node.GetId())
        node.Next()
        
    i = 0
    while len(edges) > 0 and i < maxiter:
        v1, v2, s = edges.pop()
        clusters.union(v1, v2)
        i += 1
    
    return clusters



