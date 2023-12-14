import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    M = [np.array([list(line) for line in block.splitlines(keepends=False)]) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    
    # ----------- PART 1 -----------
    #
    answer = 0
    for m in M:
        for r in range(1, m.shape[1]):
            w = min(r, m.shape[1] - r)
            if np.all(m[:, (r-w):r] == np.fliplr(m[:, r:(r+w)])):
                answer += r

        for r in range(1, m.shape[0]):
            w = min(r, m.shape[0] - r)
            if np.all(m[(r-w):r, :] == np.flipud(m[r:(r+w), :])):
                answer += 100 * r

    print("Part 1: {}".format(answer))  # 33728
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for m in M:
        for r in range(1, m.shape[1]):
            w = min(r, m.shape[1] - r)
            if np.sum(m[:, (r-w):r] != np.fliplr(m[:, r:(r+w)])) == 1:
                answer += r

        for r in range(1, m.shape[0]):
            w = min(r, m.shape[0] - r)
            if np.sum(m[(r-w):r, :] != np.flipud(m[r:(r+w), :])) == 1:
                answer += 100 * r

    print("Part 2: {}".format(answer)) # 28235
    

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
