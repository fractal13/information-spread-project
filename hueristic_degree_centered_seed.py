__author__ = 'Honey'

import snap
import seed_selector
class DegreeCenteredSeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes

        returns a Python set of node ids randomly selected from graph
        """

        return self.select_degree_centered_seed(graph, k)

    def select_degree_centered_seed(self, graph, k):
        degreeStorage = dict()
        all_node_ids = []
        node_ids = set()
        node = graph.BegNI()
        while node < graph.EndNI():
            all_node_ids.append(node.GetId())
            degreeStorage[node.GetId()]=node.GetOutDeg();
            node.Next()



        if len(all_node_ids) < k:
            for nid in all_node_ids:
                node_ids.add(nid)
        else:
            sorted_x =sorted(degreeStorage.items(), key=lambda x: x[1])
            sorted_x.reverse()
            for key in sorted_x:
                 node_ids.add(key)
        return node_ids

