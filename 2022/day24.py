import os
import sys
import numpy as np
import heapq

def run(indata):
    L = indata.splitlines(keepends=False)
    M = np.array([list(l[1:-1]) for l in L[1:-1]])
    GE = (M == '>')
    GW = (M == '<')
    GN = (M == '^')
    GS = (M == 'v')
    start = L[0].index('.') - 1, -1
    goal = L[-1].index('.') - 1, M.shape[0]
    period = np.lcm(*M.shape)
    
    def map_at(t):
        return (
            np.roll(GE,  t, axis=1) |
            np.roll(GW, -t, axis=1) |
            np.roll(GN, -t, axis=0) |
            np.roll(GS,  t, axis=0)
        )
    
    def potential(x, y, t, dest):
        return abs(dest[0] - x) + abs(dest[1] - y) + t
    
    answer = None

    #from collections import deque
    def go(start, t, goal):
        Q = []
        heapq.heappush(Q, (potential(*start, 0, goal), *start, t))
        V = dict()
        while len(Q) > 0:
            _, x, y, t = heapq.heappop(Q)
            
            # Has visited?
            if (x, y, t % period) in V:
                assert V[x, y, t % period] <= t
                continue
            V[x, y, t % period] = t

            # Start/goal?
            if (x, y) == goal:
                return t
            elif (x, y) == start:
                pass
            #elif x < 0 or x >= M.shape[1] or y < 0 or y >= M.shape[0]:
            elif x < 0 or x >= 120 or y < 0 or y >= 25:
                continue
            elif map_at(t)[y, x]:
                continue

            D = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
            for d in D:
                p = potential(x + d[0], y + d[1], t+1, goal)
                heapq.heappush(Q, (p, x + d[0], y + d[1], t+1))

    # ----------- PART 1 -----------
    #
    answer = go(start, 0, goal)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    t1 = go(goal, answer, start)
    answer = go(start, t1, goal)
    print("Part 2: {}".format(answer))
    

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
