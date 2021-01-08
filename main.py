from bitstring import BitArray, BitStream
from codec import encode, decode

HEADER_PADDING_BITS = 3
HEADER_NUM_SYMBOLS_BITS = 128
ENCODING_SYMBOL_BITS = 8
ENCODING_NBITS_BITS = 8

def construct_file_header(encoding_nbits, cipher_nbits, num_symbols):
    """Create file header bits.

    Arguments:
    encoding_nbits  -- number of bits in the huffman encoding file section
    cipher_nbits    -- number of bits in the encoded message
    num_symbols     -- the number of symbols in the file

    File header:
    ################################################
    ## PADDING - 3 BITS ## NUM SYMBOLS - 128 BITS ##
    ################################################
    """
    b = BitArray()

    bit_len = (HEADER_PADDING_BITS + HEADER_NUM_SYMBOLS_BITS
        + encoding_nbits + cipher_nbits)

    padding = (8 - (bit_len % 8)) % 8
    padding_bits = BitArray(uint=padding, length=HEADER_PADDING_BITS)
    num_symbols_bits = BitArray(uint=num_symbols, length=HEADER_NUM_SYMBOLS_BITS)
    b.append(padding_bits)
    b.append(num_symbols_bits)

    return b

def construct_encoding_bits(encoding: dict):
    """Create huffman encoding file section.

    Arguments:
    encoding    -- the huffman encoding dict
    """
    encoding_bits = BitArray()
    for s,(code,nbits) in encoding.items():
        symbol_bits = BitArray(uint=ord(s), length=ENCODING_SYMBOL_BITS)
        code_length_bits = BitArray(uint=nbits, length=ENCODING_NBITS_BITS)
        code_bits = BitArray(uint=code, length=nbits)
        encoding_bits.append(symbol_bits)
        encoding_bits.append(code_length_bits)
        encoding_bits.append(code_bits)

    return encoding_bits

def construct_encoded_file(cipher_bits: BitArray, encoding: dict):
    """Construct our custom encoded file.

    Arguments:
    cipher_bits -- the encoded message
    encoding    -- the huffman encoding dict
    """
    encoding_bits = construct_encoding_bits(encoding)

    header_bits = construct_file_header(len(encoding_bits),
        len(cipher_bits), len(encoding) - 1)

    file_bits = BitArray()
    file_bits.append(header_bits)
    file_bits.append(encoding_bits)
    file_bits.append(cipher_bits)

    return file_bits

def parse_encoded_file(file_bits: BitArray):
    """Parse our custom encoded file into cipher bits and encoding.

    Arguments:
    file_bits   -- the file bits
    """
    bs = BitStream(file_bits)
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

if __name__ == "__main__":
    """Encode or decode a file using huffman's encoding algorithm.

    The file format is custom to this application,
    so use whatever extension you like.

    If encoding the program will read normal and write binary.
    If decoding the program will read binary and write normal.
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['encode', 'decode'])
    parser.add_argument('infile')
    parser.add_argument('outfile')
    args = parser.parse_args()

    if args.cmd == 'encode':
        with open(args.infile, 'r') as fin:
            msg = fin.read()
        cipher_bits, encoding = encode(msg)
        b = construct_encoded_file(cipher_bits, encoding)
        with open(args.outfile, 'w+b') as fout:
            b.tofile(fout)
    else:
        encoded_file_bits = BitArray(filename=args.infile)
        cipher_bits, encoding = parse_encoded_file(encoded_file_bits)
        msg = decode(cipher_bits, encoding)
        with open(args.outfile, 'w+') as fout:
            fout.write(msg)
     