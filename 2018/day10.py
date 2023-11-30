import numpy as np
import aoc

from collections import deque



def run(indata):
    L = indata.splitlines(keepends=False)

    P, V = [], []
    for l in L:
        P.append([int(x) for x in l.split('<')[1].split('>')[0].split(',')])
        V.append([int(x) for x in l.split('<')[2].split('>')[0].split(',')])
    P, V = np.array(P), np.array(V)

    # LSQ-solve
    t_guess, _, _, _ = np.linalg.lstsq(V.reshape(-1, 1), -P.reshape(-1, 1), rcond=None)
    t_answer = int(t_guess - 1)

    # ----------- PART 1 -----------
    #
    aoc.points.Set2D(P + t_answer * V).print()
    answer = 'XLZAKBGZ'
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    answer = t_answer
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':

    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
