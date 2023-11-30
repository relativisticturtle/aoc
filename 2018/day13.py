import numpy as np
import matplotlib.pyplot as plt
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)

    carts = []
    for iy, row in enumerate(L):
        for ix, c in enumerate(row):
            if c in aoc.V4:
                d = aoc.V4.index(c)
                carts.append([iy, ix, d, 0])
    M = [l.replace('>', '-').replace('<', '-').replace('^', '|').replace('v', '|') for l in L]
    
    def evolve(carts, M):
        crash = None
        crashed = []
        carts = sorted(carts)
        for i, cart in enumerate(carts):
            ix, iy, d, s = cart[1], cart[0], cart[2], cart[3]
            ix += aoc.D4[d][0]
            iy += aoc.D4[d][1]
            for j, other_cart in enumerate(carts):
                if j == i:
                    continue
                if (ix, iy) == (other_cart[1], other_cart[0]):
                    crashed.append(i)
                    crashed.append(j)
                    crash = iy, ix
            if M[iy][ix] == '/':
                d = [3, 2, 1, 0][d]
            elif M[iy][ix] == '\\':
                d = [1, 0, 3, 2][d]
            elif M[iy][ix] == '+':
                d = (d + [1, 0, -1][s]) % 4
                s = (s + 1) % 3
            elif M[iy][ix] in '|-':
                pass
            else:
                print('error')
            carts[i] = [iy, ix, d, s]
        carts = [cart for i, cart in enumerate(carts) if i not in crashed]
        return carts, crash
    
    def print_state(carts, M):
        M = [[c for c in row] for row in M]
        for i, cart in enumerate(carts):
            ix, iy, d, s = cart[1], cart[0], cart[2], cart[3]
            M[iy][ix] = aoc.V4[d]
        print('\n'.join([''.join(row) for row in M]))

    # ----------- PART 1 -----------
    #
    out = None
    while out is None:
        carts, out = evolve(carts, M)
    answer = out[1], out[0]
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    while len(carts) > 1:
        carts, out = evolve(carts, M)
    answer = carts[0][1], carts[0][0]
    print("Part 2: {}".format(answer))


if __name__ == '__main__':

    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
