import os
import sys
import numpy as np


def plot(M, path):
    import matplotlib.pyplot as plt
    N = np.array([[{' ': 0, '.': 255, '#': 128}[x] for x in X] for X in M])
    plt.imshow(N, cmap='gray')
    plt.plot(np.asarray(path)[:, 0], np.asarray(path)[:, 1])
    plt.show()


def run(indata):
    L = indata.splitlines(keepends=False)
    W = max([len(l) for l in L[:-2]])
    M = np.array([list(l + (' ' * (W - len(l))))  for l in L[:-2]])
    P = L[-1]
    P = ' R '.join(P.split('R'))
    P = ' L '.join(P.split('L'))
    P = P.split(' ')
    
    D = [
        (1, 0),     # >
        (0, 1),     # v
        (-1, 0),    # <
        (0, -1),    # ^
    ]

    # ----------- PART 1 -----------
    #
    x, y, v = np.argmax(M[0] == '.'), 0, 0
    for p in P:
        if p.isdigit():
            for _ in range(int(p)):
                nx, ny = (x + D[v][0]) % M.shape[1], (y + D[v][1]) % M.shape[0]
                while M[ny, nx] == ' ':
                    nx, ny = (nx + D[v][0]) % M.shape[1], (ny + D[v][1]) % M.shape[0]
                if M[ny, nx] == '.':
                    x, y = nx, ny
                else:
                    break
        elif p == 'L':
            v = (v - 1) % 4
        elif p == 'R':
            v = (v + 1) % 4
        else:
            assert False
    answer = 1000 * (y + 1) + 4 * (x + 1) + v
    print("Part 1: {}".format(answer)) # 186128
    
    # ----------- PART 2 -----------
    #
    T = {
        # Original face, original direction  --> New face, new direction
        (1, 0): (2, 0),
        (1, 1): (4, 1),
        (1, 2): (6, 0),
        (1, 3): (9, 0),

        (2, 0): (7, 2),
        (2, 1): (4, 2),
        (2, 2): (1, 2),
        (2, 3): (9, 3),

        (4, 0): (2, 3),
        (4, 1): (7, 1),
        (4, 2): (6, 1),
        (4, 3): (1, 3),

        (6, 0): (7, 0),
        (6, 1): (9, 1),
        (6, 2): (1, 0),
        (6, 3): (4, 0),

        (7, 0): (2, 2),
        (7, 1): (9, 2),
        (7, 2): (6, 2),
        (7, 3): (4, 3),

        (9, 0): (7, 3),
        (9, 1): (2, 1),
        (9, 2): (1, 1),
        (9, 3): (6, 3),
    }
    
    path = []
    x, y, v = np.argmax(M[0] == '.'), 0, 0
    for p in P:
        if p.isdigit():
            for _ in range(int(p)):
                old_face = 3 * (y // 50) + (x // 50)
                nx, ny, nv = (x + D[v][0]) % M.shape[1], (y + D[v][1]) % M.shape[0], v
                if 3 * (ny // 50) + (nx // 50) != old_face:
                    if v == 0:
                        t = y % 50
                    elif v == 1:
                        t = 49 - (x % 50)
                    elif v == 2:
                        t = 49 - (y % 50)
                    elif v == 3:
                        t = x % 50
                    else:
                        assert False
                    
                    newface, nv = T[old_face, v]
                    fx, fy = 50 * (newface % 3), 50 * (newface // 3)
                    if nv == 0:
                        nx, ny = fx, fy + t
                    elif nv == 1:
                        nx, ny = fx + 49 - t, fy
                    elif nv == 2:
                        nx, ny = fx + 49, fy + 49 - t
                    elif nv == 3:
                        nx, ny = fx + t, fy + 49
                    else:
                        assert False

                if M[ny, nx] == '.':
                    x, y, v = nx, ny, nv
                    path.append([x, y])
                elif M[ny, nx] == '#':
                    #plot(M, path)
                    break
                else:
                    assert False
        elif p == 'L':
            v = (v - 1) % 4
        elif p == 'R':
            v = (v + 1) % 4
        else:
            assert False
    
    #x119020 (too high)
    #x101015 (too high)
    #x89204 (too high)
    answer = 1000 * (y + 1) + 4 * (x + 1) + v
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
