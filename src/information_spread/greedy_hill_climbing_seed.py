import snap
import random

import seed_selector, greedy_hill_climbing

class GreedyHillClimbingSeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        self.mSpreadProbability = 0.05
        return

    def getSpreadProbability(self):
        return self.mSpreadProbability

    def setSpreadProbability(self, v):
        self.mSpreadProbability = v
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids using the greedy hill climbing algorithm
        """

        return self.select_greedy_hill_climbing_seeds(graph, k)
        
    def select_greedy_hill_climbing_seeds(self, graph, k):

        all_node_ids = []
        node_ids = set()
        node = graph.BegNI()
        while node < graph.EndNI():
            all_node_ids.append(node.GetId())
            node.Next()
        
        if len(all_node_ids) <= k:
            for nid in all_node_ids:
                node_ids.add(nid)
        else:
            node_id_list = greedy_hill_climbing.greedy_hill_climbing(graph, k, all_node_ids, self.mSpreadProbability)
            for nid in node_id_list:
                node_ids.add(nid)
    
        return node_ids
    
