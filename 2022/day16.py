import os
import sys
import itertools
from collections import deque


def run(indata):
    L = indata.splitlines(keepends=False)

    G = dict()
    VALVE = dict()
    for l in L:
        valve = l.split()[1]
        flow = int(l.split()[4][5:-1])
        try:
            neigh = tuple(l.split('valves ')[1].split(', '))
        except IndexError:
            neigh = tuple(l.split('valve ')[1].split(', '))
        VALVE[valve] = (flow, neigh)
        if flow > 0:
            G[valve] = len(G)

    D = dict()
    for start, stop in itertools.product(VALVE.keys(), G.keys()):
        Q = deque()
        Q.append((start, 0))
        visited = set()
        while len(Q) > 0:
            pos, d = Q.popleft()
            if pos in visited:
                continue
            visited.add(pos)
            if pos == stop:
                D[start, stop] = d
                break
            for n in VALVE[pos][1]:
                Q.append((n, d + 1))

    def calculate_single_worker_visits(max_time):
        record = dict()
        vstatus = (False,) * len(G)
        Q = deque()
        Q.append(('AA', max_time, vstatus, 0))

        while len(Q) > 0:
            pos, remaining, vstatus, value = Q.pop()
            record[vstatus] = max(record.get(vstatus, 0), value)
            for n in G.keys():
                if n == pos:
                    continue
                idxn = G[n]
                new_remaining = remaining - D[pos, n] - 1
                if vstatus[idxn] or new_remaining < 0:
                    continue
                new_vstatus = vstatus[:idxn] + (True,) + vstatus[(idxn+1):]
                Q.append((n, new_remaining, new_vstatus, value + new_remaining * VALVE[n][0]))
        return record

    # ----------- PART 1 -----------
    #
    visits = calculate_single_worker_visits(30)
    answer = max(visits.values())
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    visits = calculate_single_worker_visits(26)
    answer = 0
    for v1, v2 in itertools.combinations(visits.items(), 2):
        if any([p1 and p2 for p1, p2 in zip(v1[0], v2[0])]):
            continue
        answer = max(answer, v1[1] + v2[1])
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc.utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(16, 2022)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
