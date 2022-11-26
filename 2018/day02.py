import os
import sys
import numpy as np
import itertools

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    C2, C3 = 0, 0
    for l in L:
        val, count = np.unique(np.array(list(l)), return_counts=True)
        if 2 in count:
            C2 += 1
        if 3 in count:
            C3 += 1

    answer = C2 * C3
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    for l1, l2 in itertools.combinations(L, 2):
        diffpos = np.array(list(l1)) != np.array(list(l2))
        if np.sum(diffpos) == 1:
            answer = ''.join(np.array(list(l1))[diffpos == False])
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
