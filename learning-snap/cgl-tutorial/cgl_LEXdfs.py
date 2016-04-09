#!/usr/bin/env python

import sys
import snap

sys.path.append('../../src/information_spread')

import LEXdfs

def main():
    roads = snap.LoadEdgeList(snap.PNGraph, "roadNet-TX.txt")
    #roads = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
    roadnet = snap.ConvertGraph(snap.PNEANet, roads)
    print roadnet
    LEXdfs.LEXdfs(roadnet, roadnet.BegNI())
    
    return

if __name__ == "__main__":
    main()


