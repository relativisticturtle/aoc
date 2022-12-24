import os
import sys
import numpy as np
import time

def run(indata):
    L = indata.splitlines(keepends=False)

    B = []
    # ORE
    # CLAY
    # OBSIDIAN
    # GEODE
    for l in L:
        c = [r.split('costs ')[-1] for r in l.split(':')[-1].split('.')[:-1]]
        C = np.zeros((4, 3), dtype=int)
        C[0, 0] = int(c[0].split()[0])
        C[1, 0] = int(c[1].split()[0])
        C[2, 0] = int(c[2].split()[0])
        C[2, 1] = int(c[2].split()[3])
        C[3, 0] = int(c[3].split()[0])
        C[3, 2] = int(c[3].split()[3])
        B.append(C)

    def potential(R, X, t, C):
        if t == 0:
            return X[3]

        # Find upper limit on every produce below.

        # Max ore robots (special because produces its own consumption).
        # Iterate until steady state is achieved.
        max_ore_robots = R[0] + np.arange(t)
        mor = -np.ones_like(max_ore_robots)
        while np.any(mor != max_ore_robots):
            mor = max_ore_robots
            max_ore = X[0] + np.cumsum(max_ore_robots)
            max_ore_robots = R[0] + np.min([np.arange(t), max_ore // C[0, 0]], axis=0)
        
        # Max clay robots
        max_clay_robots = R[1] + np.min([np.arange(t), max_ore // C[1, 0]], axis=0)
        max_clay = X[1] + np.cumsum(max_clay_robots)
        
        # Max obsidian
        max_obsi_robots = R[2] + np.min([np.arange(t), max_ore // C[2, 0], max_clay // C[2, 1]], axis=0)
        max_obsi = X[2] + np.cumsum(max_obsi_robots)

        # Max geod
        max_geod_robots = R[3] + np.min([np.arange(t), max_ore // C[3, 0], max_obsi // C[3, 2]], axis=0)
        max_geod = X[3] + np.cumsum(max_geod_robots)
        return max_geod[-1]

    def calculate_optimal(R, X, t, C, record, optimal=0):
        if t == 0:
            return X[3]

        # Check if we have already analyzed this scenario (or a better)?
        if R in record:
            for Xt in record[R]:
                if all([a <= b for a, b in zip(X + (t,), Xt)]):
                    return -1
            record[R].append(X + (t,))
        else:
            record[R] = [X + (t,)]

        # Check if already hopeless to beat the optimum?
        if potential(R, X, t, C) <= optimal:
            return -1

        # Make a list of options
        candidates = []
        for i in range(4):
            Y = tuple(x - c for x, c in zip(X[:-1], C[i])) + (X[-1],)
            if all([x >= 0 for x in Y]):
                _X = tuple(y + r for y, r in zip(Y, R))
                _R = R[:i] + (R[i] + 1,) + R[(i+1):]
                p = potential(_R, _X, t-1, C)
                if p > optimal:
                    candidates.append((max(p, 1), _R[::-1], _R, _X, t-1))
        # Remember the trivial "make 0 robots" scenario
        _X = tuple(x + r for x, r in zip(X, R))
        p = potential(R, _X, t-1, C)
        if p > optimal:
            candidates.append((max(p, 1), R[::-1], R, _X, t-1))
        
        # Sort by potential (A-star)
        for _, _, _R, _X, _t in sorted(candidates, reverse=True):
            optimal = max(optimal, calculate_optimal(_R, _X, _t, C, record, optimal))

        return optimal

    # ----------- PART 1 -----------
    #
    T0 = time.time()
    geodes = []
    for i, C in enumerate(B):
        g = calculate_optimal((1, 0, 0, 0), (0, 0, 0, 0), 24, C, {})
        print('{}: {}'.format(i + 1, g))
        geodes.append(g)
    print(geodes)
    answer = sum([g * (i + 1) for i, g in enumerate(geodes)]) 
    print("Part 1: {}  ({:.2f} s)".format(answer, time.time() - T0))
    
    # ----------- PART 2 -----------
    #
    T0 = time.time()
    geodes = []
    for i, C in enumerate(B[:3]):
        g = calculate_optimal((1, 0, 0, 0), (0, 0, 0, 0), 32, C, {})
        print('{}: {}'.format(i + 1, g))
        geodes.append(g)
    print(geodes)
    answer = np.prod(geodes)
    print("Part 2: {}  ({:.2f} s)".format(answer, time.time() - T0))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc_utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
