import os
import sys
import numpy as np

def run(indata):
    P = [[[int(y) for y in x.split(',')] for x in l.split(' -> ')] for l in indata.splitlines(keepends=False)]
    
    xlim = [P[0][0][0], P[0][0][0]]
    ylim = [0, P[0][0][1]]
    for p in P:
        xlim[0] = min(xlim[0], np.min(np.array(p), axis=0)[0])
        xlim[1] = max(xlim[1], np.max(np.array(p), axis=0)[0])
        ylim[0] = min(ylim[0], np.min(np.array(p), axis=0)[1])
        ylim[1] = max(ylim[1], np.max(np.array(p), axis=0)[1])
    xlim[0] -= 1
    xlim[1] += 1
    ylim[1] += 1
    x0, y0 = xlim[0], ylim[0]
    M = np.zeros((ylim[1] - ylim[0] + 1, xlim[1] - xlim[0] + 1), dtype=int)

    for p in P:
        for i in range(len(p)-1):
            y = sorted([p[i][1], p[i+1][1]])
            x = sorted([p[i][0], p[i+1][0]])
            M[(y[0] - y0):(y[1] - y0 + 1), (x[0] - x0):(x[1] - x0 + 1)] = 1

    # ----------- PART 1 -----------
    #

    while True:
        p = [500 - x0, 0 - y0]
        while True:
            if p[1] + 1 >= M.shape[0]:
                break
            if M[p[1] + 1, p[0]] == 0:
                p[1] += 1
            elif M[p[1] + 1, p[0] - 1] == 0:
                p[1] += 1
                p[0] -= 1
            elif M[p[1] + 1, p[0] + 1] == 0:
                p[1] += 1
                p[0] += 1
            else:
                break
        if p[1] + 1 >= M.shape[0]:
            break
        M[p[1], p[0]] = 2

    # x592
    answer = np.sum(M==2)
    print("Part 1: {}".format(answer))
    
    
    # ----------- PART 2 -----------
    #
    M = np.pad(M, [[0, 1], [200, 200]])
    M[-1, :] = 1
    x0 -= 200
    M1 = np.copy(M)

    while True:
        p = [500 - x0, 0 - y0]
        while True:
            if p[1] + 1 >= M.shape[0]:
                break
            if M[p[1] + 1, p[0]] == 0:
                p[1] += 1
            elif M[p[1] + 1, p[0] - 1] == 0:
                p[1] += 1
                p[0] -= 1
            elif M[p[1] + 1, p[0] + 1] == 0:
                p[1] += 1
                p[0] += 1
            else:
                break
        if p[1] == 0:
            break
        M[p[1], p[0]] = 3
    M[p[1], p[0]] = 3
    answer = np.sum(M==2) + np.sum(M==3)
    print("Part 2: {}".format(answer))

    import matplotlib.pyplot as plt
    plt.subplot(2, 1, 1)
    plt.imshow(M1, interpolation='none')
    plt.gca().set(xticks=[], yticks=[])
    plt.subplot(2, 1, 2)
    plt.imshow(M, interpolation='none')
    plt.gca().set(xticks=[], yticks=[])
    plt.show()
    

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
