import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    M = np.array([list(l) for l in L])
    y, x = np.where(M=='S')
    p0 = y[0], x[0], 0
    y, x = np.where(M=='E')
    goal = y[0], x[0]
    
    # ----------- PART 1 -----------
    #
    def adjacencies(p):
        adj = []
        d = aoc.D4[p[2]]
        q = p[0] + d[0], p[1] + d[1]
        if M[q] != '#':
            adj.append(q + (p[2],))
        adj.append(p[:2] + ((p[2]+1)%4,))
        adj.append(p[:2] + ((p[2]-1)%4,))
        return adj
    
    def cost(a, b):
        return 1 if a[2] == b[2] else 1000

    s = aoc.search.Path(adjacencies, cost).initial(p0).run()
    dgoal = np.argmin([
        s.result(goal + (0,)),
        s.result(goal + (1,)),
        s.result(goal + (2,)),
        s.result(goal + (3,)),
    ])
    answer = s.result(goal + (dgoal,)),
    print("Part 1: {}".format(answer))
    #return answer
    
    # ----------- PART 2 -----------
    #
    def adjacencies(p):
        d = aoc.D4[p[2]]
        A = [
            (p[0] - d[0], p[1] - d[1], p[2]),
            (p[0], p[1], (p[2] - 1) % 4),
            (p[0], p[1], (p[2] + 1) % 4),
        ]
        C = [1000000000] * 3
        for i, a in enumerate(A):
            if a not in s.visited():
                continue
            C[i] = s.result(a) + (1 if i == 0 else 1000)
        if min(C) != s.result(p):
            print(p)
        best_c = s.result(p)
        return [a for a, c in zip(A, C) if c == best_c]
    
    r = aoc.search.Path(adjacencies).initial(goal + (dgoal,)).run()

    M2 = M.copy()
    for p in r.visited():
        M[p[:2]] = 'O'

    answer = len(set([p[:2] for p in r.visited()]))
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
