import numpy as np
import aoc
from collections import defaultdict

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    M = np.array([list(l) for l in L])
    
    def adjacencies(node):
        adj = []
        for d in aoc.D4:
            if node[0] + d[0] < 0 or node[0] + d[0] >= M.shape[0]:
                continue
            if node[1] + d[1] < 0 or node[1] + d[1] >= M.shape[1]:
                continue
            if M[node[0] + d[0], node[1] + d[1]] == M[node[0], node[1]]:
                adj.append((node[0] + d[0], node[1] + d[1]))
        return adj
    
    # ----------- PART 1 & 2 -----------
    #
    answer1 = 0
    answer2 = 0
    visited = set()
    areas = defaultdict(list)
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            if (r, c) in visited:
                continue
            s = aoc.search.Path(adjacencies).initial({(r, c)}).run()
            area = len(s.visited())
            fence = 0
            fence_set = set()
            for node in s.visited():
                for d in aoc.D4:
                    if node[0] + d[0] < 0 or node[0] + d[0] >= M.shape[0]:
                        fence += 1
                        fence_set.add((node[0] + 0.25 * d[0], node[1] + 0.25 * d[1]))
                    elif node[1] + d[1] < 0 or node[1] + d[1] >= M.shape[1]:
                        fence += 1
                        fence_set.add((node[0] + 0.25 * d[0], node[1] + 0.25 * d[1]))
                    elif M[node[0] + d[0], node[1] + d[1]] != M[node[0], node[1]]:
                        fence += 1
                        fence_set.add((node[0] + 0.25 * d[0], node[1] + 0.25 * d[1]))
            answer1 += area * fence
            for f in fence_set:
                if (f[0] + 1, f[1]) in fence_set:
                    fence -= 1
                if (f[0], f[1] + 1) in fence_set:
                    fence -= 1
            answer2 += area * fence
            areas[M[r, c]].append((area, fence))
            visited = visited.union(s.visited())
            
    print("Part 1: {}".format(answer1))
    print("Part 2: {}".format(answer2))


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    #indata = get_input(test='test2')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
