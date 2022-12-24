import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    C = np.array([[int(c) for c in L], range(len(L))], dtype=np.int64)

    def mixing(C):
        for x in range(C.shape[1]):
            idx = np.argmax(C[1, :] == x)
            val = C[0, idx]
            moveto = (val + idx) % (C.shape[1] - 1)
            if moveto > idx:
                C[:, idx:moveto] = C[:, (idx+1):(moveto+1)]
                C[:, moveto] = val, x
            elif moveto < idx:
                C[:, (moveto+1):(idx+1)] = C[:, moveto:idx]
                C[:, moveto] = val, x

    # ----------- PART 1 -----------
    #
    D = C.copy()
    mixing(D)
    d = np.argmax(D[0, :] == 0)
    answer = np.sum(D[0, [(d+1000)%D.shape[1], (d+2000)%D.shape[1], (d+3000)%D.shape[1]]])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    D = C.copy()
    D[0, :] *= 811589153
    for _ in range(10):
        mixing(D)
    d = np.argmax(D[0, :] == 0)
    answer = np.sum(D[0, [(d+1000)%D.shape[1], (d+2000)%D.shape[1], (d+3000)%D.shape[1]]])
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
