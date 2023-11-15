import os
import sys

import numpy as np
import hw_python.utils.transformations as T
M_left = T.rotate(90, 'Z', degrees=True)
M_right = T.rotate(-90, 'Z', degrees=True)
M_fw = T.translate(0, 1, 0)

def run(indata):
    L = indata.splitlines(keepends=False)

    # ----------- PART 1 -----------
    #
    M = T.id()
    for s in L[0].split(','):
        d, l = s.strip()[0], int(s.strip()[1:])
        if d == 'L':
            M = M @ M_left @ np.linalg.matrix_power(M_fw, l)
        elif d == 'R':
            M = M @ M_right @ np.linalg.matrix_power(M_fw, l)
        else:
            assert False
    pos = M[:2, 3].round().astype(int)
    answer = abs(pos[0]) + abs(pos[1])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    visited = set()
    visited.add((0, 0))
    M = T.id()
    for s in L[0].split(','):
        d, l = s.strip()[0], int(s.strip()[1:])
        if d == 'L':
            M = M @ M_left
        elif d == 'R':
            M = M @ M_right
        else:
            assert False
        
        for _ in range(l):
            M = M @ M_fw
            pos = tuple(M[:2, 3].round().astype(int))
            if pos in visited:
                break
            visited.add(pos)
        else:
            continue
        break
    
    answer = abs(pos[0]) + abs(pos[1])
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
