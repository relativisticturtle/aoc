def run(indata):
    # number of winning cards per game
    G = [
        set.intersection(*[set(map(int, v.split())) for v in l.split(':')[1].split('|')])
        for l in indata.splitlines(keepends=False)
    ]
    
    # ----------- PART 1 -----------
    #
    answer = sum([int(2**(len(g) - 1)) for g in G])
    print("Part 1: {}".format(answer)) # 21105

    # ----------- PART 2 -----------
    #
    won_card = [1] * len(G)
    for i, g in enumerate(G):
        w = len(g)
        while w > 0:
            won_card[i + w] += won_card[i]
            w -= 1
    answer = sum(won_card)
    print("Part 2: {}".format(answer)) # 5329815


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
