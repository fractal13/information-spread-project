import seed_selector

class GreedySeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids greedily selected from graph
        """

        return self.select_greedy_seeds(graph, k)
        
    def select_greedy_seeds(self, graph, k):
        all_nodes = dict();
        node = graph.BegNI()
        node_ids = set()
        while node < graph.EndNI():
            all_nodes[node.GetId()] = node;
            node.Next()

        if len(all_nodes) < k:
            for nid in all_nodes:
                node_ids.add(nid)
        else:
            distance = dict();
            for node_id in all_nodes:
                distance[node_id]=self.getDist(all_nodes[node_id], graph);
            mdist = sorted(distance,key=distance.get)
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
                
    
