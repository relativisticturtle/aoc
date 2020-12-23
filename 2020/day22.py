import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from collections import deque




def run(indata):
    L = [[int(c) for c in l.splitlines()[1:]] for l in indata.split('\n\n')]
    
    d1 = deque(L[0])
    d2 = deque(L[1])
    
    while len(d1) > 0 and len(d2) > 0:
        c1 = d1.popleft()
        c2 = d2.popleft()
        
        if c1 > c2:
            d1.append(c1)
            d1.append(c2)
        elif c1 < c2:
            d2.append(c2)
            d2.append(c1)
        else:
            assert False
    
    d = d1 if len(d1) > 0 else d2
    w = 1
    count = 0
    while len(d) > 0:
        count += d.pop() * w
        w += 1
    
    answer = count
    
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    return
    # ----------- PART 2 -----------
    #
    
    # 273806840172142 too low
    answer = sum([eval2X(X)[0] for X in L])
    
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=22, year=2020)
    run(indata)
