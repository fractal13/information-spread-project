class SeedSelector:

    def __init__(self):
        self.mInternalTime = 0.0
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids selected from graph according to an algorithm
        """
        raise NotImplementedError
        return set()

    def get_internal_time(self):
        return self.mInternalTime

    def reset_internal_time(self):
        self.mInternalTime = 0.0
        return



