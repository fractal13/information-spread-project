#!/usr/bin/env python

import sys
import snap

sys.path.append('../../src/information_spread')

import compact_community

def main():
    #roads = snap.LoadEdgeList(snap.PNGraph, "roadNet-TX.txt")
    roads = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
    roadnet = snap.ConvertGraph(snap.PNEANet, roads)

    clusters = compact_community.compact_community(roadnet, 5, 10)
    print clusters
    
    return

if __name__ == "__main__":
    main()


