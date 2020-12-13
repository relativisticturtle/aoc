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
    return
    # ----------- PART 2 -----------
    #
    
    d = 0
    wp = [1, 10]
    p =[0, 0]
    for l in L:
        if l[0] == 'N':
            wp[0] += int(l[1:])
        elif l[0] == 'S':
            wp[0] -= int(l[1:])
        elif l[0] == 'E':
            wp[1] += int(l[1:])
        elif l[0] == 'W':
            wp[1] -= int(l[1:])
        elif l[0] == 'F':
            p[0] += wp[0] * int(l[1:])
            p[1] += wp[1] * int(l[1:])
        elif l[0] == 'L':
            for c in range(int(int(l[1:])/90)):
                wp_y = wp[1]
                wp[1] = -wp[0]
                wp[0] = wp_y
        elif l[0] == 'R':
            for c in range(int(int(l[1:])/90)):
                wp_y = wp[1]
                wp[1] = wp[0]
                wp[0] = -wp_y
    
    answer = abs(p[0]) + abs(p[1])
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=13, year=2020)
    run(indata)
