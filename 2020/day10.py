import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np


C = dict()
def count_combinations(adapters):
    if len(adapters) == 1:
        return 1
    if tuple(adapters) in C:
        return C[tuple(adapters)]
    
    count = 0
    for i in range(min(3, len(adapters) - 1)):
        if adapters[i+1] - adapters[0] <= 3:
            count += count_combinations(adapters[i+1:])
        else:
            break
    
    C[tuple(adapters)] = count
    return count

def run(indata):
    L = indata.splitlines()
    adapters = np.sort([0] + [int(l) for l in L])
    
    d1 = 0
    d3 = 1
    for a in range(len(adapters) - 1):
        if adapters[a+1] - adapters[a] == 1:
            d1 += 1
        if adapters[a+1] - adapters[a] == 3:
            d3 += 1
    print((d1, d3))
    answer = d1 * d3
    
    # 1953 too low
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    

    # ----------- PART 2 -----------
    #
    answer = count_combinations(adapters)
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=10, year=2020)
    run(indata)
