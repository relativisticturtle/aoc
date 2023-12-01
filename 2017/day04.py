def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    # ----------- PART 1 -----------
    #
    answer = 0
    for l in L:
        words = l.split()
        unique = set(words)
        if len(words) == len(unique):
            answer += 1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for l in L:
        words = [''.join(sorted(w)) for w in l.split()]
        unique = set(words)
        if len(words) == len(unique):
            answer += 1
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
