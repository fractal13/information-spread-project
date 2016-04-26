import snap
import random, os, sys, time, json, tempfile

import seed_selector
import compact_community
import greedy_hill_climbing

CHOOSE_RANDOM_COMMUNITY  = 1
CHOOSE_CYCLIC_COMMUNITY  = 2
CHOOSE_BIGGEST_COMMUNITY = 3

# lifted from stackoverflow
def copy_graph(graph):
    #tmpfile = '.copy.bin'
    (fd, tmpfile) = tempfile.mkstemp()
    os.close(fd)
    os.remove(tmpfile)

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

    in_community = set(community)
    in_dist = set([node_id])
    
    dist = { node_id: 0}
    size = len(community)
    # for n in community:
    #     dist[n] = size
    # dist[node_id] = 0

    processed = 0
    queue = [ node_id ]
    while len(queue) > 0:
        u = queue.pop()
        processed += 1
        children = []
        node = graph.GetNI(u)
        for i in range(node.GetOutDeg()):
            v = node.GetOutNId(i)
            #if v in community and dist[v] > dist[u] + 1:
            if v in in_community and v not in in_dist:
                dist[v] = dist[u] + 1
                children.append(v)
                in_dist.add(v)
        queue = children + queue
    
    d = 0.0 + (size-processed) * size
    for u in dist:
        d += dist[u]
    return d / size

def average_bfs_distance_all(graph, community):
    average_distances = {}
    for node_id in community:
        #print len(average_distances), node_id
        average_distances[node_id] = average_bfs_distance(graph, node_id, community)
    return average_distances

def copy_dist(dist):
    return [ [ dist[i][j] for j in range(len(dist[i])) ] for i in range(len(dist)) ]

def floyd_warshall(graph, node_ids):
    inf = 2 * len(node_ids)
    id_to_index = {}
    for i in range(len(node_ids)):
        id_to_index[node_ids[i]] = i
        
    dist = [ [ inf for j in node_ids ] for i in node_ids ]
    dist_prime = copy_dist(dist)

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
        print "FW: ", k
        #dist_prime = copy_dist(dist)
        for i in range(len(node_ids)):
            for j in range(len(node_ids)):
                dist_prime[i][j] = min(dist[i][k] + dist[k][j],  dist[i][j])
        #dist = dist_prime
        dist, dist_prime = dist_prime, dist

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
        self.mMaxIterations    = 1
        self.mMaxCommunitySize = 1
        self.mCommunityType    = compact_community.UNTIL_ITERATION
        self.mCommunityFile         = None
        self.mCommunityFileData     = None
        self.mCommunityFilePosition = 0
        self.mCommunityChoiceType   = CHOOSE_CYCLIC_COMMUNITY
        self.mSpreadProbability = 0.05
        self.initialize_cycle_community()
        return

    def getLexCount(self):
        return self.mLexCount
    def getMaxIterations(self):
        return self.mMaxIterations
    def getMaxCommunitySize(self):
        return self.mMaxCommunitySize
    def getCommunityType(self):
        return self.mCommunityType
    def getCommunityFile(self):
        return self.mCommunityFile
    def getCommunityChoiceType(self):
        return self.mCommunityChoiceType
    def getSpreadProbability(self):
        return self.mSpreadProbability

    def setLexCount(self, v):
        self.mLexCount = v
        return
    def setMaxIterations(self, v):
        self.mMaxIterations = v
        return
    def setMaxCommunitySize(self, v):
        self.mMaxCommunitySize = v
        return
    def setCommunityType(self, v):
        self.mCommunityType = v
        return
    def setCommunityFile(self, v):
        self.mCommunityFile = v
        return
    def setCommunityChoiceType(self, v):
        self.mCommunityChoiceType = v
        return
    def setSpreadProbability(self, v):
        self.mSpreadProbability = v
        return

    def findCommunities(self, graph):
        self.initialize_cycle_community()

        if self.mCommunityFile and (not self.mCommunityFileData) and os.path.exists(self.mCommunityFile):
            fin = open(self.mCommunityFile, "r")
            self.mCommunityFileData = json.load(fin)
            fin.close()
            self.mCommunityFilePosition = 0

        if self.mCommunityFileData and self.mCommunityFilePosition < len(self.mCommunityFileData['trials']):
            self.mCommunityList  = self.mCommunityFileData['trials'][self.mCommunityFilePosition]
            self.mCommunityRoots = self.mCommunityList.keys()
            self.mCommunityRoots.sort(key = lambda r: len(self.mCommunityList[r]), reverse=True)
            self.mCommunityFilePosition = (self.mCommunityFilePosition + 1) % len(self.mCommunityFileData['trials'])
            self.mInternalTime += self.mCommunityFileData['average-generation-time']

        else:
            
            if self.mCommunityType == compact_community.UNTIL_ITERATION:
                parameter = self.mMaxIterations
            elif self.mCommunityType == compact_community.UNTIL_MAXSIZE:
                parameter = self.mMaxCommunitySize
            elif self.mCommunityType == compact_community.LIMIT_CLUSTER_SIZE:
                parameter = self.mMaxCommunitySize
            else:
                raise Exception("Bad community type")
            
            self.mCommunities = compact_community.compact_community(graph, self.mLexCount, self.mCommunityType, parameter)
            self.mCommunityList = self.mCommunities.get_sets()
            self.mCommunityRoots = self.mCommunities.get_roots()
            self.mCommunityRoots.sort(key = lambda r: len(self.mCommunityList[r]), reverse=True)
            # print "Number of communities: ", len(self.mCommunityRoots)
            # print "Sizes:",
            # for r in self.mCommunityRoots:
            #     print self.mCommunities.get_set_size(r),
            #     print
                
        return

    def choose_community(self):
        if self.mCommunityChoiceType == CHOOSE_RANDOM_COMMUNITY:
            return self.choose_random_community()
        elif self.mCommunityChoiceType == CHOOSE_CYCLIC_COMMUNITY:
            return self.choose_next_cycle_community()
        elif self.mCommunityChoiceType == CHOOSE_BIGGEST_COMMUNITY:
            return self.choose_current_cycle_community()
        else:
            raise Exception("Bad community choice type")
            return 0

    def bad_community_choice(self):
        if self.mCommunityChoiceType == CHOOSE_RANDOM_COMMUNITY:
            pass
        elif self.mCommunityChoiceType == CHOOSE_CYCLIC_COMMUNITY:
            pass
        elif self.mCommunityChoiceType == CHOOSE_BIGGEST_COMMUNITY:
            self.advance_next_cycle_community()
        else:
            raise Exception("Bad community choice type")
        return
        
    def choose_random_community(self):
        return random.choice(self.mCommunityRoots)

    def initialize_cycle_community(self):
        self.mCommunityCounter = 0
        return
    def advance_next_cycle_community(self):
        self.mCommunityCounter += 1
        self.mCommunityCounter %= len(self.mCommunityRoots)
        return
    def choose_next_cycle_community(self):
        r = self.mCommunityRoots[self.mCommunityCounter]
        self.advance_next_cycle_community()
        return r
    def choose_current_cycle_community(self):
        r = self.mCommunityRoots[self.mCommunityCounter]
        return r

        

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
        while len(seeds) < k and len(seeds) < graph.GetNodes():
            r = self.choose_community()

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
            else:
                self.bad_community_choice()

            # end while loop

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
        failed = 0
        seeds = []
        average_distances = {}
        while len(seeds) < k and len(seeds) < graph.GetNodes():
            r = self.choose_community()

            # Find the average distances for this community, if not yet known
            added = False
            if len(self.mCommunityList[r]) > 1:
                if r not in average_distances:
                    #average_distances[r] = floyd_warshall(graph, self.mCommunityList[r])
                    average_distances[r] = average_bfs_distance_all(graph, self.mCommunityList[r])
                random.shuffle(self.mCommunityList[r])
                potential_seeds = sorted(self.mCommunityList[r], key=lambda node_id: average_distances[r][node_id])
                for node_id in potential_seeds:
                    if node_id not in seeds:
                        seeds.append(node_id)
                        added = True
                        break

            # don't allow a loop forever
            # if the first (and thus largest) community doesn't have a node to add, reduce our expectations by 1
            if not added:
                self.bad_community_choice()
                failed += 1
                if failed % len(self.mCommunityRoots) == 0:
                    k -= 1
                
            # end while loop

        return seeds

class CompactCommunityGreedyHillClimbingSeedSelector(CompactCommunitySeedSelector):
    
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

        # for each community, find the best node to add based on greedy hill climbing
        failed = 0
        seeds = []
        while len(seeds) < k and len(seeds) < graph.GetNodes():
            r = self.choose_community()

            # Find the average distances for this community, if not yet known
            added = False
            node_id = greedy_hill_climbing.greedy_hill_climing_choose_next_node(graph, seeds, self.mCommunityList[r], self.mSpreadProbability)
            if node_id >= 0:
                seeds.append(node_id)
                added = True

            # don't allow a loop forever
            # if the first (and thus largest) community doesn't have a node to add, reduce our expectations by 1
            if not added:
                self.bad_community_choice()
                failed += 1
                if failed % len(self.mCommunityRoots) == 0:
                    k -= 1
                
            # end while loop

        return seeds
