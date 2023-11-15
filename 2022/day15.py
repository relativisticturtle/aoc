import os
import sys
import numpy as np
import time

def run(indata):
    L = indata.splitlines(keepends=False)
    
    S = dict()
    for l in L:
        s = tuple(int(x[2:]) for x in l[10:].split(':')[0].split(', '))
        b = tuple(int(x[2:]) for x in l.split('beacon')[1][7:].split(', '))
        S[s] = b

    # ----------- PART 1 -----------
    #
    T0 = time.time()
    
    y2m_x = -200000
    y2m_y = 2000000
    y2m_b = 1

    y2m = np.zeros(4700000, dtype=int)
    for s, b in S.items():
        d = abs(s[0] - b[0]) + abs(s[1] - b[1])
        y2m_d = d - abs(s[1] - y2m_y)
        assert s[0] - y2m_d - y2m_x >= 0
        assert s[0] + y2m_d - y2m_x + 1 < len(y2m)
        if y2m_d >= 0:
            y2m[(s[0] - y2m_d - y2m_x):(s[0] + y2m_d - y2m_x + 1)] = 1
    answer = np.sum(y2m) - y2m_b
    print("Part 1: {}".format(answer))
    print('Elapsed time (s): {}'.format(time.time() - T0))
    
    # ----------- PART 2 -----------
    #
    T0 = time.time()
    P = dict()
    for s, b in S.items():
        #break
        print('Processing sensor {}...'.format(s))
        d = abs(s[0] - b[0]) + abs(s[1] - b[1]) + 1

        for dx in range(-d, (d+1)):
            dy = d - abs(dx)
            p = (s[0] + dx, s[1] - dy)
            if p in P:
                P[p] += 1
            elif p[0] > 0 and p[0] < 4000001 and p[1] > 0 and p[1] < 4000001:
                P[p] = 1
            if dy == 0:
                continue
            p = (s[0] + dx, s[1] + dy)
            if p in P:
                P[p] += 1
            elif p[0] > 0 and p[0] < 4000001 and p[1] > 0 and p[1] < 4000001:
                P[p] = 1
    A = [p for p, f in P.items() if f > 3]
    #A = [(1780971, 230594), (1780972, 230595), (1830854, 280477), (3516124, 3802508), (3120101, 2634249), (1780973, 230594), (1807042, 204525), (3516123, 3802509), (1780972, 230593)]
    for a in A:
        for s, b in S.items():
            db = abs(s[0] - b[0]) + abs(s[1] - b[1])
            da = abs(s[0] - a[0]) + abs(s[1] - a[1])
            if da < db:
                break
        else:
            answer = 4000000 * a[0] + a[1]
            print(a)

    #answer = None
    print("Part 2: {}".format(answer))
    print('Elapsed time (s): {}'.format(time.time() - T0))
    print('A-dict: {} elements'.format(len(P)))


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
