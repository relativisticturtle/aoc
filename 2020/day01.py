import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

#import numpy as np
#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    items = [int(l) for l in L]
    
    # ----------- PART 1 -----------
    #
    answer = None
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i] + items[j] == 2020:
                answer = items[i] * items[j]
                break
        if answer:
            break
    
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = None
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            for k in range(j+1, len(items)):
                if items[i] + items[j] + items[k] == 2020:
                    answer = items[i] * items[j] * items[k]
                    break
            if answer:
                break
        if answer:
            break
    
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=1, year=2020)
    run(indata)

