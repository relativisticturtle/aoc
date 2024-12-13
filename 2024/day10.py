import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    M = np.array([[int(x) for x in l] for l in L])

    def adjacencies(node):
        if M[node[0], node[1]] == 9:
            return []
        adj = []
        for d in aoc.D4:
            n = (node[0] + d[0], node[1] + d[1])
            if n[0] < 0 or n[0] >= M.shape[0]:
                continue
            if n[1] < 0 or n[1] >= M.shape[1]:
                continue
            if M[n[0], n[1]] == M[node[0], node[1]] + 1:
                adj.append(n)
        return adj

    # ----------- PART 1 -----------
    #
    answer = 0
    for start in zip(*np.where(M==0)):
        s = aoc.search.Path(adjacencies).initial({start}).run()
        for v in s.visited():
            if M[v[0], v[1]] == 9:
                answer += 1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    def go(node):
        if M[node[0], node[1]] == 9:
            return 1
        return sum([go(n) for n in adjacencies(node)])

    answer = 0
    for start in zip(*np.where(M==0)):
        answer += go(start)

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
