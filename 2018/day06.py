import os
import sys
import numpy as np

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    data = np.array([[int(a) for a in l.split(',')] for l in L])
    xlim = np.min(data[:, 0]), np.max(data[:, 0]) + 1
    ylim = np.min(data[:, 1]), np.max(data[:, 1]) + 1

    X, Y = np.meshgrid(np.arange(*xlim), np.arange(*ylim))
    D = np.array([np.abs(X - xy[0]) + np.abs(Y - xy[1]) for xy in data])
    A = np.argmin(D, axis=0)
    B = np.take_along_axis(D, A[np.newaxis, ...], axis=0)[0]
    C = np.sum(D == B, axis=0)
    A[C > 1] = -1

    area = 0
    for c in range(len(data)):
        if c in A[0, :] or c in A[-1, :] or c in A[:, 0] or c in A[:, -1]:
            continue
        area = max(area, np.sum(A==c))
    answer = area
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    answer = np.sum(np.sum(D, axis=0) < 10000)
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
