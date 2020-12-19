import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np


def run(indata):
    L = indata.splitlines()
    
    T = int(L[0])
    D = [int(l) for l in L[1].split(',') if l is not 'x']
    
    R = np.ceil(T / np.array(D)) * D - T
    b = np.argmin(R)
    
    answer = int(D[b] * R[b])
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    D = []
    for d, l in enumerate(L[1].split(',')):
        if l != 'x':
            D.append((d, int(l)))
    
    for i in range(len(D)):
        print('x = %2d (mod %3d)' % (-D[i][0] % D[i][1], D[i][1]))
    
    N = D[0][1]
    x = D[0][0]
    for d in D[1:]:
        for a in range(d[1]):
            if (x + a * N) % d[1] == -d[0] % d[1]:
                #print('(%d + %d * %d) %% %d == %d' % (x, a, N, d[1], -d[0] % d[1]))
                x += a * N
                N *= d[1]
                break
        #print(x)
    
    # 751731698158528 too low
    answer = x
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=13, year=2020)
    run(indata)
