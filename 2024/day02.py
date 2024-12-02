import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    D = [[int(x) for x in l.split()] for l in L]
    
    # ----------- PART 1 -----------
    #
    answer = 0

    for l in D:
        d = np.diff(l)
        if np.any(d > 0) and np.any(d < 0):
            continue
        if np.min(np.abs(d)) == 0 or np.max(np.abs(d)) > 3:
            continue
        answer += 1

    # x 269
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for l in D:
        for ex in range(len(l) + 1):
            d = np.diff(l[:ex] + l[(ex+1):])
            if np.any(d > 0) and np.any(d < 0):
                continue
            if np.min(np.abs(d)) == 0 or np.max(np.abs(d)) > 3:
                continue
            answer += 1
            break

    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input() #test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
