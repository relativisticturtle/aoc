import os
import sys
import numpy as np

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    d = np.array([int(x) for x in L[0]])
    answer = np.sum(d[d == np.roll(d, 1)])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = np.sum(d[d == np.roll(d, int(len(d)/2))])
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
