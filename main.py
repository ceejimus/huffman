from bitstring import BitArray
from codec import encode, decode

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['encode', 'decode'])
    parser.add_argument('-f', '--file', action='store')
    parser.add_argument('-o', '--outfile', action='store')
    args = parser.parse_args()

    if args.cmd == 'encode':
        with open(args.file, 'r') as fin:
            msg = fin.read()
        b = encode(msg)
        with open(args.outfile, 'w+b') as fout:
            b.tofile(fout)
    else:
        b = BitArray(filename=args.file)
        msg = decode(b)
        with open(args.outfile, 'w+') as fout:
            fout.write(msg)
     