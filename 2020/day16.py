import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
#from collections import defaultdict


def run(indata):
    L = indata.split('\n\n')
    
    R = L[0].splitlines()
    M = [int(m) for m in L[1].splitlines()[1].split(',')]
    N = [[int(m) for m in t.split(',')] for t in L[2].splitlines()[1:]]
    
    S = dict()
    for r in R:
        f = r.split(':')[0]
        V = [[int(v) for v in s.split('-')] for s in r.split(':')[1].split(' or ')]
        S[f] = V
        print((f, V))
    
    validtickets = []
    tser = 0
    for t in N:
        ticketvalid = True
        for v in t:
            valid = False
            for f in S:
                V = S[f]
                valid = (V[0][0] <= v and v <= V[0][1]) or (V[1][0] <= v and v <= V[1][1])
                if valid:
                    break
            if not valid:
                tser += v
                ticketvalid = False
        if ticketvalid:
            validtickets.append(t)
    
    answer = tser
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    fields = S.keys()
    C = np.ones((len(fields), len(fields)), dtype=int)
    
    for t in validtickets:
        for i, v in enumerate(t):
            for j, f in enumerate(fields):
                V = S[f]
                valid = (V[0][0] <= v and v <= V[0][1]) or (V[1][0] <= v and v <= V[1][1])
                if not valid:
                    C[i, j] = 0
    
    progress = True
    while progress:
        before_sum = np.sum(C)
        for i in range(len(fields)):
            if np.sum(C[i, :]) == 1:
                mask = -C[i, :]+1
                for k in range(len(fields)):
                    if k == i:
                        continue
                    C[k, :] *= mask
        progress = np.sum(C) < before_sum
    
    prd = 1
    for j, f in enumerate(fields):
        if f.startswith('departure'):
            idx = np.argmax(C[:, j])
            prd *= M[idx]
            print((idx,M[idx]))
    
    answer = prd
    # 1821618948371 too high
    # 998358379943
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=16, year=2020)
    run(indata)
