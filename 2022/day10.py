import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    X = [0]
    C = [0]
    for l in L:
        if l.startswith('addx'):
            X.append(int(l.split()[1]))
            C.append(2)
        else:
            X.append(0)
            C.append(1)
    C = np.cumsum(C)
    X = 1 + np.cumsum(X)

    answer = 0
    for cycle in 20, 60, 100, 140, 180, 220:
        idx = np.argmax(C >= cycle) - 1
        signal = X[idx]
        print('{} : {}'.format(cycle, signal))
        answer += cycle * signal
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    D = ''
    for cycle in range(240):
        idx = np.argmax(C > cycle) - 1
        if abs(X[idx] - (cycle%40)) < 2:
            D += '#'
        else:
            D += '.'

    print(D[  0: 40])
    print(D[ 40: 80])
    print(D[ 80:120])
    print(D[120:160])
    print(D[160:200])
    print(D[200:240])
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
