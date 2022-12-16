import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def run(indata):
    L = indata.splitlines(keepends=False)
    D = [(l.split()[0], int(l.split()[1])) for l in L]
    
    # ----------- PART 1 -----------
    #
    T_vis = set()
    T = [0, 0]
    T_vis.add(tuple(T))
    H = [0, 0]
    for d, l in D:
        for _ in range(l):
            if d[0] == 'R':
                H[0] += 1
            elif d[0] == 'L':
                H[0] -= 1
            elif d[0] == 'U':
                H[1] -= 1
            elif d[0] == 'D':
                H[1] += 1

            if abs(H[0] - T[0]) + abs(H[1] - T[1]) > 2:
                T[0] += 1 if H[0] > T[0] else -1
                T[1] += 1 if H[1] > T[1] else -1
            elif abs(H[0] - T[0]) > 1:
                T[0] += 1 if H[0] > T[0] else -1
            elif abs(H[1] - T[1]) > 1:
                T[1] += 1 if H[1] > T[1] else -1
            T_vis.add(tuple(T))

    answer = len(T_vis)
    print("Part 1: {}".format(len(T_vis)))
    
    # ----------- PART 2 -----------
    #
    M = np.zeros((200, 250))
    N = np.zeros((200, 250))
    m = 144, 122
    j = 0
    lims = [0, 0, 0, 0]

    T_vis = set()
    T_vis.add((0, 0))
    R = np.zeros((10, 2), dtype=int)
    for d, l in D:
        lims = [
            min(R[0][1], lims[0]),
            max(R[0][1], lims[1]),
            min(R[0][0], lims[2]),
            max(R[0][0], lims[3]),
        ]
        for _ in range(l):
            if d[0] == 'R':
                R[0][0] += 1
            elif d[0] == 'L':
                R[0][0] -= 1
            elif d[0] == 'U':
                R[0][1] -= 1
            elif d[0] == 'D':
                R[0][1] += 1

            for i in range(1, 10):
                if abs(R[i-1][0] - R[i][0]) + abs(R[i-1][1] - R[i][1]) > 2:
                    R[i][0] += 1 if R[i-1][0] > R[i][0] else -1
                    R[i][1] += 1 if R[i-1][1] > R[i][1] else -1
                elif abs(R[i-1][0] - R[i][0]) > 1:
                    R[i][0] += 1 if R[i-1][0] > R[i][0] else -1
                elif abs(R[i-1][1] - R[i][1]) > 1:
                    R[i][1] += 1 if R[i-1][1] > R[i][1] else -1
                N[m[0] + R[i][1], m[1] + R[i][0]] = 1
            T_vis.add(tuple(R[-1]))
            
            M[m[0] + R[-1][1], m[1] + R[-1][0]] += 1
        j += 1
        if j % 10 == 0:
            I = np.dstack([N*63 + np.clip(M,0,8)*24, N*63 - np.clip(M,0,8)*4, N*63 - np.clip(M,0,8)*4]).astype(np.uint8)
            #plt.imsave('knots_{:04d}.png'.format(j), I)

        if True:
            for i in range(0, 10):
                M[m[0] + R[i][1], m[1] + R[i][0]] += 1
            M[m[0] + R[-1][1], m[1] + R[-1][0]] += 3
            
            for i in range(0, 10):
                M[m[0] + R[i][1], m[1] + R[i][0]] -= 1
            M[m[0] + R[-1][1], m[1] + R[-1][0]] -= 3
    
    answer = len(T_vis)
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
