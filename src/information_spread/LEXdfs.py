import snap
import random
from stack import Stack

VISITED  = "visited"
LEX      = "lex"

def LEXdfs(graph, start):
    """
    Does DFS search of graph, beginning at start.
    Implemented from Algorithm 1 in
    "Finding compact communities in large graphs"
    by Creusefond, Largillier and Peyronnet.
    http://dx.doi.org/10.1145/2808797.2808868 
    """

    #
    # Create and initialize VISITED and LEX for all nodes
    #
    graph.AddIntAttrN(VISITED, 0)
    graph.AddStrAttrN(LEX, "")
    
    node = graph.BegNI()
    while node < graph.EndNI():
        graph.AddIntAttrDatN(node, 0, VISITED)
        graph.AddStrAttrDatN(node, "0", LEX)
        node.Next()
    

    # initialize DFS variables
    stack = Stack()
    stack.append( start.GetId() )
    i = 1

    # do the search
    while len(stack) > 0:

        # print "stack:"
        # print node_list_to_str(graph, stack)
        # print
        # print
        
        # process top node
        # print
        # stack.print_all()
        # print
        node_id = stack.pop()
        node = graph.GetNI(node_id)
        graph.AddIntAttrDatN(node, i, VISITED)
        array = []
        
        # find unvisited neighbors of node
        for in_id in range(node.GetOutDeg()):
            out_id = node.GetOutNId(in_id)
            out_node = graph.GetNI(out_id)
            if graph.GetIntAttrDatN(out_node, VISITED) == 0:
                # will raise exception if out_node not there
                try:
                    # print "Trying to remove", node_to_str(graph, out_id)
                    stack.remove(out_id)
                    # print "Removed", node_to_str(graph, out_id)
                except ValueError as e:
                    # expected to occur
                    pass

                lex = str(i) + graph.GetStrAttrDatN(out_node, LEX)
                graph.AddStrAttrDatN(out_node, lex, LEX)
                array.append(out_id)

            # end of unvisited neighbor
        # end of neighbors

        # print "Not sure if this is correct.  Needs to randomize order for ties"
        # print "Before"
        # print node_list_to_str(graph, array)
        array.sort(key = lambda n_id: graph.GetStrAttrDatN(n_id, LEX))
        randomize_equal_neighbors(graph, array)
        # print "After"
        # print node_list_to_str(graph, array)
        # print
        # print
        stack.extend(array)
        i = i + 1
        # print "stack:"
        # print node_list_to_str(graph, stack)
        # print
        # print

    # end of stack processing
    
    return

def randomize_equal_neighbors(graph, array):
    i = 0
    j = 0
    while i < len(array):
        i1 = i
        v1 = graph.GetStrAttrDatN(array[i1], LEX)
        i2 = i+1
        while i2 < len(array) and v1 == graph.GetStrAttrDatN(array[i2], LEX):
            i2 += 1
            
        # i1 through i2-1 are the same, shuffle them
        if i2 - i1 > 1:
            replacement = array[i1:i2]
            random.shuffle(replacement)
            for j in range(i1, i2):
                array[j] = replacement[j-i1]
        # done with shuffling
        
        i = i2
    return
    
def node_list_to_str(graph, array):
    s = ""
    for node_id in array:
        if len(s):
            s += "\n"
        s += node_to_str(graph, node_id)
    return s

def node_to_str(graph, node_id):
    node = graph.GetNI(node_id)
    s = "%09d %1d %s" % (node.GetId(), graph.GetIntAttrDatN(node, VISITED), graph.GetStrAttrDatN(node, LEX))
    return s
    
    
    
    
