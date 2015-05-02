#!/usr/bin/env python

import os
import stat
import sys

infiles = []

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg == '-':
            infiles.append(os.fdopen(sys.stdin.fileno(), 0))
        else:
            infiles.append(open(arg, 'rb', 0))
else:
    infiles.append(os.fdopen(sys.stdin.fileno(), 0))

totalsize = 0

size_known = True

for f in infiles:
    try:
        st = os.fstat(f.fileno())
        if stat.S_ISREG(st.st_mode):
            totalsize += st.st_size
        else:
            size_known = False
            break
    except:
        size_known = False
        break

def convert_percent(part, total):
    if 0 < part < total:
        result = part * 100.0 / total
        return max(min(result, 99.99), 0.01)
    elif part == total:
        return 100.0
    else:
        return part * 100.0 / total

read_size = 0

while infiles:
    if size_known:
        sys.stderr.write("\r%s/%s bytes (%.2f%%)" % (read_size, totalsize, convert_percent(read_size, totalsize)))
    else:
        sys.stderr.write("\r%s bytes" % read_size)

    buf = infiles[0].read(8192)
    if buf:
        read_size += len(buf)
        sys.stdout.write(buf)
    else:
        infiles.pop(0).close()

sys.stderr.write("\n")

