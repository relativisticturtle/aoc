import numpy as np
import aoc



def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]


    H = [(l.split()[0], int(l.split()[1])) for l in L]

    
    # ----------- PART 1 -----------
    #
    def rank(h):
        hand = tuple(sorted([sum([c == z for c in h[0]]) for z in h[0]])[::-1])
        h_rank = h[0]
        h_rank = h_rank.replace('T', 'a')
        h_rank = h_rank.replace('J', 'b')
        h_rank = h_rank.replace('Q', 'c')
        h_rank = h_rank.replace('K', 'd')
        h_rank = h_rank.replace('A', 'e')
        return (hand, h_rank)
    H_sorted = sorted(H, key=rank)
    answer = sum([h[1] * (r + 1) for r, h in enumerate(H_sorted)])
    print("Part 1: {}".format(answer)) # x247886171
    
    # ----------- PART 2 -----------
    #
    def rank(h):
        # Do Joker-replace (brute-force)
        hands = []
        for c in '23456789TQKA':
            h2 = h[0].replace('J', c)
            hands.append(tuple(sorted([sum([c == z for c in h2]) for z in h2])[::-1]))
        hand = sorted(hands)[-1]

        h_rank = h[0]
        h_rank = h_rank.replace('T', 'a')
        h_rank = h_rank.replace('J', '1')
        h_rank = h_rank.replace('Q', 'c')
        h_rank = h_rank.replace('K', 'd')
        h_rank = h_rank.replace('A', 'e')
        return (hand, h_rank)
    H_sorted = sorted(H, key=rank)
    answer = sum([h[1] * (r + 1) for r, h in enumerate(H_sorted)])
    print("Part 2: {}".format(answer)) # x244974022
    

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
