from bitstring import BitStream, BitArray
from huffman import get_encoding, get_tree_from_encoding

HEADER_PADDING_BITS = 3
HEADER_NUM_SYMBOLS_BITS = 128
ENCODING_SYMBOL_BITS = 8
ENCODING_NBITS_BITS = 8

def create_encoding(msg: str):
    symbols = {}
    for c in msg:
        if c not in symbols:
            symbols[c] = 0
        symbols[c] += 1

    return get_encoding(symbols)

def encode_message(msg: str, encoding: dict):
    cb = BitArray()
    for i in range(len(msg)):
        x = msg[i]
        code, bits = encoding[msg[i]]
        encoded = BitArray(uint=code, length=bits)
        cb.append(encoded)
    
    return cb

def get_encoded_message_bits(cipher_bits: BitArray, encoding: dict):
    b = BitArray()

    # create header which is 3 bits padding specifier and symbol count
    padding_bits = BitArray(uint=0, length=HEADER_PADDING_BITS)
    num_symbols = len(encoding) - 1
    num_symbols_bits = BitArray(uint=num_symbols, length=HEADER_NUM_SYMBOLS_BITS)
    b.append(padding_bits)
    b.append(num_symbols_bits)

    # write encoding
    for s,(code,nbits) in encoding.items():
        symbol_bits = BitArray(uint=ord(s), length=ENCODING_SYMBOL_BITS)
        code_length_bits = BitArray(uint=nbits, length=ENCODING_NBITS_BITS)
        code_bits = BitArray(uint=code, length=nbits)
        b.append(symbol_bits)
        b.append(code_length_bits)
        b.append(code_bits)

    # write message
    b.append(cipher_bits)
    padding = (8 - (len(b) % 8)) % 8
    b.overwrite(BitArray(uint=padding, length=HEADER_PADDING_BITS), 0)
    return b

def process_encoded_message_bits(b: BitArray):
    bs = BitStream(b)
    padding = bs.read(f'uint:{HEADER_PADDING_BITS}')
    num_symbols = bs.read(f'uint:{HEADER_NUM_SYMBOLS_BITS}') + 1
    encoding = {}
    for i in range(num_symbols):
        s = chr(bs.read(f'uint:{ENCODING_SYMBOL_BITS}'))
        nbits = bs.read(f'uint:{ENCODING_NBITS_BITS}')
        code = bs.read(f'uint:{nbits}')
        encoding[s] = (code, nbits)
    
    cb = bs.read(f'bits:{len(bs)-bs.bitpos-padding}')
    return (cb, encoding)

def decode_message(cipher_bits: BitArray, tree: object):
    n = tree
    msg = ''
    for i in range(len(cipher_bits)):
        n = n.right if cipher_bits[i] else n.left
        if n.is_leaf():
            msg += n.x # add corresponding symbol to message string
            n = tree # reset current node to tree root
    
    return msg

def encode(msg: str):
    tree, encoding = create_encoding(msg)
    cypher_bits = encode_message(msg, encoding)
    msg = decode_message(cypher_bits, tree)
    b = get_encoded_message_bits(cypher_bits, encoding)
    return b

def decode(message_bits: BitArray):
    cipher_bits, encoding = process_encoded_message_bits(message_bits)
    tree = get_tree_from_encoding(encoding)
    msg = decode_message(cipher_bits, tree)
    return msg

# the main just runs a test cuz I'm lazy
if __name__ == '__main__':
    message_file = 'message.txt'

    with open(message_file, 'r', encoding='ascii') as fin:
        msg = fin.read()
    
    b = encode(msg)
    msg = decode(b)
    
    print(msg)
