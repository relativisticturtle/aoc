import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
from collections import deque


def run(indata):
    L = [int(c) for c in indata.splitlines()[0]]
    
    S = deque(L)

    for i in range(100):
        # Take current
        current = S.popleft()

        #print('({}) {}'.format(current, list(S)))

        # Take 3
        picked = [S.popleft() for j in range(3)]

        # Find target label
        target = current
        while target not in S:
            target = target - 1 if target > 1 else max(L)

        # Make new stack
        Q = deque()
        q = 0
        while len(S) > 0:
            q = S.popleft()
            Q.append(q)
            if q == target:
                for p in picked:
                    Q.append(p)
        Q.append(current)
        S = Q
    
    Q = S
    while True:
        q = Q.popleft()
        if q == 1:
            break
        Q.append(q)
    
    answer = ''.join(['%d' % q for q in Q])
    
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    
    max_card = 1000000
    K = L[:]
    for i in range(len(K)+1, max_card+1):
        K.append(i)
    S = dict()
    S[K[-1]] = K[0]
    for i in range(1, len(K)):
        S[K[i-1]] = K[i]

    next_c = L[0]
    for i in range(10000000):
        current_c = next_c
        p1 = S[current_c]
        p2 = S[p1]
        p3 = S[p2]
        next_c = S[p3]

        # X = [next_c]
        # while X[-1] != current_c:
        #     X.append(S[X[-1]])
        # print('({}) [{}, {}, {}] {}'.format(current_c, p1, p2, p3, X[:-1]))

        target = current_c
        while target in [current_c, p1, p2, p3]:
            target = target - 1 if target > 1 else max_card
        
        S[p3] = S[target]
        S[target] = p1
        S[current_c] = next_c
    
    p1 = S[1]
    p2 = S[p1]
    answer = p1 * p2
    
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=23, year=2020)
    #run('389125467')
    run(indata)
