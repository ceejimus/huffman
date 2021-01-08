from bitstring import BitArray
from huffman import create_huffman_encoding, get_tree_from_encoding

def create_symbols_map(msg: str):
    """Create a map of symbols to counts.

    Arguments:
    msg -- message string
    """
    symbols = {}
    for c in msg:
        if c not in symbols:
            symbols[c] = 0
        symbols[c] += 1

    return symbols

def encode_message(msg: str, encoding: dict):
    """Encode message string using encoding map and returns bits.

    Arguments:
    msg         -- message string
    encoding    -- mapping of symbols to codes
    """
    cb = BitArray()
    for s in msg:
        code, bits = encoding[s]
        cb.append(BitArray(uint=code, length=bits))
    
    return cb

def decode_message(cipher_bits: BitArray, tree: object):
    """Decode cipher bits using huffman tree and returns decoded message.

    This function simply traverses the tree for each bit of the cipher,
    adding characters to the message and resetting the tree to the root node
    when it finds a leaf.
    
    0 (False) -> go left, 1 (True) -> go right

    Arguments:
    cipher_bits -- bits of the encoded message
    tree        -- root node of the huffman tree
    """
    n = tree
    msg = ''
    for i in range(len(cipher_bits)):
        n = n.right if cipher_bits[i] else n.left
        if n.is_leaf():
            msg += n.symbol
            n = tree
    
    return msg

def encode(msg: str):
    """Encode a message using optimal huffman encoding.

    Arguments:
    msg         -- message string
    """
    symbols = create_symbols_map(msg)
    tree, encoding = create_huffman_encoding(symbols)
    cypher_bits = encode_message(msg, encoding)
    return cypher_bits, encoding

def decode(cipher_bits: BitArray, encoding: dict):
    """Decode huffman encoded cipher bits

    Arguments:
    cipher_bits -- bits of encoded message
    encoding    -- mapping of symbols to codes
    """
    tree = get_tree_from_encoding(encoding)
    msg = decode_message(cipher_bits, tree)
    return msg
