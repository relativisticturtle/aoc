import os
import sys
import numpy as np


def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return p2 - p1
    elif isinstance(p1, list) and isinstance(p2, int):
        p2 = [p2]
    elif isinstance(p1, int) and isinstance(p2, list):
        p1 = [p1]
    
    for i in range(max(len(p1), len(p2))):
        if i < len(p1) and i < len(p2):
            c = compare(p1[i], p2[i]) 
            if c != 0:
                return c
        elif i < len(p2):
            return 1
        elif i < len(p1):
            return -1
    return 0


def run(indata):
    #L = indata.splitlines(keepends=False)
    D = [l.splitlines(keepends=False) for l in indata.split('\n\n')]
    
    # ----------- PART 1 -----------
    #
    answer = 0
    for i, p in enumerate(D):
        p0 = eval(p[0])
        p1 = eval(p[1])
        if compare(p0, p1) > 0:
            answer += (i + 1)
        #print(i, compare(p0, p1))

    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    E = []
    D.append(['[[2]]', '[[6]]'])
    for d in D:
        E.extend([eval(p) for p in d])

    import functools

    E = sorted(E, key=functools.cmp_to_key(compare), reverse=True)
    idx1 = np.argmax([str(p) == '[[2]]' for p in E])
    idx2 = np.argmax([str(p) == '[[6]]' for p in E])

    answer = (idx1 + 1) * (idx2 + 1)
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
