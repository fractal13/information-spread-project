import snap
import random, os, sys, time

import seed_selector
import compact_community

# lifted from stackoverflow
def copy_graph(graph):
    tmpfile = '.copy.bin'

    # Saving to tmp file
    FOut = snap.TFOut(tmpfile)
    graph.Save(FOut)
    FOut.Flush()

    # Loading to new graph
    FIn = snap.TFIn(tmpfile)
    graphtype = type(graph)
    new_graph = graphtype.New()
    new_graph = new_graph.Load(FIn)

    os.remove(tmpfile)
    
    return new_graph

def average_bfs_distance(graph, node_id, community):
    """
    finds the average bfs distance from node_id to every other
    node in the community
    """

    dist = { node_id: 0 }
    queue = [ node_id ]
    while len(queue) > 0:
        u = queue.pop()
        children = []
        node = graph.GetNI(u)
        for i in range(node.GetOutDeg()):
            v = node.GetOutNId(i)
            if v in community and v not in dist:
                dist[v] = dist[u] + 1
                children.append(v)
        queue = children + queue
    
    d = 0.0
    for u in dist:
        d += dist[u]
    return d / len(dist)


def copy_dist(dist):
    return [ [ dist[i][j] for j in range(len(dist[i])) ] for i in range(len(dist)) ]

def floyd_warshall(graph, node_ids):
    inf = 2 * len(node_ids)
    id_to_index = {}
    for i in range(len(node_ids)):
        id_to_index[node_ids[i]] = i
        
    dist = [ [ inf for j in node_ids ] for i in node_ids ]

    edge = graph.BegEI()
    while edge < graph.EndEI():
        i_id = edge.GetSrcNId()
        j_id = edge.GetDstNId()
        if i_id in node_ids and j_id in node_ids:
            i = id_to_index[i_id]
            j = id_to_index[j_id]
            dist[i][j] = 1
            dist[j][i] = 1
        edge.Next()
        
    for i in range(len(node_ids)):
        dist[i][i] = 0

    for k in range(len(node_ids)):
        dist_prime = copy_dist(dist)
        for i in range(len(node_ids)):
            for j in range(len(node_ids)):
                dist_prime[i][j] = min(dist[i][k] + dist[k][j],  dist[i][j])
        dist = dist_prime

    average_distance = {}
    for i in range(len(node_ids)):
        total = 0.0
        for j in range(len(node_ids)):
            if i != j:
                total += dist[i][j]
        average_distance[node_ids[i]] = total / float(len(node_ids) - 1)
        
    return average_distance
    
class CompactCommunitySeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        self.mLexCount         = 10
        self.mMaxIterations    = -1
        self.mMaxCommunitySize = -1
        return

    def getLexCount(self):
        return self.mLexCount
    def getMaxIterations(self):
        return self.mMaxIterations
    def getMaxCommunitySize(self):
        return self.mMaxCommunitySize

    def setLexCount(self, v):
        self.mLexCount = v
        return
    def setMaxIterations(self, v):
        self.mMaxIterations = v
        return
    def setMaxCommunitySize(self, v):
        self.mMaxCommunitySize = v
        return

    def findCommunities(self, graph):
        self.mCommunities = compact_community.compact_community(graph, self.mLexCount, self.mMaxIterations, self.mMaxCommunitySize)
        self.mCommunityList = self.mCommunities.get_sets()
        self.mCommunityRoots = self.mCommunities.get_roots()
        self.mCommunityRoots.sort(key = lambda r: len(self.mCommunityList[r]), reverse=True)
        print "Number of communities: ", len(self.mCommunityRoots)
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids selected from graph
        """
        
        # make copy of graph, so original isn't messed up
        graph = copy_graph(graph)

        # do the community finding work
        self.findCommunities(graph)

        # do the specialized work to find seeds within the communities
        seeds = self.specialized_select_seeds(graph, k)
        
        # remove references to copy of graph
        graph = None
        
        return seeds

    def specialized_select_seeds(self, graph, k):
        raise NotImplementedError()
        return


class CompactCommunityDegreeSeedSelector(CompactCommunitySeedSelector):
    
    def __init__(self):
        CompactCommunitySeedSelector.__init__(self)
        return

    def specialized_select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids selected from graph
        """

        # communities have already been found.
        
        #
        # For each community, find the node with highest degree
        # and add it to the seeds.  Rotate through the communities
        # from largest to smallest, choosing a seed.  If necessary,
        # return to the front of the community list and keep choosing.
        #
        seeds = []
        i = 0
        while len(seeds) < k and len(seeds) < graph.GetNodes():
            r = self.mCommunityRoots[i%len(self.mCommunityRoots)]

            # find highest out degree of members in this community
            # randomize the list to get variety amongst ties
            max_degree = -1
            seed = -1
            random.shuffle(self.mCommunityList[r])
            for node_id in self.mCommunityList[r]:
                if node_id in seeds:
                    continue
                node = graph.GetNI(node_id)
                if node.GetOutDeg() > max_degree:
                    max_degree = node.GetOutDeg()
                    seed = node_id

            if seed > -1:
                seeds.append(seed)
                
            i += 1

        return seeds

class CompactCommunityDistanceSeedSelector(CompactCommunitySeedSelector):
    
    def __init__(self):
        CompactCommunitySeedSelector.__init__(self)
        return

    def specialized_select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids selected from graph
        """

        # communities have already been found.

        #
        # For each community, find the node with smallest average
        # distance to the rest of the community, and add it to
        # the seeds.
        #
        seeds = []
        i = 0
        average_distances = {}
        while len(seeds) < k and len(seeds) < graph.GetNodes():
            r = self.mCommunityRoots[i%len(self.mCommunityRoots)]

            # Find the average distances for this community, if not yet known
            added = False
            if len(self.mCommunityList[r]) > 1:
                if r not in average_distances:
                    average_distances[r] = floyd_warshall(graph, self.mCommunityList[r])
                    random.shuffle(self.mCommunityList[r])
                    potential_seeds = sorted(self.mCommunityList[r], key=lambda node_id: average_distances[r][node_id])
                    for node_id in potential_seeds:
                        if node_id not in seeds:
                            seeds.append(node_id)
                            added = True
                            break

            # don't allow a loop forever
            # if the first (and thus largest) community doesn't have a node to add, reduce our expectations by 1
            if (not added) and (i % len(self.mCommunityRoots) == 0):
                k -= 1
                
            i += 1

        return seeds
