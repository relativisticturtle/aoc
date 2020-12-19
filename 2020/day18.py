import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
#from collections import defaultdict


def eval1(X):
    if X[0] == '(':
        return evalX(X[1:])
    else:
        return int(X[0]), X[1:]


def evalX(X):
    ans, X = eval1(X)
    
    while len(X) > 0:
        if X[0] == ')':
            return ans, X[1:]
        elif X[0] == '+':
            a, X = eval1(X[1:])
            ans += a
        elif X[0] == '*':
            a, X = eval1(X[1:])
            ans *= a
        else:
            print('')
            print('###')
            print(X)
            assert False
    return ans, X[1:]


def eval21(X):
    if X[0] == '(':
        return eval2X(X[1:])
    else:
        return int(X[0]), X[1:]


def eval2X(X):
    ans, X = eval21(X)
    
    P = [ans]
    
    while len(X) > 0:
        if X[0] == ')':
            return np.prod(P), X[1:]
        elif X[0] == '+':
            a, X = eval21(X[1:])
            P[-1] += a
        elif X[0] == '*':
            a, X = eval21(X[1:])
            P.append(a)
        else:
            print('')
            print('###')
            print(X)
            assert False
    return np.prod(P), []


def run(indata):
    L = [l.replace('(', '( ').replace(')', ' )').split(' ') for l in indata.splitlines()]
    
    # 43708644 too low
    answer = sum([evalX(X)[0] for X in L])
    
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))
    
    # ----------- PART 2 -----------
    #
    
    # 273806840172142 too low
    answer = sum([eval2X(X)[0] for X in L])
    
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=18, year=2020)
    run(indata)
