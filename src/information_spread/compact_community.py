import snap
import LEXdfs, disjoint_set
import random, os, sys, time

SCORE = "score"

def compact_community(graph, lexcount, maxiter=-1):
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

    sections = "initial-edge-attributes"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";
    # set all scores to 0.0
    graph.AddFltAttrE(SCORE, 0.0)
    edge = graph.BegEI()
    while edge < graph.EndEI():
        graph.AddFltAttrDatE(edge, 0.0, SCORE)
        edge.Next()
    sections = "initialization-done"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";

    # average scores over lexcount runs
    m = float(graph.GetEdges())
    for i in range(lexcount):
        # print "LEXdfs:", i, time.time()
        sections = "LEXdfs"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(10); print "SLEPT";
        LEXdfs.LEXdfs(graph, graph.GetNI(graph.GetRndNId()))
        
        sections = "score-edges"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(10); print "SLEPT";
        # adding current score to average
        edge = graph.BegEI()
        while edge < graph.EndEI():
            d = float(abs(graph.GetIntAttrDatN(edge.GetSrcNId(), LEXdfs.VISITED) -
                          graph.GetIntAttrDatN(edge.GetDstNId(), LEXdfs.VISITED)))
            s = 1.0 - d/m
            score = (graph.GetFltAttrDatE(edge, SCORE) * i + s) / (i+1)
            graph.DelAttrDatE(edge, SCORE)
            graph.AddFltAttrDatE(edge, s, SCORE)
            edge.Next()
        # done adding current score to average

    # done with edge scoring

    sections = "make-edges-list"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";
    # construct list of edges ordered by SCORE
    edges = []
    edge = graph.BegEI()
    midscore = 0.0
    while edge < graph.EndEI():
        score = graph.GetFltAttrDatE(edge, SCORE)
        midscore += score
        edges.append( ((edge.GetSrcNId(), edge.GetDstNId(), score)) )
        # print "%d - %d : %f" % edges[-1]
        edge.Next()

    midscore /= len(edges)
    
    # we leave in ascending order to make pop() give the next edge we want.
    edges.sort(key = lambda e: e[2])
    # print
    # print
    # print "Sorted"
    # print
    # for e in edges:
    #     print "%d - %d : %f" % e

    sections = "grow-clusters"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";
    clusters = disjoint_set.DisjointSet(True)
    
    node = graph.BegNI()
    while node < graph.EndNI():
        clusters.makeset(node.GetId())
        node.Next()

    i = 0
    while len(edges) > 0 and (i < maxiter or (maxiter < 0 and edges[-1][2] > midscore)):
        v1, v2, s = edges.pop()
        # print s, midscore
        clusters.union(v1, v2)
        i += 1
    # print "done:", edges[-1][2], midscore
    sections = "clusters-done"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";
    return clusters



