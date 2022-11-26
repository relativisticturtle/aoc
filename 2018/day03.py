import os
import sys
import numpy as np
import itertools

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    fabric = np.zeros((1000, 1000))
    for l in L:
        f = l.split()
        cid = int(f[0][1:])
        x = int(f[2].split(',')[0])
        y = int(f[2].split(',')[1][:-1])
        w = int(f[3].split('x')[0])
        h = int(f[3].split('x')[1])
        fabric[y:(y+h), x:(x+w)] += 1

    answer = np.sum(fabric > 1)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    for l in L:
        f = l.split()
        cid = int(f[0][1:])
        x = int(f[2].split(',')[0])
        y = int(f[2].split(',')[1][:-1])
        w = int(f[3].split('x')[0])
        h = int(f[3].split('x')[1])
        if np.all(fabric[y:(y+h), x:(x+w)] == 1):
            answer = cid
            break
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc_utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
