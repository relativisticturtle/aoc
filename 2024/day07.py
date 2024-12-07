import numpy as np
import aoc
import itertools


def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    # ----------- PART 1 -----------
    #
    answer = 0

    for l in L:
        R = int(l.split(':')[0])
        X = [int(x) for x in l.split()[1:]]

        for op in itertools.product('+*', repeat=len(X)-1):
            r = X[0]
            for p, x in zip(op, X[1:]):
                r = r + x if p == '+' else r * x
            if r == R:
                answer += R
                break

    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for l in L:
        R = int(l.split(':')[0])
        X = [int(x) for x in l.split()[1:]]

        for op in itertools.product('+*|', repeat=len(X)-1):
            r = X[0]
            for p, x in zip(op, X[1:]):
                if p == '|':
                    r = int(str(r) + str(x))
                else:
                    r = r + x if p == '+' else r * x
            if r == R:
                answer += R
                break
        #else:
        #    print(l)
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    #indata = get_input(test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))

