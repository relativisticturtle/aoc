import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def plot(M, path):
    import matplotlib.pyplot as plt
    N = np.array([[{' ': 0, '.': 255, '#': 128}[x] for x in X] for X in M])
    plt.imshow(N, cmap='gray')
    plt.plot(np.asarray(path)[:, 0], np.asarray(path)[:, 1])
    plt.show()

def run(indata):
    L = indata.splitlines(keepends=False)
    M = np.array([[x == '#' for x in l]  for l in L], dtype=int)
    M = np.pad(M, [(60, 60), (70, 70)], mode='constant', constant_values=0)

    D = [
        [( 0, -1), (-1, -1), ( 1, -1)],
        [( 0,  1), (-1,  1), ( 1,  1)],
        [(-1,  0), (-1, -1), (-1,  1)],
        [( 1,  0), ( 1, -1), ( 1,  1)],
    ]
    import itertools
    
    # ----------- PART 1 -----------
    #
    turn = -1
    while True:
        turn += 1
        if turn == 10:
            L = np.argmax(np.any(M, axis=0))
            R = M.shape[1] - np.argmax(np.any(M[:, ::-1], axis=0)) - 1
            T = np.argmax(np.any(M, axis=1))
            B = M.shape[0] - np.argmax(np.any(M[::-1, :], axis=1)) - 1
                
            answer = np.sum(M[T:(B+1), L:(R+1)]==0)
            print("Part 1: {}".format(answer))
        # Pass 1
        P = np.zeros_like(M)
        Px = np.zeros_like(M)
        for r, c in zip(*np.where(M)):
            if r == 0 or c == 0 or r + 1 == M.shape[0] or c + 1 == M.shape[1]:
                continue
            if M[r, c] == 0:
                continue
            if np.sum(M[(r-1):(r+2), (c-1):(c+2)]) < 2:
                continue
            for t in range(4):
                d = (turn + t) % 4
                if M[r + D[d][0][1], c + D[d][0][0]] == 0 and M[r + D[d][1][1], c + D[d][1][0]] == 0 and M[r + D[d][2][1], c + D[d][2][0]] == 0:
                    P[r + D[d][0][1], c + D[d][0][0]] += 1
                    Px[r, c] = d + 1
                    break
        # Pass 2
        N = M.copy()
        for r, c in zip(*np.where(M)):
            if Px[r, c] == 0:
                continue
            d = Px[r, c] - 1
            if P[r + D[d][0][1], c + D[d][0][0]] == 1:
                N[r, c] = 0
                N[r + D[d][0][1], c + D[d][0][0]] = 1

        # Update
        if np.all(M == N):
            break
        M = N
    
    L = np.argmax(np.any(M, axis=0))
    R = M.shape[1] - np.argmax(np.any(M[:, ::-1], axis=0)) - 1
    T = np.argmax(np.any(M, axis=1))
    B = M.shape[0] - np.argmax(np.any(M[::-1, :], axis=1)) - 1
        
    # ----------- PART 2 -----------
    #
    answer = turn + 1
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
