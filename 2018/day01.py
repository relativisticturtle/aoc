import os
import sys
import numpy as np

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    answer = np.sum([int(l) for l in L])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    f = 0
    idx = 0
    freq = set()
    while f not in freq:
        freq.add(f)
        f += int(L[idx])
        idx = (idx + 1) % len(L)
    answer = f
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc.utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
