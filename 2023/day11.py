import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    # ----------- PART 1 -----------
    #
    M = aoc.points.Set2D.fromtext(indata)
    H = M.image()
    empty_cols = np.where(np.sum(H, axis=0) == 0)[0]
    empty_rows = np.where(np.sum(H, axis=1) == 0)[0]

    total_dist = 0
    for g in M.points:
        for h in M.points:
            x = sorted((g[0], h[0]))
            y = sorted((g[1], h[1]))
            dist = (x[1] - x[0]) + (y[1] - y[0])
            xtra = np.sum((x[0] < empty_cols) & (empty_cols < x[1]))
            ytra = np.sum((y[0] < empty_rows) & (empty_rows < y[1]))
            total_dist += dist + xtra + ytra

    answer = total_dist / 2
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    total_dist = 0
    for g in M.points:
        for h in M.points:
            x = sorted((g[0], h[0]))
            y = sorted((g[1], h[1]))
            dist = (x[1] - x[0]) + (y[1] - y[0])
            xtra = np.sum((x[0] < empty_cols) & (empty_cols < x[1]))
            ytra = np.sum((y[0] < empty_rows) & (empty_rows < y[1]))
            total_dist += dist + 999999 * np.int64(xtra + ytra)

    answer = total_dist / 2
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
