import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    P = [tuple(map(int, l.split(','))) for l in L]
    
    # ----------- PART 1 -----------
    #
    
    # Let first 1024 bytes fall
    M = np.zeros((71, 71))
    for p in P[:1024]:
        M[p] = 1

    def adjacencies(p):
        adj = []
        for d in aoc.D4:
            q = p[0] + d[0], p[1] + d[1]
            if not aoc.in_range(q, M.shape):
                continue
            if M[q] == 0:
                adj.append(q)
        return adj
    
    s = aoc.search.Path(adjacencies).initial({(0,0)}).run()
    answer = s.result((70, 70))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    current_path = s.path_to((70, 70))
    for p in P[1024:]:
        M[p] = 1
        # Only do new path-search if byte falls on
        # previously established path
        if p not in current_path:
            continue
        s = aoc.search.Path(adjacencies).initial({(0,0)}).run()
        if s.result((70, 70)) is None:
            # Finally, no path to exit anymore
            answer = '{},{}'.format(*p)
            break
        current_path = s.path_to((70, 70))
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
