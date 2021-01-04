import json
from heapq import heapify, heappop, heappush
from node import Node
    
def extend_tree(s: list):
    n2,n1 = (heappop(s), heappop(s))
    heappush(s, Node(n1.p + n2.p, left=n2, right=n1))
    return extend_tree(s) if len(s) > 1 else s

def get_huffman_tree(symbols: dict):
    s = [Node(p,x=x) for x,p in symbols.items()]
    heapify(s)
    tree = extend_tree(s)
    return heappop(s)

def add_node(encoding: dict, prefix: int, depth: int):
    symbols = list(encoding.keys())
    for s in symbols:
        (code, nbits) = encoding[s]
        if nbits == depth and code == prefix:
            return Node(0, x=s)
    left_node = add_node(encoding, (prefix << 1) + 0, depth+1)
    right_node = add_node(encoding, (prefix << 1) + 1, depth+1)
    return Node(0, left=left_node, right=right_node)

def get_tree_from_encoding(encoding: dict):
    return add_node(encoding, 0, 0)

def get_encoding_from_tree(tree, encodings=[], e=0, bits=1):
    l = tree.left
    r = tree.right

    _encodings = {}
    if l.is_leaf():
        _encodings[l.x] = ((e << 1) + 0, bits)
    else:
        _encodings = {**_encodings, **get_encoding_from_tree(l, encodings, (e << 1) + 0, bits + 1)}

    if r.is_leaf():
        _encodings[r.x] = ((e << 1) + 1, bits)
    else:
        _encodings = {**_encodings, **get_encoding_from_tree(r, encodings, (e << 1) + 1, bits + 1)}
    return _encodings

def get_encoding(symbols: dict):
    tree = get_huffman_tree(symbols)
    encodings = get_encoding_from_tree(tree, [])
    return (tree, encodings)
