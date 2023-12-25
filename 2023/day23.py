import numpy as np
import aoc

def run(indata):
    M = np.array([list(line) for line in indata.splitlines(keepends=False)])

    # Get all branches
    branches = []
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            if M[r, c] == '#':
                continue
            if len([q for q in aoc.neighbors((r, c), lim=M.shape) if M[q] != '#']) > 2:
                branches.append((r, c))
    # include start/stop
    branches = [(0, 1)] + branches + [(M.shape[0] - 1, M.shape[1] - 2)]

    # Find branch-to-branch reachability
    def generate_graph(slippery=True):
        G = []
        for b in branches:
            reachable = []
            def adjacencies(p):
                if p in branches:
                    reachable.append(p)
                    return []
                if slippery:
                    if M[p] == '>':
                        return [(p[0], p[1] + 1)]
                    elif M[p] == '<':
                        return [(p[0], p[1] - 1)]
                    elif M[p] == '^':
                        return [(p[0] - 1, p[1])]
                    elif M[p] == 'v':
                        return [(p[0] + 1, p[1])]
                return [q for q in aoc.neighbors(p, lim=M.shape) if M[q] != '#']
        
            start = {q: 1 for q in aoc.neighbors(b, lim=M.shape) if M[q] != '#'}
            search = aoc.search.Path(adjacencies).initial(start).run()
            G.append({branches.index(r): search.result(r) for r in reachable if r != b})
        return G

    # ----------- PART 1 -----------
    #
    G = generate_graph(slippery=True)

    from collections import deque
    Q = deque()
    Q.append((0, 0))
    visited = dict()
    while len(Q) > 0:
        i, c = Q.popleft()
        if i not in visited or visited[i] < c:
            visited[i] = c
        for j, dc in G[i].items():
            Q.append((j, c + dc))
    answer = visited[len(G)-1]
    print("Part 1: {}".format(answer)) #2070

    # ----------- PART 2 -----------
    #
    G = generate_graph(slippery=False)

    def search(i, cost, visited):
        if i == len(G) - 1:
            return cost
        visited.add(i)
        best = 0
        for j, c in G[i].items():
            if j not in visited:
                best = max(best, search(j, cost+c, visited.copy()))
        return best

    answer = search(0, 0, set())
    print("Part 2: {}".format(answer)) #6498


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
