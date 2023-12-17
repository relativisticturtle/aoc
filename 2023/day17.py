import numpy as np
import aoc

def run(indata):
    M = np.array([[int(x) for x in line] for line in indata.splitlines(keepends=False)])

    def adjacent(p, start, stop):
        adj = []
        d = (p[3], p[2])
        for s in range(start, stop+1):
            q = (p[0] + s * d[0], p[1] + s * d[1], d[0], d[1])
            if aoc.in_range(q[:2], M.shape):
                adj.append(q)
            q = (p[0] - s * d[0], p[1] - s * d[1], -d[0], -d[1])
            if aoc.in_range(q[:2], M.shape):
                adj.append(q)
        return adj

    def cost(p, q):
        yr = sorted([p[0], q[0]])
        xr = sorted([p[1], q[1]])
        return np.sum(M[yr[0]:(yr[1] + 1), xr[0]:(xr[1] + 1)]) - M[p[:2]]

    def finished(p):
        return (p[0] == M.shape[0] - 1) and (p[1] == M.shape[1] - 1)

    # ----------- PART 1 -----------
    #
    adjacent1 = lambda p: adjacent(p, 1, 3)
    answer = aoc.search.Path(adjacent1, cost, finished).initial({(0, 0, 1, 0), (0, 0, 0, 1)}).run().result()
    print("Part 1: {}".format(answer)) # 1001
    
    # ----------- PART 2 -----------
    #
    adjacent1 = lambda p: adjacent(p, 4, 10)
    answer = aoc.search.Path(adjacent1, cost, finished).initial({(0, 0, 1, 0), (0, 0, 0, 1)}).run().result()
    print("Part 2: {}".format(answer)) # 1197


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
