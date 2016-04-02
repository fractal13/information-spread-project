import snap
import random

def select_random_seeds(graph, k):
    """
    graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
    k is an integer, the desired number of seed nodes

    returns a Python set of node ids randomly selected from graph
    """

    all_node_ids = []
    node_ids = set()
    node = graph.BegNI()
    while node < graph.EndNI():
        all_node_ids.append(node.GetId())
        node.Next()

    if len(all_node_ids) < k:
        for nid in all_node_ids:
            node_ids.add(nid)
    else:
        while len(node_ids) < k:
            nid = random.choice(all_node_ids)
            node_ids.add(nid)
    
    return node_ids
    
