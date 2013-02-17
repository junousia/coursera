import os
from glob import glob
from Crypto.Hash import SHA256

def read_to_chunks(file, chunk_size=1024):
    size = os.fstat(file.fileno()).st_size
    pos = size%chunk_size
    for read_pos in range(pos, size+1, chunk_size):
        file.seek(-read_pos, os.SEEK_END)
        yield bytearray(file.read(chunk_size))

def hash_file(file):
    print "Hashing file {file}...".format(file=file)
    f = open(file)
    previous_hash = bytearray()
    for chunk in read_to_chunks(f):
        sha = SHA256.new()
        sha.update(chunk + previous_hash)
        previous_hash = sha.digest()
    return ''.join('%02x' % ord(byte) for byte in previous_hash)

def main():
    for fname in glob('*.mp4'):
        print hash_file(fname)

if __name__ == '__main__':
    main()

