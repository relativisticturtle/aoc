import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    M = np.array([[int(x) for x in l.split()] for l in L])
    M.sort(0)

    # ----------- PART 1 -----------
    #
    #answer = None
    # x 1410183
    answer = np.sum(np.abs(np.diff(M, axis=1)))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for i in range(len(M)):
        answer += np.sum(M[:, 1] == M[i, 0]) * M[i, 0]
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
