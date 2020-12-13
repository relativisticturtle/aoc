import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
#from collections import deque

def run(indata):
    L = indata.split('\n\n')
    
    count = 0
    for l in L:
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c in l:
                count += 1

    answer = count
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))

    # ----------- PART 2 -----------
    #
    count = 0
    for l in L:
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if all([c in ans for ans in l.splitlines()]):
                count += 1

    answer = count
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=6, year=2020)
    run(indata)
