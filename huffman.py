import json
from heapq import heapify, heappop, heappush
from node import Node
    
def construct_huffman_tree(s: list):
    """Recursively transform list of symbol nodes into a huffman tree.

    Arguments:
    s   -- list of symbol nodes
    """
    n2,n1 = (heappop(s), heappop(s))
    heappush(s, Node(n1.freq + n2.freq, left=n2, right=n1))
    return construct_huffman_tree(s) if len(s) > 1 else s

def create_huffman_tree(symbols: dict):
    """Create node heap from symbols dict and pass them to constructor.

    Arguments:
    symbols -- a dictionary mapping symbols to occurance frequencies
    """
    s = [Node(freq,symbol=symbol) for symbol,freq in symbols.items()]
    heapify(s)
    tree = construct_huffman_tree(s)
    return heappop(s)

def get_tree_from_encoding(encoding: dict, code: int=0, nbits: int=0):
    """Re-constructs a huffman node tree from an encoding map.

    Arguments:
    encoding    -- a dictionary mapping symbols to binary codes and bit counts

    Keyword Arguments:
    code        -- the expected binary code of this node in the tree
    nbits       -- the number of bits in the code
    """
    for symbol, (_code, _nbits) in encoding.items():
        if (_nbits, _code) == (nbits, code):
            return Node(0, symbol=symbol)
    nbits += 1
    code = code << 1
    return Node(0,
        left=get_tree_from_encoding(encoding, code + 0, nbits),
        right=get_tree_from_encoding(encoding, code + 1, nbits)
    )

def codes_from_node(node, code=0, nbits=0):
    """Creates an encoding map from huffman tree.

    Arguments:
    node        -- a node of a huffman tree

    Keyword Arguments:
    code        -- the binary code of this node
    nbits       -- the number of bits in the code
    """
    if node.is_leaf():
        return { node.symbol: (code, nbits)}
    
    child_nbits = nbits + 1
    child_code_prefix = code << 1
    
    return {
        **codes_from_node(node.left, child_code_prefix, child_nbits),
        **codes_from_node(node.right, child_code_prefix + 1, child_nbits),
    }

def create_huffman_encoding(symbols: dict):
    """Creates a huffman encoding from a symbols dictionary.

    Arguments:
    symbols -- a dictionary mapping symbols to frequency
    """
    tree = create_huffman_tree(symbols)
    encodings = codes_from_node(tree)
    return (tree, encodings)
