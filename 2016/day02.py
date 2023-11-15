import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    answer = ''
    pos = [1, 1]
    for l in L:
        for c in l:
            if c == 'L' and pos[0] > 0:
                pos[0] -= 1
            if c == 'R' and pos[0] < 2:
                pos[0] += 1
            if c == 'U' and pos[1] > 0:
                pos[1] -= 1
            if c == 'D' and pos[1] < 2:
                pos[1] += 1
        answer += str(pos[0] + 3 * pos[1] + 1)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = ''
    keypad = ['  1  ', ' 234 ', '56789', ' ABC ', '  D  ']
    pos = [2, 2]
    for l in L:
        for c in l:
            if c == 'L' and pos[0] > abs(pos[1] - 2):
                pos[0] -= 1
            if c == 'R' and pos[0] < 4 - abs(pos[1] - 2):
                pos[0] += 1
            if c == 'U' and pos[1] > abs(pos[0] - 2):
                pos[1] -= 1
            if c == 'D' and pos[1] < 4 - abs(pos[0] - 2):
                pos[1] += 1
        answer += keypad[pos[1]][pos[0]]
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
