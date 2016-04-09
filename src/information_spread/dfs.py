import snap

VISITED  = "visited"
PRENUM   = "pre-num"
POSTNUM  = "post-num"

g_visit_num = 0

def explore(graph, node):
    global g_visit_num
    graph.AddIntAttrDatN(node, 1, VISITED)
    g_visit_num += 1
    graph.AddIntAttrDatN(node, g_visit_num, PRENUM)

    for i in range(node.GetOutDeg()):
        out_id = node.GetOutNId(i)
        out_node = graph.GetNI(out_id)
        if graph.GetIntAttrDatN(out_node, VISITED) == 0:
            explore(graph, out_node)
    g_visit_num += 1
    graph.AddIntAttrDatN(node, g_visit_num, POSTNUM)
    return

def explore_iter(graph, node):
    global g_visit_num
    stack = [ node ]
    
    while len(stack) > 0:
        
        node = stack.pop()

        if graph.GetIntAttrDatN(node, VISITED) != 0:
            continue
        
        graph.AddIntAttrDatN(node, 1, VISITED)
        g_visit_num += 1
        #print "Visiting: ", node.GetId(), g_visit_num
        graph.AddIntAttrDatN(node, g_visit_num, PRENUM)
        
        for i in range(node.GetOutDeg()):
            out_id = node.GetOutNId(i)
            out_node = graph.GetNI(out_id)
            if graph.GetIntAttrDatN(out_node, VISITED) == 0:
                stack.append( out_node )

        # this is wrong.  Should not fire until after children are visited
        g_visit_num += 1
        graph.AddIntAttrDatN(node, g_visit_num, POSTNUM)
        #print "Visited ", node.GetId(), g_visit_num

    return

def dfs(graph):
    global g_visit_num
    g_visit_num = 0
    graph.AddIntAttrN(VISITED, 0)
    graph.AddIntAttrN(PRENUM, 0)
    graph.AddIntAttrN(POSTNUM, 0)
    node = graph.BegNI()
    while node < graph.EndNI():
        graph.AddIntAttrDatN(node, 0, VISITED)
        graph.AddIntAttrDatN(node, 0, PRENUM)
        graph.AddIntAttrDatN(node, 0, POSTNUM)
        node.Next()

    node = graph.BegNI()
    while node < graph.EndNI():
        if graph.GetIntAttrDatN(node, VISITED) == 0:
            a = g_visit_num
            explore_iter(graph, node)
            b = g_visit_num
            #print "visited ", b-a, " nodes"
        node.Next()
    return
