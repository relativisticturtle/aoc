import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    data = np.array([[int(d) for d in r.split()] for r in L])
    sdata = np.sort(data, axis=1)
    answer = np.sum(sdata[:, 0] + sdata[:, 1] > sdata[:, 2])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    sdata = np.sort(data.reshape((-1, 3, 3)), axis=1)
    answer = np.sum(sdata[:, 0, :] + sdata[:, 1, :] > sdata[:, 2, :])
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
