import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
from collections import defaultdict, deque


def run(indata):
    L = indata.splitlines()
    code = [int(l) for l in L]
    
    answer = None
    for i in range(25, len(code)):
        valid = False
        for j in range(i-25, i-1):
            for k in range(j+1, i):
                if code[i] == code[j] + code[k]:
                    valid = True
                    break
            if valid:
                break
        if not valid:
            answer = code[i]
            break

    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))


    # ----------- PART 2 -----------
    #
    A = answer
    answer = None
    
    code = [0] + code
    
    C = np.cumsum(code)
    for i in range(len(C)-2):
        for j in range(i+2, len(C)):
            if C[j] - C[i] == A:
                L = code[(i+1):(j+1)]
                answer = np.max(L) + np.min(L)
                break
        if answer is not None:
            break
    # 41384461 too high
    # 36816557 too low
    print(np.sum(L))
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=9, year=2020)
    run(indata)
