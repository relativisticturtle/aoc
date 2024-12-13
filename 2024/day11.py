import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    S0 = tuple((int(x) for x in L[0].split()))

    # ----------- PART 1 -----------
    #
    def evolve(S):
        S2 = []
        for x in S:
            s = str(x)
            if x == 0:
                S2.append(1)
            elif len(s) % 2 == 0:
                S2.append(int(s[:(len(s)//2)]))
                S2.append(int(s[(len(s)//2):]))
            else:
                S2.append(x * 2024)
        return tuple(S2)

    S = S0
    for _ in range(25):
        S = evolve(S)
    answer = len(S)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    from collections import defaultdict
    def evolve2(S):
        S2 = defaultdict(int)
        for x, v in S.items():
            s = str(x)
            if x == 0:
                S2[1] += v
            elif len(s) % 2 == 0:
                S2[int(s[:(len(s)//2)])] += v
                S2[int(s[(len(s)//2):])] += v
            else:
                S2[x * 2024] += v
        return S2

    S = defaultdict(int)
    for x in S0:
        S[x] += 1
    for _ in range(75):
        S = evolve2(S)
        #print(len(S))
    answer = sum([v for v in S.values()])

    print("Part 2: {}".format(answer))
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
