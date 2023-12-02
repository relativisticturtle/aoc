import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    
        #print(g)
    
    # ----------- PART 1 -----------
    #
    answer = 0
    for i, l in enumerate(L):
        g = [{x.split()[1]: int(x.split()[0]) for x in s.split(',')} for s in l.split(':')[1].split(';')]
        for _g in g:
            if _g.get('red', 0) > 12 or _g.get('green', 0) > 13 or _g.get('blue', 0) > 14:
                break
        else:
            answer += i+1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for i, l in enumerate(L):
        g = [{x.split()[1]: int(x.split()[0]) for x in s.split(',')} for s in l.split(':')[1].split(';')]
        m = {'red': 0, 'green': 0, 'blue': 0}
        for _g in g:
            for c, n in _g.items():
                m[c] = max(m[c], n)
        answer += m['red'] * m['green'] * m['blue']
    print("Part 2: {}".format(answer))
    

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
