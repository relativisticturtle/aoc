import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    M = np.array([list(l) for l in indata.splitlines(keepends=False)])
    S = np.where(M == 'S')
    S = S[0][0], S[1][0]
    M[S] = '.'

    def adjancencies(p):
        #if p[2] == 0:
        #    return []
        #n = []
        #for q in aoc.neighbors(p[:2], lim=M.shape):
        #    n.append(q + (p[:2] - 1,))

        return [q for q in aoc.neighbors(p, lim=M.shape) if M[q] == '.']

    # ----------- PART 1 -----------
    #
    search = aoc.search.Path(adjancencies).initial(S).run()
    answer = 0
    for v in search.visited():
        if search.result(v) <= 64 and (search.result(v) % 2 == 0):
            answer += 1
    print("Part 1: {}".format(answer)) # 3716
    


    # ----------- PART 2 -----------
    #
    if False:
        results = []
        for X in [3]:
            print('Calculating for X = {}...'.format(X))
            steps = 65 + 131 * X
            M2 = np.tile(M, (1 + 2*X, 1 + 2*X))
            def adjancencies2(p):
                return [q for q in aoc.neighbors(p, lim=M2.shape) if M2[q] == '.']
            S2 = X * M.shape[0] + S[0], X * M.shape[1] + S[1]
            search2 = aoc.search.Path(adjancencies2).initial(S2).run()

            V = np.zeros(M2.shape, dtype=int)
            results.append(0)
            for v in search2.visited():
                if search2.result(v) <= steps and (search2.result(v) % 2 == (steps % 1)):
                    results[-1] += 1
                    V[v] = 2
                elif search2.result(v) <= steps:
                    V[v] = 2
            print(results[-1])
            import matplotlib.pyplot as plt
            plt.imshow(V)
            plt.show()
        
        print('Fitting 2nd degree polynomial')
        c = results[0]
        a = (results[2] - 2 * results[1] + results[0]) / 2
        b = results[1] - a - c

        answer = a * (202300 / 2)**2 + b * (202300 / 2) + c
        print("Part 2: {}".format(answer))
        return


    # 196 steps : 34009
    h = (M.shape[0] - 1) // 2
    start = {
        'C': (h, h),
        'N': (M.shape[0] - 1, h),
        'E': (h, 0),
        'S': (0, h),
        'W': (h, M.shape[1] - 1),
        'NE': (M.shape[0] - 1, 0),
        'SE': (0, 0),
        'SW': (0, M.shape[1] - 1),
        'NW': (M.shape[0] - 1, M.shape[1] - 1),
        'NE2': (M.shape[0] - 1, 0),
        'SE2': (0, 0),
        'SW2': (0, M.shape[1] - 1),
        'NW2': (M.shape[0] - 1, M.shape[1] - 1),
    }

    tiles = dict()
    for lbl, S in start.items():
        tiles[lbl] = [0, 0]
        search = aoc.search.Path(adjancencies).initial(S).run()
        for v in search.visited():
            if lbl in ['C', 'N', 'E', 'S', 'W'] and search.result(v) <= 130:
                tiles[lbl][search.result(v) % 2] += 1
            elif lbl in ['NE', 'SE', 'SW', 'NW'] and search.result(v) <= 65:
                tiles[lbl][search.result(v) % 2] += 1
            elif lbl in ['NE2', 'SE2', 'SW2', 'NW2'] and search.result(v) <= 196:
                tiles[lbl][search.result(v) % 2] += 1

    steps = 26501365
    assert M.shape[0] == M.shape[1], 'Assumption violated'
    assert (steps - h) % M.shape[0] == 0, 'Assumption violated'
    s = (steps - h) // M.shape[0]

    # Count for every species
    A = tiles['C'][0]                                                   # full, even
    B = tiles['C'][1]                                                   # full, odd
    C = sum([tiles[lbl][0] for lbl in ['N', 'E', 'S', 'W']])            # corners, always even
    D = sum([tiles[lbl][0] for lbl in ['NE', 'SE', 'SW', 'NW']])        # edge small, even
    E = sum([tiles[lbl][1] for lbl in ['NE2', 'SE2', 'SW2', 'NW2']])    # edge large, odd
    
    answer = s**2 * A + (s - 1)**2 * B + s * D + (s-1) * E + C
    print("Part 2: {}".format(answer))
    return


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
