import itertools
import numpy as np


def run(indata):
    K = []
    L = []
    for b in [block.splitlines(keepends=False) for block in indata.split('\n\n')]:
        A = np.array([list(l) for l in b])
        if all(A[0, :] == '.'):     #key
            K.append(np.sum(A=='#', axis=0))
        elif all(A[0, :] == '#'):   #lock
            L.append(np.sum(A=='#', axis=0))
        else:
            raise RuntimeError

    answer = 0
    for k, l in itertools.product(K, L):
        if np.all(k+l < 8):
            answer += 1
    
    # ----------- PART 1 -----------
    #
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    print("Part 2: Merry Christmas!")
    return answer


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    #indata = get_input(test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
