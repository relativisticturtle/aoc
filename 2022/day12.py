import os
import sys
import numpy as np
from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    M = np.array([list(l) for l in L])
    S = np.where(M=='S')
    E = np.where(M=='E')

    s = S[0][0], S[1][0]
    e = E[0][0], E[1][0]
    M[s] = 'a'
    M[e] = 'z'
    
    # ----------- PART 1 -----------
    #
    vis = np.zeros((472,) + M.shape)

    Q = deque()
    Q.append((s, 'a', 0))
    V = set()
    while len(Q) > 0:
        p, h, x = Q.popleft()
        if p == e:
            break
        elif p in V:
            continue
        else:
            V.add(p)
        
        vis[x:, p[0], p[1]] = x

        if p[0] > 0 and ord(M[p[0] - 1, p[1]]) <= ord(h) + 1:
            Q.append( ( (p[0] - 1, p[1]), M[p[0] - 1, p[1]], x + 1) )
        if p[0] < M.shape[0] - 1 and ord(M[p[0] + 1, p[1]]) <= ord(h) + 1:
            Q.append( ( (p[0] + 1, p[1]), M[p[0] + 1, p[1]], x + 1) )
        if p[1] > 0 and ord(M[p[0], p[1] - 1]) <= ord(h) + 1:
            Q.append( ( (p[0], p[1] - 1), M[p[0], p[1] - 1], x + 1) )
        if p[1] < M.shape[1] - 1 and ord(M[p[0], p[1] + 1]) <= ord(h) + 1:
            Q.append( ( (p[0], p[1] + 1), M[p[0], p[1] + 1], x + 1) )
    assert len(Q) > 0
    answer = x
    print("Part 1: {}".format(answer))

    # Visualize
    N = np.array([[ord(x) - ord('a') for x in m] for m in M]) / (ord('z') - ord('a'))
    vis = ((vis / 472) + (vis > 0)) / 2
    N = np.clip(np.stack([N + 0.5 * vis, N - 0.5 * vis, N - 0.5 * vis], 3), 0, 1)
    import matplotlib.pyplot as plt
    for j in range(N.shape[0]):
        plt.imsave('track_{:03d}.png'.format(j), N[j, ...])

    
    # ----------- PART 2 -----------
    #
    Q = deque()
    V = set()
    S = np.where(M=='a')
    for s in zip(list(S[0]), list(S[1])):
        Q.append((s, 'a', 0))
    while len(Q) > 0:
        p, h, x = Q.popleft()
        if p == e:
            break
        elif p in V:
            continue
        else:
            V.add(p)

        if p[0] > 0 and ord(M[p[0] - 1, p[1]]) <= ord(h) + 1:
            Q.append( ( (p[0] - 1, p[1]), M[p[0] - 1, p[1]], x + 1) )
        if p[0] < M.shape[0] - 1 and ord(M[p[0] + 1, p[1]]) <= ord(h) + 1:
            Q.append( ( (p[0] + 1, p[1]), M[p[0] + 1, p[1]], x + 1) )
        if p[1] > 0 and ord(M[p[0], p[1] - 1]) <= ord(h) + 1:
            Q.append( ( (p[0], p[1] - 1), M[p[0], p[1] - 1], x + 1) )
        if p[1] < M.shape[1] - 1 and ord(M[p[0], p[1] + 1]) <= ord(h) + 1:
            Q.append( ( (p[0], p[1] + 1), M[p[0], p[1] + 1], x + 1) )
    assert len(Q) > 0
    answer = x
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
