import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
#from collections import deque

def update_(M):
    newM = np.array(M)
    diff = 0
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            if M[r, c] == 0:
                continue
            n = np.sum(M[max(0, r-1):min(r+2, M.shape[0]), max(0, c-1):min(c+2, M.shape[1])] == 2)
            if M[r, c] == 1 and n == 0:
                newM[r, c] = 2
                diff += 1
            elif M[r, c] == 2 and n >= 5:
                newM[r, c] = 1
                diff += 1
    
    return newM, diff


def update2_(M):
    D = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    newM = np.array(M)
    diff = 0
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            if M[r, c] == 0:
                continue

            n = 0
            for d in D:
                for s in range(1, 100):
                    if r + s*d[0] < 0 or r + s*d[0] >= M.shape[0]:
                        break
                    if c + s*d[1] < 0 or c + s*d[1] >= M.shape[1]:
                        break
                    if M[r + s*d[0], c + s*d[1]] == 1:
                        break
                    if M[r + s*d[0], c + s*d[1]] == 2:
                        n += 1
                        break

            if M[r, c] == 1 and n == 0:
                newM[r, c] = 2
                diff += 1
            elif M[r, c] == 2 and n >= 5:
                newM[r, c] = 1
                diff += 1
    
    return newM, diff

def run(indata):
    L = indata.split('\n')
    
    M = np.array([[c == 'L' for c in l] for l in L[:-1]]).astype(int)

    diff = 1
    while diff > 0:
        M, diff = update_(M)
        #print(M)
        #print('Diff: %d' % diff)
    
    # 2588 too high
    answer = np.sum(M == 2)
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))

    # ----------- PART 2 -----------
    #
    M = np.array([[c == 'L' for c in l] for l in L[:-1]]).astype(int)

    diff = 1
    while diff > 0:
        M, diff = update2_(M)
        #print(M)
        print('Diff: %d' % diff)
    
    # 2414 too high
    answer = np.sum(M == 2)
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=11, year=2020)
    run(indata)

