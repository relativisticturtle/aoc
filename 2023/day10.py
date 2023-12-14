import numpy as np
import aoc

def run(indata):
    M = np.array([list(x) for x in indata.splitlines(keepends=False)])
    S = np.where(M == 'S')
    S = S[0][0], S[1][0]
    
    # ----------- PART 1 -----------
    #
    def adjacencies(p):
        #print(p)
        adj = []
        for q in aoc.neighbors(p, lim=M.shape):
            if q[1] - p[1] == 1 and  M[p] in 'S-LF' and M[q] in '-J7':
                adj.append(q)
            elif q[1] - p[1] == -1 and  M[p] in 'S-J7' and M[q] in '-LF':
                adj.append(q)
            elif q[0] - p[0] == 1 and  M[p] in 'S|7F' and M[q] in '|LJ':
                adj.append(q)
            elif q[0] - p[0] == -1 and  M[p] in 'S|LJ' and M[q] in '|7F':
                adj.append(q)
        return adj

    search = aoc.search.Path(adjacencies).initial(S).run()
    answer = max([search.result(p) for p in search.visited()])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    longest = answer
    longest_path = [p for p in search.visited() if search.result(p) == longest]
    next_longest_paths = [p for p in search.visited() if search.result(p) == longest - 1]
    assert len(next_longest_paths) == 2
    path = search.path_to(next_longest_paths[0]) + longest_path + search.path_to(next_longest_paths[1])[-1:0:-1]

    R = np.zeros(M.shape, dtype=int)
    for i in range(len(path)):
        p = path[i]
        q = path[(i + 1) % len(path)]
        dp = q[0] - p[0], q[1] - p[1]
        tp = dp[1], -dp[0]
        if aoc.in_range((p[0] + tp[0], p[1] + tp[1]), M.shape):
            R[p[0] + tp[0], p[1] + tp[1]] = -1
        if aoc.in_range((p[0] - tp[0], p[1] - tp[1]), M.shape):
            R[p[0] - tp[0], p[1] - tp[1]] = 1
        if aoc.in_range((p[0] + dp[0] + tp[0], p[1] + dp[1] + tp[1]), M.shape):
            R[p[0] + dp[0] + tp[0], p[1] + dp[1] + tp[1]] = -1
        if aoc.in_range((p[0] + dp[0] - tp[0], p[1] + dp[1] - tp[1]), M.shape):
            R[p[0] + dp[0] - tp[0], p[1] + dp[1] - tp[1]] = 1

    # ------------------------------------------------------------
    # Note: Depending on which direction the path is traversed
    # the sign will be opposite. Run twice with/without "R *= -1"
    # and take whichever produces the lower result.
    #
    # R *= -1
    # ------------------------------------------------------------

    for p in path:
        R[p] = -1

    def adjacencies(p):
        return [tuple(q) for q in aoc.neighbors(p, lim=M.shape) if R[q] == 0]
    y, x = np.where(R==1)
    start = set(zip(list(y), list(x)))
    fill = aoc.search.Path(adjacencies).initial(start).run().visited()
    answer = len(fill)
    print("Part 2: {}".format(answer)) #x


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
