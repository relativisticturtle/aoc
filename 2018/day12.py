import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    S0 = L[0][15:]
    M = {l[:5]: l[-1] for l in L[2:]}

    def evolve(pots, start):
        pots = '....' + pots + '....'
        next_pots = ''.join([M.get(pots[(i-2):(i+3)], '.') for i in range(2, len(pots)-3)])
        x1 = next_pots.find('#')
        x2 = next_pots.rfind('#')
        next_pots = next_pots[x1:(x2+1)]
        next_start = start + x1 - 2
        return next_pots, next_start

    e = aoc.simul.Evolution(evolve, S0, 0).run(20)
    pots, start = e.history()
    answer = sum([(start + i) if c == '#' else 0 for i, c in enumerate(pots)])
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    pots, loops, start1, start2 = e.run().extrapolate(50000000000)
    start = start1 + (start2 - start1) * loops
    answer = sum([(start + i) if c == '#' else 0 for i, c in enumerate(pots)])
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':

    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
