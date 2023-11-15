import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np


def run(indata):
    L = indata.splitlines()

    A = dict()
    for l in L:
        m = l.split(' (contains ')
        for a in m[1][:-1].split(', '):
            i = m[0].split(' ')
            if not a in A:
                A[a] = set(i)
            else:
                A[a] = A[a].intersection(i)
    
    redux = True
    while redux:
        redux = False
        for a in A:
            if len(A[a]) == 1:
                Aa = next(iter(A[a]))
                for b in A:
                    if b != a and Aa in A[b]:
                        A[b].remove(Aa)
                        redux = True

    has_allergen = []
    for a in A:
        assert len(A[a]) == 1
        Aa = next(iter(A[a]))
        has_allergen.append(Aa)
        print('{}: {}'.format(a, A[a]))
    

    count = 0
    for l in L:
        m = l.split(' (contains ')
        for i in m[0].split(' '):
            if i not in has_allergen:
                count += 1

    answer = count
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = ','.join([next(iter(A[a])) for a in sorted(A.keys())])
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=21, year=2020)
    run(indata)
