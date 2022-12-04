import os
import sys
import numpy as np


# Lessons learned
#  - understanding np.unique on matrices:
#    - just specifying "axis=") didn't produce expected results
#    - better make row-wise, column-wise (loops or comprehension)


def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    data = np.array([list(l) for l in L])
    answer = ''
    for c in range(data.shape[1]):
        abc, counts = np.unique(data[:, c], return_counts=True)
        answer += abc[np.argmax(counts)]
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = ''
    for c in range(data.shape[1]):
        abc, counts = np.unique(data[:, c], return_counts=True)
        answer += abc[np.argmin(counts)]
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
