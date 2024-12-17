import numpy as np
import aoc


def run(indata):
    M = np.array([list(l) for l in indata.splitlines(keepends=False)])
    y, x = np.where(M=='S')
    p0 = y[0], x[0], 0          # Start, facing east
    y, x = np.where(M=='E')
    goal = y[0], x[0]           # Goal, unknown direction
    
    # ----------- PART 1 -----------
    #
    def adjacencies(p):
        # Straight ahead or turn 90 deg cw/ccw
        adj = []
        d = aoc.D4[p[2]]
        q = p[0] + d[0], p[1] + d[1]
        if M[q] != '#':
            adj.append(q + (p[2],))
        adj.append(p[:2] + ((p[2]+1)%4,))
        adj.append(p[:2] + ((p[2]-1)%4,))
        return adj
    
    def cost(a, b):
        # Cost 1 for straight ahead, 1000 for turning
        return 1 if a[2] == b[2] else 1000

    # Cheapest path with costs (Djikstra)
    s = aoc.search.Path(adjacencies, cost).initial(p0).run()
    dgoal = np.argmin([
        s.result(goal + (0,)),
        s.result(goal + (1,)),
        s.result(goal + (2,)),
        s.result(goal + (3,)),
    ])
    answer = s.result(goal + (dgoal,))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    def adjacencies(p):
        # Check backwards for paths that don't
        # incur sub-optimal cost
        max_cost = s.result(p)
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
            C[i] = s.result(a) + cost(p, a)
        return [a for a, c in zip(A, C) if c == max_cost]

    r = aoc.search.Path(adjacencies).initial(goal + (dgoal,)).run()
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
