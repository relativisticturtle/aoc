import itertools
import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    M = np.array([list(l) for l in L])

    start = np.where(M=='S')
    stop = np.where(M=='E')
    start = start[0][0], start[1][0]
    stop = stop[0][0], stop[1][0]
    M[start] = '.'
    M[stop] = '.'
    
    def adjencies(p):
        return [q for q in aoc.neighbors(p, lim=M.shape) if M[q]=='.']
    s = aoc.search.Path(adjencies).initial(start).run()

    # ----------- PART 1 -----------
    #
    answer = 0
    DX = set()
    for d1, d2 in itertools.product(aoc.D4, repeat=2):
        DX.add((d1[0] + d2[0], d1[1] + d2[1]))
    for p in s.visited():
        for d in DX:
            q = p[0]+d[0], p[1]+d[1]
            if q not in s.visited():
                continue
            if s.result(q) - s.result(p) - abs(d[0]) - abs(d[1]) >= 100:
                answer += 1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    DX = set()
    for dy in range(-20, 21):
        for dx in range(-20, 21):
            if abs(dx) + abs(dy) <= 20:
                DX.add((dy, dx))
    answer = 0
    for p in s.visited():
        for d in DX:
            q = p[0]+d[0], p[1]+d[1]
            if q not in s.visited():
                continue
            if s.result(q) - s.result(p) - abs(d[0]) - abs(d[1]) >= 100:
                answer += 1
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
