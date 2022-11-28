import os
import sys
import numpy as np
import itertools

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    L = sorted(L)
    G = dict()
    g = None
    asleep = None
    for l in L:
        date = l[1:11]
        if l[19:24] == 'Guard':
            g = int(l[26:].split()[0])
        elif l.endswith('falls asleep'):
            asleep = int(l[15:17])
        elif l.endswith('wakes up'):
            awoke = int(l[15:17])
            if g not in G:
                G[g] = np.zeros(60)
            G[g][asleep:awoke] += 1
            asleep = None

    max_sleep = 0
    max_g = None
    max_minute = None
    for g, sleepy in G.items():
        if np.sum(sleepy) > max_sleep:
            max_sleep = np.sum(sleepy)
            max_g = g
            max_minute = np.argmax(sleepy)
    answer = max_g * max_minute
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    max_sleep = 0
    max_g = None
    max_minute = None
    for g, sleepy in G.items():
        if np.max(sleepy) > max_sleep:
            max_sleep = np.max(sleepy)
            max_g = g
            max_minute = np.argmax(sleepy)
    answer = max_g * max_minute
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc_utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
