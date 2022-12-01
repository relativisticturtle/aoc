import os
import sys
import numpy as np

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    snacks = list()
    c = 0
    for l in L:
        if l == '':
            snacks.append(c)
            c = 0
        else:
            c += int(l)
    answer = max(snacks)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    snacks = sorted(snacks, reverse=True)
    answer = sum(snacks[0:3])
    print("Part 2: {:d}".format(answer))
    

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
