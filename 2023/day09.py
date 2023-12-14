import numpy as np
import aoc

def run(indata):
    V0 = [[int(x) for x in l.split()] for l in indata.splitlines(keepends=False)]
    
    # ----------- PART 1 & 2 -----------
    #
    answer1 = 0
    answer2 = 0
    for v0 in V0:
        V = [v0]
        while len(V[-1]) > 1:
            V.append(list(np.diff(V[-1])))
            if np.all(V[-1] == V[-1][0]):
                break
        while len(V) > 1:
            V[-2]= [V[-2][0] - V[-1][0]] + V[-2] + [V[-2][-1] + V[-1][-1]]
            V = V[:-1]
        answer1 += V[0][-1]
        answer2 += V[0][0]
    print("Part 1: {}".format(answer1)) # 1974913025
    print("Part 2: {}".format(answer2)) # 884

    # ---- With NumPy-polynomial ----
    #
    from numpy.polynomial.polynomial import Polynomial
    answer = [0, 0]
    for line in indata.splitlines(keepends=False):
        y = [int(x) for x in line.split()]
        poly = Polynomial.fit(np.arange(len(y)), y, deg=len(y)-1 + 5)
        answer[0] += round(poly(len(y)))
        answer[1] += round(poly(-1))
        print(len(y))
    print("Part 1: {}\nPart 2: {}".format(*answer))


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
