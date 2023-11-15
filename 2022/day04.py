import os
import sys
import numpy as np


# Lessons learned
#  - Write carefully (mis-typed an index)
#  - Less efficient, but had been easier to made sets of ranges:
#    "set(range(a, b+1))"


def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    answer = 0
    data = np.array([[int(x) for x in l.replace('-', ',').split(',')] for l in L])
    cL = (data[:, 0] <= data[:, 2]) & (data[:, 1] >= data[:, 3])
    cR = (data[:, 0] >= data[:, 2]) & (data[:, 1] <= data[:, 3])
    answer = np.sum(cL | cR)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    cO1 = (data[:, 0] <= data[:, 2]) & (data[:, 2] <= data[:, 1])
    cO2 = (data[:, 0] <= data[:, 3]) & (data[:, 3] <= data[:, 1])
    answer = np.sum(cL | cR | cO1 | cO2)
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
