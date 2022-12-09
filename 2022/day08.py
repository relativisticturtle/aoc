import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    F = np.array([[int(x) for x in l] for l in L])
    # ----------- PART 1 -----------
    #
    answer = 0
    trees = []
    for r in range(F.shape[0]):
        for c in range(F.shape[1]):
            if np.all(F[r, :c] < F[r, c]) or np.all(F[r, (c+1):] < F[r, c]):
                trees.append((r, c))
                answer += 1
                continue
            if np.all(F[:r, c] < F[r, c]) or np.all(F[(r+1):, c] < F[r, c]):
                trees.append((r, c))
                answer += 1
                continue
    #x8065
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for r, c in trees:
        n = F[:r, c][::-1] >= F[r, c]
        s = F[(r+1):, c] >= F[r, c]
        e = F[r, :c][::-1] >= F[r, c]
        w = F[r, (c+1):] >= F[r, c]

        score = 1
        for d in [n, s, e, w]:
            if np.any(d):
                score *= (np.argmax(d) + 1)
            else:
                score *= d.shape[0]

        answer = max(answer, score)
    # x148
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
