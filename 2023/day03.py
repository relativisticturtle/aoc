import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    # ----------- PART 1 -----------
    #
    labels = []
    for r in range(len(L)):
        c = 0
        p = 0
        x = False
        for c in range(len(L[r]) + 1):
            if c < len(L[r]) and L[r][c] in '0123456789':
                p = 10 * p + int(L[r][c])
                for _rc in aoc.neighbors((r, c), aoc.D8, lim=[len(L), len(L[r])]):
                    if L[_rc[0]][_rc[1]] not in '0123456789.':
                        x = True
            else:
                if x:
                    labels.append(p)
                p = 0
                x = False
            
    answer = sum(labels)
    print("Part 1: {}".format(answer)) # 526404
    
    # ----------- PART 2 -----------
    #
    gears = dict()
    labels = []
    for r in range(len(L)):
        c = 0
        p = 0
        active_gears = []
        for c in range(len(L[r]) + 1):
            if c < len(L[r]) and L[r][c] in '0123456789':
                p = 10 * p + int(L[r][c])
                for _rc in aoc.neighbors((r, c), aoc.D8, lim=[len(L), len(L[r])]):
                    if L[_rc[0]][_rc[1]] == '*':
                        if _rc not in gears:
                            gears[_rc] = []
                        if _rc not in active_gears:
                            active_gears.append(_rc)
            else:
                if len(active_gears) > 0:
                    for _rc in active_gears:
                        gears[_rc].append(p)
                p = 0
                active_gears = []
            
                        
    answer = sum([g[0] * g[1] for g in gears.values() if len(g) == 2])
    print("Part 2: {}".format(answer)) # 84399773
    

if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
