import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    D = np.array([[int(x) for x in l.split(',')] for l in L], dtype=int)
    M = np.zeros((24, 24, 24), dtype=int)
    for (x, y, z) in D:
        M[x+1, y+1, z+1] = 1

    
    # ----------- PART 1 -----------
    #
    answer = np.sum(np.abs(np.diff(M, axis=0))) + np.sum(np.abs(np.diff(M, axis=1))) + np.sum(np.abs(np.diff(M, axis=2)))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    from collections import deque
    N = np.ones_like(M)
    Q = deque()
    Q.append((0, 0, 0))

    while len(Q) > 0:
        xyz = Q.popleft()
        if xyz[0] < 0 or xyz[1] < 0 or xyz[2] < 0:
            continue
        if xyz[0] == N.shape[0] or xyz[1] == N.shape[1] or xyz[2] == N.shape[2]:
            continue
        if M[xyz[0], xyz[1], xyz[2]] == 1:
            continue
        if N[xyz[0], xyz[1], xyz[2]] == 0:
            continue
        N[xyz[0], xyz[1], xyz[2]] = 0

        for i in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
            Q.append((xyz[0] + i[0], xyz[1] + i[1], xyz[2] + i[2]))
            
    answer = np.sum(np.abs(np.diff(N, axis=0))) + np.sum(np.abs(np.diff(N, axis=1))) + np.sum(np.abs(np.diff(N, axis=2)))
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
