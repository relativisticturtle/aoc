import os
import sys
import numpy as np
from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)

    M = {l.split(':')[0]: l.split(': ')[1] for l in L}
    

    # ----------- PART 1 -----------
    #
    X = dict()
    def calc(monkey):
        if monkey in X:
            return X[monkey]
        expr = M[monkey].split()
        if len(expr) == 1:
            result = int(expr[0])
        elif expr[1] == '+':
            result = calc(expr[0]) + calc(expr[2])
        elif expr[1] == '-':
            result = calc(expr[0]) - calc(expr[2])
        elif expr[1] == '*':
            result = calc(expr[0]) * calc(expr[2])
        elif expr[1] == '/':
            assert calc(expr[0]) % calc(expr[2]) == 0

            result = calc(expr[0]) // calc(expr[2])
        X[monkey] = result
        return result

    answer = calc('root')
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    monkey = 'humn'
    deps = ['humn']
    while monkey != 'root':
        monkeys = [x for x, y in M.items() if monkey in y]
        if len(monkeys) > 2:
            break
        monkey = monkeys[0]
        deps.append(monkey)

    def deduce(monkey, should_value):
        if monkey not in deps:
            return X[monkey]
        
        expr = M[monkey].split()
        if len(expr) == 1:
            raise StopIteration((monkey, should_value))

        elif expr[1] == '+':
            if expr[0] in deps:
                deduce(expr[0], should_value - X[expr[2]])
            elif expr[2] in deps:
                deduce(expr[2], should_value - X[expr[0]])
            else:
                assert False
        elif expr[1] == '-':
            if expr[0] in deps:
                deduce(expr[0], should_value + X[expr[2]])
            elif expr[2] in deps:
                deduce(expr[2], X[expr[0]] - should_value)
            else:
                assert False
        elif expr[1] == '*':
            if expr[0] in deps:
                assert should_value % X[expr[2]] == 0
                deduce(expr[0], should_value // X[expr[2]])
            elif expr[2] in deps:
                assert should_value % X[expr[0]] == 0
                deduce(expr[2], should_value // X[expr[0]])
            else:
                assert False
        elif expr[1] == '/':
            if expr[0] in deps:
                deduce(expr[0], should_value * X[expr[2]])
            elif expr[2] in deps:
                assert X[expr[0]] % should_value == 0
                deduce(expr[2], X[expr[0]] // should_value)
            else:
                assert False

    M['root'] = ' - '.join(M['root'].split()[::2])
    try:
        deduce('root', 0)
    except StopIteration as e:
        if e.value[0] == 'humn':
            answer = e.value[1]
        else:
            answer = None

    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc.utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
