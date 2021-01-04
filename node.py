class Node():
    def __init__(self, p, x=None, left=None, right=None):
        self.p = p
        self.x = x
        self.left = left
        self.right = right
    
    def is_leaf(self):
        return self.x is not None
    
    # for popping of the heapq stack
    # lower frequency items have higher priority
    def __lt__(self, other):
        return self.p < other.p
