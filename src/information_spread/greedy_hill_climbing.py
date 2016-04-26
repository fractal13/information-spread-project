import independent_cascade
import threading

class WorkData:

    def __init__(self, graph, A0, candidate_node_ids, spread_probability):
        self.mGraph = graph
        self.mA0 = A0
        self.mCandidateNodeIds = candidate_node_ids
        self.mSpreadProbability = spread_probability
        self.mLock = threading.Lock()
        self.mNodesNotDone = self.mCandidateNodeIds[:]
        self.mNodesDone = {}
        self.mBestNodeId = -1
        self.mBestSpreadCount = 0
        return

    def getBestNodeId(self):
        return self.mBestNodeId
        
    def getJob(self):
        node_id = -1
        self.mLock.acquire()
        try:
            if len(self.mNodesNotDone) > 0:
                node_id = self.mNodesNotDone.pop()
        finally:
            self.mLock.release()
        #print threading.currentThread().getName(), 'job:', node_id
        return node_id

    def jobDone(self, node_id, spread_count):
        #print threading.currentThread().getName(), 'job:', node_id, 'done'
        self.mLock.acquire()
        try:
            if spread_count > self.mBestSpreadCount:
                self.mBestSpreadCount = spread_count
                self.mBestNodeId = node_id
            self.mNodesDone[node_id] = True
        finally:
            self.mLock.release()
        return

    def runJob(self, node_id):
        A1 = self.mA0[:] + [ node_id ]
        # FIXME: For true greedy hill climbing best results, must repeat this
        #        many times and average
        final_active = independent_cascade.independent_cascade(self.mGraph, A1, self.mSpreadProbability)
        return len(final_active)

def worker(wd):
    done = False
    while not done:
        node_id = wd.getJob()
        if node_id >= 0:
            spread_count = wd.runJob(node_id)
            wd.jobDone(node_id, spread_count)
        else:
            done = True
    return
            

def greedy_hill_climing_choose_next_node_thread(graph, A0, candidate_node_ids, spread_probability):
    wd = WorkData(graph, A0, candidate_node_ids, spread_probability)
    for i in range(8):
        t = threading.Thread(target=worker, args=(wd,))
        t.start()
        
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    return


def greedy_hill_climbing_thread(graph, k, candidate_node_ids, spread_probability):
    candidate_node_ids = candidate_node_ids[:]
    A0 = []
    while len(A0) < k and len(candidate_node_ids) > 0:
        node_id = greedy_hill_climing_choose_next_node_thread(graph, A0, candidate_node_ids, spread_probability)
        if node_id >= 0:
            A0.append(node_id)
            candidate_node_ids.remove(node_id)
    return A0
        

def greedy_hill_climing_choose_next_node(graph, A0, candidate_node_ids, spread_probability):
    
    final_active = independent_cascade.independent_cascade(graph, A0, spread_probability)
    best_spread_count = len(final_active)
    best_node_id = -1
    
    for node_id in candidate_node_ids:
        
        A1 = A0[:] + [ node_id ]
        # FIXME: For true greedy hill climbing best results, must repeat this
        #        many times and average
        for i in range(1):
            final_active = independent_cascade.independent_cascade(graph, A1, spread_probability)
            if len(final_active) > best_spread_count:
                best_spread_count = len(final_active)
                best_node_id = node_id
    
    return best_node_id
        

def greedy_hill_climbing_non_thread(graph, k, candidate_node_ids, spread_probability): 
    candidate_node_ids = candidate_node_ids[:]
    A0 = []
    while len(A0) < k and len(candidate_node_ids) > 0:
        node_id = greedy_hill_climing_choose_next_node(graph, A0, candidate_node_ids, spread_probability)
        if node_id >= 0:
            A0.append(node_id)
            candidate_node_ids.remove(node_id)
    return A0

def greedy_hill_climbing(graph, k, candidate_node_ids, spread_probability):
    return greedy_hill_climbing_non_thread(graph, k, candidate_node_ids, spread_probability)
