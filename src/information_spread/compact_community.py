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

def score_edges(graph, lexcount):
    #
    # score the edges
    #
    
    ## set all scores to 0.0
    scores = {}
    edge = graph.BegEI()
    while edge < graph.EndEI():
        key = (edge.GetSrcNId(), edge.GetDstNId())
        scores[key] = 0.0
        edge.Next()

    ## average scores over lexcount runs
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

    #
    # done with edge scoring
    #
    return scores

def sort_edges(graph, scores):
    #
    # construct list of edges ordered by SCORE
    #
    edges = []
    edge = graph.BegEI()
    while edge < graph.EndEI():
        key = (edge.GetSrcNId(), edge.GetDstNId())
        edges.append( ((edge.GetSrcNId(), edge.GetDstNId(), scores[key])) )
        edge.Next()

    # we leave in ascending order to make pop() give the next edge we want.
    edges.sort(key = lambda e: e[2])
    
    #
    # done ordering list of edges
    #
    return edges

def initialize_clusters(graph):
    # initialize every node into its own cluster
    clusters = disjoint_set.DisjointSet(True)
    node = graph.BegNI()
    while node < graph.EndNI():
        clusters.makeset(node.GetId())
        node.Next()
    
    return clusters

def merge_communities_until_iteration(graph, edges, clusters, maxiter):
    """
    Merge by number of edges processed.
    """
    i = 0
    while (len(edges) > 0) and (i < maxiter):
        v1, v2, s = edges.pop()
        clusters.union(v1, v2)
        i += 1
    return clusters
    
def merge_communities_until_maxsize(graph, edges, clusters, maxsize):
    """
    Merge clusters until the largest is at least maxsize.
    Attempts to make the large important clusters first, and other clusters are not made.
    """
    currsize = 0
    while (len(edges) > 0) and (currsize < maxsize):
        v1, v2, s = edges.pop()
        clusters.union(v1, v2)
        s = clusters.get_set_size(v2)
        if s > currsize:
            currsize = s
    return clusters

def merge_communities_limit_cluster_size(graph, edges, clusters, max_cluster_size):
    """
    Merge clusters if result is no larger than max_cluster_size.
    Attempts to make clusters of approximately max_cluster_size
    """
    currsize = 0
    while (len(edges) > 0):
        v1, v2, s = edges.pop()
        s1 = clusters.get_set_size(v1)
        s2 = clusters.get_set_size(v2)
        if s1 + s2 <= max_cluster_size:
            clusters.union(v1, v2)
    return clusters


UNTIL_ITERATION = 1
UNTIL_MAXSIZE = 2
LIMIT_CLUSTER_SIZE = 3

def compact_community(graph, lexcount, which_version=UNTIL_ITERATION, parameter=-1):
    """
    Find compact communities in graph.  Average
    edge scores of lexcount trials.
    
    The hierachical clustering algorithm from Algorithm 2 of 
    "Finding compact communities in large graphs"
    by Creusefond, Largillier and Peyronnet.
    http://dx.doi.org/10.1145/2808797.2808868 
    """

    # Find edge scores and sort them
    scores = score_edges(graph, lexcount)
    edges = sort_edges(graph, scores)

    # create clusters based on choice
    clusters = initialize_clusters(graph)
    if which_version == UNTIL_ITERATION:
        maxiter = parameter
        clusters = merge_communities_until_iteration(graph, edges, clusters, maxiter)
    elif which_version == UNTIL_MAXSIZE:
        maxsize = parameter
        clusters = merge_communities_until_maxsize(graph, edges, clusters, maxsize)
    elif which_version == LIMIT_CLUSTER_SIZE:
        max_cluster_size = parameter
        clusters = merge_communities_limit_cluster_size(graph, edges, clusters, max_cluster_size)
    else:
        raise Exception("Bad option to compact community.")

    return clusters



