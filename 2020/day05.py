import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
#from collections import deque

def run(indata):
    L = indata.splitlines()
    
    seat_ids = []
    for l in L:
        row_code = l[:7].replace('B', '1').replace('F', '0')
        col_code = l[7:].replace('R', '1').replace('L', '0')
        row = int(row_code, 2)
        col = int(col_code, 2)
        
        print('{}, {} : {}, {}'.format(row_code, col_code, row, col))
        seat_ids.append(row*8 + col)

    answer = np.max(seat_ids)
    print("Part 1: {}".format(answer))
    clipboard_set("{}".format(answer))

    # ----------- PART 2 -----------
    #
    for sid in range(np.min(seat_ids), np.max(seat_ids)):
        if sid not in seat_ids:
            answer = sid
            break
    print("Part 2: {}".format(answer))
    clipboard_set("{}".format(answer))


if __name__ == '__main__':
    indata = get_input(day=5, year=2020)
    run(indata)
