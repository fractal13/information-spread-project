import seed_selector
import compact_community_seed
import random

class DistanceSeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids greedily selected from graph
        """

        return self.select_distance_seeds(graph, k)
        
    def select_distance_seeds(self, graph, k):
        all_nodes = dict();
        node = graph.BegNI()
        node_ids = set()
        while node < graph.EndNI():
            all_nodes[node.GetId()] = True;
            node.Next()

        if len(all_nodes) < k:
            for nid in all_nodes:
                node_ids.add(nid)
        else:
            distance = dict();
            for node_id in all_nodes:
                distance[node_id]=self.getDist(graph.GetNI(node_id), graph);
            mdist = sorted(distance,key=distance.get, reverse=True)
            for i in mdist[:k]:
                node_ids.add(i);
                
        return node_ids
    
    def getDist(self,node, graph):
        out = node.GetOutDeg();
        if(out==0):
            return 0;

        maxN = -1;
        for i in range(node.GetOutDeg()):
            n = graph.GetNI(node.GetOutNId(i))
            o = n.GetOutDeg();
            if o > maxN:
                m = n;
                maxN = o;
        return out+self.getDist(m, graph);
                
    
class FWDistanceSeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        self.mHaveAverageDistances = False
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids greedily selected from graph
        """

        return self.select_distance_seeds(graph, k)
        
    def select_distance_seeds(self, graph, k):

        if not self.mHaveAverageDistances:

            node = graph.BegNI()
            self.mNodeIds = []
            while node < graph.EndNI():
                self.mNodeIds.append(node.GetId())
                node.Next()
        
            self.mAverageDistances = compact_community_seed.floyd_warshall(graph, self.mNodeIds)
            self.mHaveAverageDistances = True
                
        random.shuffle(self.mNodeIds)
        potential_seeds = sorted(self.mNodeIds, key=lambda node_id: self.mAverageDistances[node_id])
        seeds = potential_seeds[:k]
        # for node_id in potential_seeds[:50]:
        #     print node_id, self.mAverageDistances[node_id]
            
        return seeds

class BFSDistanceSeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        self.mHaveAverageDistances = False
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids greedily selected from graph
        """

        return self.select_distance_seeds(graph, k)
        
    def select_distance_seeds(self, graph, k):

        if not self.mHaveAverageDistances:

            node = graph.BegNI()
            self.mNodeIds = []
            while node < graph.EndNI():
                self.mNodeIds.append(node.GetId())
                node.Next()

            self.mAverageDistances = compact_community_seed.average_bfs_distance_all(graph, self.mNodeIds)
            self.mHaveAverageDistances = True
            
        random.shuffle(self.mNodeIds)
        potential_seeds = sorted(self.mNodeIds, key=lambda node_id: self.mAverageDistances[node_id])
        seeds = potential_seeds[:k]
        # for node_id in potential_seeds[:50]:
        #     print node_id, self.mAverageDistances[node_id]
            
        return seeds
