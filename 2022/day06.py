import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    L = L[0]
    
    # ----------- PART 1 -----------
    #
    for i in range(len(L)-3):
        if (L[i] != L[i+1] and L[i] != L[i+2] and L[i] != L[i+3] and
            L[i+1] != L[i+2] and L[i+1] != L[i+3] and L[i+2] != L[i+3]):
            answer = i + 4
            break
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = None
    for i in range(len(L)-3):
        if np.max(np.unique(list(L[i:(i+14)]), return_counts=True)[1]) == 1:
            answer = i + 14
            break
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
