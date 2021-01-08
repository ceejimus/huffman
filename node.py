class Node():
    def __init__(self, freq, symbol=None, left=None, right=None):
        """Initializes the node.
        
        Arguments:
        freq    -- the expected freqency of occurence
        symbol  -- the symbol of the leaf node (None for branching nodes)
        left    -- the node obtained when branching left (None for leaf nodes)
        right   -- the node obtained when branching right (None for leaf nodes)
        """
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def is_leaf(self):
        """Return True if the node has a symbolue and is thus a leaf."""
        return self.symbol is not None
    
    def __lt__(self, other):
        """Compare node frequencies - lower frequencies have higher priority
        This is used internally by heapq when creating the huffman tree.
        """
        return self.freq < other.freq
