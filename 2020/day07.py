import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
from collections import defaultdict, deque


def has_shiny_gold(bagrules, col):
    for b in bagrules[col]:
        if b[0] < 1:
            continue
        if b[1] == 'shiny gold':
            return True
        elif has_shiny_gold(bagrules, b[1]):
            return True


def bags_in(bagrules, col):
    count = 0
    for b in bagrules[col]:
        count += b[0] * (1 + bags_in(bagrules, b[1]))
    return count


def run(indata):
    L = indata.splitlines()

    bagrules = defaultdict(list)
    for l in L:
        bagr = l.split(' bags contain ')
        bagrules[bagr[0]] = [(int(b.split(' ')[0].replace('no', '0')), ' '.join(b.split(' ')[1:-1])) for b in bagr[1].split(', ')]

    count = 0
    for col in bagrules.keys():
        if has_shiny_gold(bagrules, col):
            count += 1

    answer = count
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))

    # ----------- PART 2 -----------
    #
    answer = bags_in(bagrules, 'shiny gold')
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=7, year=2020)
    run(indata)
