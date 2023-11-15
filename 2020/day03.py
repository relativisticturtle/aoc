import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)

    trees = np.array([[c == '#' for c in l] for l in L])

    count = 0
    for r in range(trees.shape[0]):
        if trees[r][3*r % trees.shape[1]]:
            count += 1

    print("Part 1: {}".format(count))
    clipboard_set("{}".format(count))

    # ----------- PART 2 -----------
    #
    counts = []
    for d in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        count = 0
        for s in range(0, int(trees.shape[0]/d[1])):
            if trees[d[1]*s][d[0]*s % trees.shape[1]]:
                count += 1
        print('{}: {}'.format(d, count))
        counts.append(count)

    answer = np.prod(np.array(counts, dtype='uint64'))
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=3, year=2020)
    run(indata)

