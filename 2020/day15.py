import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
#from collections import defaultdict


def run(indata):
    L = indata.splitlines()
    
    #L = ['0,3,6']
    
    S = dict()
    for i, s in enumerate(L[0].split(',')[:-1]):
        S[int(s)] = i
        print(i+1, s)
    
    i = len(L[0].split(',')) - 1
    s = int(L[0].split(',')[-1])
    while True:
        old_s = s
        if s in S:
            s = i - S[s]
        else:
            s = 0
        S[old_s] = i
        i += 1
        
        if i == 2020:
            answer1 = old_s
            print(i, old_s)
        elif i == 3e7:
            answer2 = old_s
            break
    answer = answer1
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = answer2
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=15, year=2020)
    run(indata)
