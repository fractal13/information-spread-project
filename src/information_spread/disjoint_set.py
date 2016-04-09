#!/usr/bin/python

class DisjointSet:

    # for now, use associative arrays, hope for has implementation
    def __init__(self, do_compress=False):
        self.parent = {}
        self.rank = {}
        self.compress = do_compress
        return

    # create placeholders for node u
    def makeset(self, u):
        self.parent[u] = u
        self.rank[u] = 0
        return

    # move all children to point directly at root (shallow trees!)
    def find_compress(self, u):
        if u != self.parent[u]:
            self.parent[u] = self.find_compress(self.parent[u])
        return self.parent[u]

    # find the root of the tree
    def find(self, u):
        if self.compress:
            return self.find_compress(u)
        
        while u != self.parent[u]:
            u = self.parent[u]
        return u

    # to keep trees shallow, point shorter tree to taller tree's root
    def union(self, u, v):
        pu = self.find(u)
        pv = self.find(v)
        if pu == pv:
            return
        if self.rank[pu] > self.rank[pv]:
            self.parent[pv] = pu
        else:
            self.parent[pu] = pv
            if self.rank[pu] == self.rank[pv]:
                self.rank[pv] = self.rank[pv] + 1
        
        return

    def __str__(self):
        s = ''
        for u in self.parent.keys():
            s += "%s:%s:%d " % (u, self.parent[u], self.rank[u])
        return s

    def __repr__(self):
        return self.__str__()
    

def main():
    nodes = [ 'a', 'b', 'c', 'd', 'e', 'f' ]
    dj = DisjointSet()
    for n in nodes:
        dj.makeset(n)
    print dj
    for i in range(0, len(nodes), 2):
        dj.union(nodes[i], nodes[i+1])
    print dj
    return

if __name__ == "__main__":
    main()
    pass

    
