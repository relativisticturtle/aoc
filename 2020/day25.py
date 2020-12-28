import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
from collections import deque


def run(indata):
    L = [int(l) for l in indata.splitlines()]

    v = 1
    s = 7
    M = 20201227
    for i in range(M):
        #v = (v * 7) % M
        v = pow(s, i, M)
        if v == L[0]:
            answer = pow(L[1], i, M)
            print('1: {} = 7**{} (mod {}) --> E = {}'.format(L[0], i, M, answer))
            break
        elif v == L[1]:
            answer = pow(L[0], i, M)
            print('2: {} = 7**{} (mod {}) --> E = {}'.format(L[1], i, M, answer))
            break
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    return
    # ----------- PART 2 -----------
    #
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=25, year=2020)
    run(indata)
