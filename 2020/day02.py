import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

#import numpy as np
#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    passwords = []
    for l in L:
        a = int(l.split('-')[0])
        b = int(l.split('-')[1].split(' ')[0])
        c = l.split(' ')[1].split(':')[0]
        d = l.split(':')[1].split(' ')[1]
        passwords.append([a, b, c, d])

    valid = 0
    for entry in passwords:
        c = entry[3].count(entry[2]) 
        if entry[0] <= c and c <= entry[1]:
            valid += 1

    print("Part 1: {}".format(valid))
    clipboard_set("{}".format(valid))

    # ----------- PART 2 -----------
    #
    valid = 0
    for entry in passwords:
        pos1 = entry[0]-1
        pos2 = entry[1]-1
        if (entry[3][pos1] == entry[2]) != (entry[3][pos2] == entry[2]):
            valid += 1
    print("Part 2: {}".format(valid))
    clipboard_set("{}".format(valid))


if __name__ == '__main__':
    indata = get_input(day=2, year=2020)
    run(indata)

