#
# A "stack" with a fast remove method
#

# I know it's not a stack.  It's a container with fast
# append(x)
# extend([x1, x2,...])
# pop()
# remove(x)
# len()

class Node:

    def __init__(self, value=-1, up=None, down=None):
        self.value = value
        self.up = up
        self.down = down
        return

class Stack:

    def __init__(self):
        self.top = self.bottom = Node()
        self.nodes = {}
        return

    def extend(self, values):
        for v in values:
            self.push(v)
        return

    def append(self, v):
        self.push(v)
        return
        
    def push(self, v):
        # print "push", v
        node = Node(v, None, self.top)
        self.top.up = node
        self.top = node
        self.nodes[v] = node
        return

    def pop(self):
        if self.top.down != None:
            node = self.top
            # print "pop", node.value
            self.top = node.down
            self.top.up = None
            del self.nodes[node.value]
        else:
            # print "pop", None
            node = Node()
        return node.value

    def remove(self, v):
        if v not in self.nodes:
            return
            
        # print "remove", v
        
        node = self.nodes[v]
        
        down_node = node.down
        up_node = node.up
        if down_node != None:
            down_node.up = up_node
        if up_node != None:
            up_node.down = down_node
        else:
            self.top = down_node

        del self.nodes[v]
        # print "-------------"
        # self.print_all()
        # print "-------------"
        return

    def remove_linear(self, v):
        node = self.top
        while node.down != None:
            if node.value == v:
                down_node = node.down
                up_node = node.up
                if down_node != None:
                    down_node.up = up_node
                if up_node != None:
                    up_node.down = down_node
                return
            node = node.down
        return


    def print_all(self):
        node = self.top
        while node.down != None:
            print node.value, node.down, node.up
            node = node.down
        print node.value, node.down, node.up
        return

    def __len__(self):
        return len(self.nodes)



