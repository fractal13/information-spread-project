import snap
import random, os, sys, time

import seed_selector
import compact_community

# lifted from stackoverflow
def copy_graph(graph):
    tmpfile = '.copy.bin'

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

class CompactCommunitySeedSelector(seed_selector.SeedSelector):

    def __init__(self):
        seed_selector.SeedSelector.__init__(self)
        return

    def select_seeds(self, graph, k):
        """
        graph is a snap.PNEANet network (directed edges, attributes allowed for edges and nodes)
        k is an integer, the desired number of seed nodes
        
        returns a Python set of node ids selected from graph
        """

        # make copy of graph, so original isn't messed up
        # sections = "copy-graph"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(1); print "SLEPT";
        graph = copy_graph(graph)
        # sections = "find-communities"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(1); print "SLEPT";
        
        # print "Finding communities"
        communities = compact_community.compact_community(graph, 10)
        # print "Found communities"
        # sections = "get-sets-roots"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(1); print "SLEPT";
        community_list = communities.get_sets()
        roots = communities.get_roots()
        roots.sort(key = lambda r: len(community_list[r]), reverse=True)

        # sections = "seed-choice-loop"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(1); print "SLEPT";
        seeds = []
        i = 0
        while len(seeds) < k and len(seeds) < graph.GetNodes():
            r = roots[i%len(roots)]
            max_degree = -1
            seed = -1
            random.shuffle(community_list[r])
            for node_id in community_list[r]:
                if node_id in seeds:
                    continue
                node = graph.GetNI(node_id)
                if node.GetOutDeg() > max_degree:
                    max_degree = node.GetOutDeg()
                    seed = node_id

            if seed > -1:
                seeds.append(seed)
                
            i += 1

        # remove references to copy of graph
        graph = None
        # sections = "seed-done"; print "SLEEPING", sections,; sys.stdout.flush(); time.sleep(3); print "SLEPT";
        return seeds

        
