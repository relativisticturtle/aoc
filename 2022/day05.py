import os
import sys
import numpy as np
#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    crates = [l[1::4] for l in L[:8]]
    instr = [[int(x) for x in l.split()[1::2]] for l in L[10:]]

    
    C = [[c[i] for c in crates if c[i] != ' '][::-1] for i in range(9)]
    for i in instr:
        for _ in range(i[0]):
            C[i[2]-1].append(C[i[1]-1].pop())

    answer = ''.join([str(c[-1]) for c in C])

    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    C = [[c[i] for c in crates if c[i] != ' '][::-1] for i in range(9)]
    for i in instr:
        T = []
        for _ in range(i[0]):
            T.append(C[i[1]-1].pop())
        C[i[2]-1].extend(T[::-1])

    answer = ''.join([str(c[-1]) for c in C])
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
