import snap
import random, time

x = snap.TStr("a")
y = snap.TStr("b")
z = snap.TStr("")
print x
print y
print z
print x == "a"
print y == "b"
print z == ""


v = snap.TIntV()
for j in range(10):
    v.Add(random.randint(1, 1000))

print v.Len()
print v[v.Len()-1]


h = snap.TIntStrH()
for j in range(10):
    i = random.randint(1, 1000)
    h[i] = "--value--%d--%d--" % (j, i)
    
print h.Len()
for j in h:
    print "%d %s" % (j, h[j])


rand = snap.TRnd(int(time.time()))
for i in range(5):
    print rand.GetUniDev()


##########################################################
g = snap.TNGraph.New()
g.AddNode(1)
g.AddNode(2)
g.AddNode(3)
g.AddNode(4)
g.AddNode(5)
g.AddEdge(1, 2)
g.AddEdge(1, 3)
g.AddEdge(1, 5)
g.AddEdge(2, 1)
g.AddEdge(2, 4)
g.AddEdge(2, 5)
g.AddEdge(3, 1)
g.AddEdge(3, 2)
g.AddEdge(3, 4)
g.AddEdge(4, 1)
g.AddEdge(5, 1)

g.Dump()

for n in g.Nodes():
    print n.GetId()
print g.GetNodes()

for e in g.Edges():
    print e.GetId(), e.GetSrcNId(), e.GetDstNId()
print g.GetEdges()

###########################################################

fout = snap.TFOut("cgl_sample.graph")
g.Save(fout)
fout.Flush()

fin = snap.TFIn("cgl_sample.graph")
g2 = snap.TNGraph.Load(fin)
g2.Dump()

snap.SaveEdgeList(g2, "cgl_sample.txt", "This is comment text - don't put a newline.")

g3 = snap.LoadEdgeList(snap.PNGraph, "cgl_sample.txt")
g3.Dump()

