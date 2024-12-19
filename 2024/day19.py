import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    patterns = set(L[0].split(', '))
    towels = L[2:]

    # ----------- PART 1 & 2 -----------
    #
    possib = {'': 1}
    def possible(t):
        if t in possib:
            return possib[t]
        c = 0
        for p in patterns:
            if t.startswith(p):
                c += possible(t[len(p):])
        possib[t] = c
        return c

    answer = sum([possible(t) != 0 for t in towels])
    print("Part 1: {}".format(answer))
    answer = sum([possible(t) for t in towels])
    print("Part 2: {}".format(answer))


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))