import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
from collections import deque


def run(indata):
    L = [' '.join([c for c in l]).replace('n ', 'n').replace('s ', 's').split(' ') for l in indata.splitlines()]

    D = {
        'e': (0, -1),
        'w': (0, 1),
        'se': (-1, 0),
        'sw': (-1, 1),
        'ne': (1, -1),
        'nw': (1, 0),
    }
    
    T = dict()
    for l in L:
        dy = sum([D[s][0] for s in l])
        dx = sum([D[s][1] for s in l])
        if (dy, dx) in T:
            T[(dy, dx)] = 1 - T[(dy, dx)]
        else:
            T[(dy, dx)] = 1


    count = 0
    for t in T:
        count += T[t]
    answer = count
    
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    for i in range(100):
        X = set()
        for t in T:
            X.add(t)
            for d in D:
                X.add((t[0] + D[d][0], t[1] + D[d][1]))
        
        T2 = dict()
        for t in X:
            count = 0
            for d in D:
                if (t[0] + D[d][0], t[1] + D[d][1]) in T:
                    count += T[(t[0] + D[d][0], t[1] + D[d][1])]

            if t in T and T[t] == 1 and count > 0 and count <= 2:
                T2[t] = 1
            elif (t not in T or T[t] == 0) and count == 2:
                T2[t] = 1
        T = T2

    count = 0
    for t in T:
        count += T[t]
    answer = count
    
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=24, year=2020)
    run(indata)
