import os
import snap
import gzip
import glob
import utilities
import tarfile
#content = "Lots of content here"
#f = gzip.open('Onlyfinnaly.log.gz', 'wb')
#f.write(content)
#f.close()
#f=gzip.open('Onlyfinnaly.log.gz','rb')
#file_content=f.read()
#print file_content
#f.close();

def unzipTarGz(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
    elif (fname.endswith("tar")):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()
    

cdir = os.path.dirname(os.path.realpath(__file__))
if not glob.glob(cdir+"/facebook"): 
    sArrFiles = glob.glob(cdir+"/../networks/facebook/facebook.tar.gz")
    unzipTarGz(sArrFiles[0]);    


## generate a network using Forest Fire model
#G3 = snap.GenForestFire(1000, 0.35, 0.35)
## save and load binary
#FOut = snap.TFOut("test.graph")
#G3.Save(FOut)
#FOut.Flush()
#FIn = snap.TFIn("test.graph")
#G4 = snap.TNGraph.Load(FIn)
## save and load from a text file
#snap.SaveEdgeList(G4, "test.txt", "Save as tab-separated list of edges")
#G5 = snap.LoadEdgeList(snap.PNGraph, "test.txt", 0, 1)

## create a directed random graph on 10k nodes and 5k edges
#G6 = snap.GenRndGnm(snap.PNGraph, 10000, 5000)
## convert to undirected graph
#G7 = snap.ConvertGraph(snap.PUNGraph, G6)
## get largest weakly connected component
#WccG = snap.GetMxWcc(G6)
## generate a network using Forest Fire model
#G8 = snap.GenForestFire(1000, 0.35, 0.35)
## get a subgraph induced on nodes {0,1,2,3,4}
#SubG = snap.GetSubGraph(G8, snap.TIntV.GetV(0,1,2,3,4))
## get 3-core of G8
#Core3 = snap.GetKCore(G8, 3)
## delete nodes of out degree 3 and in degree 2
#snap.DelDegKNodes(G8, 3, 2)


import snap

Graph = snap.GenRndGnm(snap.PNGraph, 10, 20)
snap.DrawGViz(Graph, snap.gvlDot, "graph.png", "graph 1")

UGraph = snap.GenRndGnm(snap.PUNGraph, 10, 40)
snap.DrawGViz(UGraph, snap.gvlNeato, "graph_undirected.png", "graph 2", True)

NIdColorH = snap.TIntStrH()
NIdColorH[0] = "green"
NIdColorH[1] = "red"
NIdColorH[2] = "purple"
NIdColorH[3] = "blue"
NIdColorH[4] = "yellow"
Network = snap.GenRndGnm(snap.PNEANet, 5, 10)
snap.DrawGViz(Network, snap.gvlSfdp, "network.png", "graph 3", True, NIdColorH)