import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from collections import deque
import itertools


def exp_rules(R):
    for r in range(len(R)):
        if all([all([isinstance(y, str) for y in x]) and not isinstance(x, str) for x in R[r]]):
            R[r] = list(np.unique(list(itertools.chain(*R[r]))))
            print('#R[{}] = {}'.format(r, R[r]))
        # rule finished if "flat"
        if all([isinstance(x, str) for x in R[r]]):
            #print('R[{}] = {}'.format(r, R[r]))
            continue
        
        #W = []
        #F = True
        for i in range(len(R[r])):
            if not all([x in R for x in R[r][i]]):
                F = False
                continue
            
            # can make R[str(r)][i] list of str?
            if not all([all([isinstance(y, str) for y in R[x]]) for x in R[r][i]]):
                F = False
                continue
            
            w = [''.join(p) for p in itertools.product(*[R[x] for x in R[r][i]])]
            w = list(np.unique(w))
            R[r][i] = w
            #W.extend(w)
            print('*R[{}][{}] = {}'.format(r, i, R[r][i]))
        #if F:
        #    R[r] = list(np.unique(W))
        #    print('+R[{}] = {}'.format(r, R[r]))
    return R


def match2rule(r, R, S):
    print('{}: {}'.format(r, S))
    M = []
    
    for x in R[r]:
        if isinstance(x, str):
            if S.startswith(x):
                M.append(S[len(x):])
                print(' ^R[{}]: {}|{}'.format(r, x,  S[len(x):]))
            continue
            
        Q = deque()
        Q.append((0, S))
        while len(Q) > 0:
            y, s = Q.popleft()
            
            for q in R[r][y]:
                Z = match2rule(q, R, s)
                print(' +R[{}]: *|{}'.format(q, Z))
                if y+1 == len(R[r]):
                    M.extend(Z)
                    print(' _R[{}][{}]: *|{}'.format(r, y, Z))
                    continue
                for z in Z:
                    Q.append((y+1, z))
                    print(' -R[{}][{}]: *|{}'.format(r, y, z))
    return M

def run(indata):
    L = [l.splitlines() for l in indata.split('\n\n')]
    
    R = dict()
    for r in L[0]:
        R[int(r.split(':')[0])] = [s[1:-1] if s.startswith('"') else [int(z) for z in s.split(' ')] for s in r.split(': ')[1].split(' | ')]
    
    for r in range(len(R)):
        print('{}: {}'.format(r, R[r]))
    
    for I in range(14):
        print('----------------------')
        R = exp_rules(R)
    
    print('======================')
    for r in range(len(R)):
        print('{}: {}'.format(r, R[r]))
    print('======================')
    
    count = 0
    for l in L[1]:
        M = match2rule(0, R, l)
        print(l)
        print(M)
        if '' in M:
            count += 1
        break
    
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
    indata = get_input(day=19, year=2020)
    run(indata)
