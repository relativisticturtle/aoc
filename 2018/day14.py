import numpy as np
import matplotlib.pyplot as plt
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)

    # ----------- PART 1 -----------
    #
    r_max = int(L[0])

    R = [3, 7]
    E = [0, 1]
    while len(R) < r_max + 10:
        s = R[E[0]] + R[E[1]]
        if s >= 10:
            R.append(s // 10)
        R.append(s % 10)
        E[0] = (E[0] + 1 + R[E[0]]) % len(R)
        E[1] = (E[1] + 1 + R[E[1]]) % len(R)
    answer = ''.join([str(r) for r in R[r_max:(r_max+10)]])
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    r_pattern = tuple(int(l) for l in L[0])
    #r_pattern = (0, 1, 2, 4, 5)

    R = [3, 7]
    E = [0, 1]
    while len(R) < len(r_pattern):
        s = R[E[0]] + R[E[1]]
        if s >= 10:
            R.append(s // 10)
        R.append(s % 10)
        E[0] = (E[0] + 1 + R[E[0]]) % len(R)
        E[1] = (E[1] + 1 + R[E[1]]) % len(R)

    while True:
        s = R[E[0]] + R[E[1]]
        if s >= 10:
            R.append(s // 10)
            if tuple(R[-len(r_pattern):]) == r_pattern:
                answer = len(R) - len(r_pattern)
                break
        R.append(s % 10)
        if tuple(R[-len(r_pattern):]) == r_pattern:
            answer = len(R) - len(r_pattern)
            break
        E[0] = (E[0] + 1 + R[E[0]]) % len(R)
        E[1] = (E[1] + 1 + R[E[1]]) % len(R)
    print("Part 2: {}".format(answer))


if __name__ == '__main__':
    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
