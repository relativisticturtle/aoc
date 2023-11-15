import os
import sys
import numpy as np
import networkx as nx
#from queue import PriorityQueue
#from collections import defaultdict

#from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    G = nx.DiGraph()
    for l in L:
        before = l.split()[1]
        after = l.split()[7]
        G.add_edge(before, after)

    answer = ''
    missing = set([g for g in G.nodes()])
    completed = set()

    while len(missing) > 0:
        to_build = None
        for g in missing:
            ready = all([f[0] in completed for f in G.in_edges(g)])
            if ready and (to_build is None or g < to_build):
                to_build = g
        assert to_build is not None
        missing.remove(to_build)
        completed.add(to_build)
        answer += to_build

    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = ''
    missing = set([g for g in G.nodes()])
    completed = set()
    inprogress = dict()
    steps = 0
    while len(missing) > 0 or len(inprogress) > 0:
        while len(inprogress) < 5:
            to_build = None
            for g in missing:
                ready = all([f[0] in completed for f in G.in_edges(g)])
                if ready and (to_build is None or g < to_build):
                    to_build = g
            if to_build is not None:
                missing.remove(to_build)
                inprogress[to_build] = ord(to_build) - ord('A') + 61
            else:
                break
        
        assert len(inprogress) > 0
        for g in sorted(inprogress.keys()):
            inprogress[g] -= 1
            if inprogress[g] == 0:
                inprogress.pop(g)
                completed.add(g)
                answer += g
        steps += 1
    answer = steps
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc.utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
