class SeedSelector:

    def __init__(self):
        # empty
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids selected from graph according to an algorithm
        """
        raise NotImplementedError
        return set()

