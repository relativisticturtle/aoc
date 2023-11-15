import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    S = np.array([(ord(l[0]) - ord('A') + 1, ord(l[2]) - ord('X') + 1) for l in L])
    
    # ----------- PART 1 -----------
    #
    answer = np.sum(S[:, 1] + 3 * np.mod(S[:, 1] - S[:, 0] + 1, 3))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    M = np.mod((S[:, 0] - 1) + (S[:, 1] - 2), 3) + 1
    answer = np.sum(M + 3 * (S[:, 1] - 1))
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
