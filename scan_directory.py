import struct
import sys

dsk = file(sys.argv[1], "rb")
blocksize = 4096
block = 0

# see if this block could potentially be a directory
def isvalid(bytes):
    if len(bytes) < 8:
        print "error in block", block
        
    (inode, reclen, namelen, ftype) = struct.unpack("IHBB", bytes[0:8])

    if namelen != 1 or ftype != 2 or bytes[8] != '.':
        return False

    (inode, newreclen, namelen, ftype) = struct.unpack("IHBB", bytes[reclen:reclen+8])

    if namelen != 2 or ftype != 2 or bytes[reclen+8] != '.' or bytes[reclen+9] != '.':
        return False

    return True

# list some names in the given directory block
def names(bytes):
    ix = 0
    while ix < len(bytes):
        (inode, reclen, namelen, ftype) = struct.unpack("IHBB", bytes[ix:ix+8])
        name = bytes[ix+8:ix+8+namelen]
        yield name
        ix += reclen
    
while True:
    bytes = dsk.read(blocksize)

    if len(bytes) == 0: break

    if isvalid(bytes):
        print "block #", block
        print list(names(bytes))

    block += 1
