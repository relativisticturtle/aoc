import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
from collections import defaultdict, deque


def run_modified_code(L, q):
    visited = set()
    count = 0
    p = 0
    while p < len(L):
        if p in visited:
            return None
        visited.add(p)
        
        i = L[p].split(' ')
        
        if i[0] == 'acc':
            count += int(i[1])
        elif (i[0] == 'jmp' and p != q):
            p += int(i[1])
            continue
        elif (i[0] == 'nop' and p == q):
            p += int(i[1])
            continue
        p += 1
    return count


def run(indata):
    L = indata.splitlines()

    visited = set()
    count = 0
    p = 0
    while True:
        if p in visited:
            break
        visited.add(p)
        
        i = L[p].split(' ')
        
        if i[0] == 'acc':
            count += int(i[1])
        elif i[0] == 'jmp':
            p += int(i[1])
            continue
        p += 1

    answer = count
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))

    # ----------- PART 2 -----------
    #
    answer = 0
    for p in range(len(L)):
        if L[p].split(' ')[0] == 'acc':
            continue
        answer = run_modified_code(L, p)
        if answer is not None:
            break
    
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=8, year=2020)
    run(indata)
