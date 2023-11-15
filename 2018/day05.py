import os
import sys
import numpy as np

#from collections import deque

def reduce(P, ignore=''):
    i = 0
    while i < len(P):
        if i + 1 < len(P) and abs(ord(P[i]) - ord(P[i + 1])) == 32:
            del P[i:(i+2)]
        elif P[i] in ignore:
            del P[i]
        else:
            i += 1
    return len(P)


def run(indata):
    L = indata.splitlines(keepends=False)

    P = list(L[0])
    l1 = len(P)
    l2 = l1 + 1
    while l1 < l2:
        l2 = l1
        l1 = reduce(P)

    # ----------- PART 1 -----------
    #
    answer = l1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    best_len = l1
    for q in 'abcdefghijklmnopqrstuvwxyz':
        P2 = P[:]
        l1 = len(P2)
        l2 = l1 + 1
        while l1 < l2:
            l2 = l1
            l1 = reduce(P2, ignore=q + q.upper())
        best_len = min(best_len, l1)
    
    answer = best_len
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
