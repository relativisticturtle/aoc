import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    R = {tuple(map(int,r.split('|'))) for r in L[0]}
    L = [list(map(int, l.split(','))) for l in L[1]]
    
    # ----------- PART 1 -----------
    #
    answer = 0
    for l in L:
        valid = True
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                if (l[j], l[i]) in R:
                    valid = False
                if not valid:
                    break
            if not valid:
                break
        if valid:
            answer += l[len(l)//2]


    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for l in L:
        correction_count = 0
        while True:
            valid = True
            for i in range(len(l)):
                for j in range(i+1, len(l)):
                    if (l[j], l[i]) in R:
                        l_tmp = l[i]
                        l[i] = l[j]
                        l[j] = l_tmp
                        valid = False
                    if not valid:
                        break
                if not valid:
                    break
            if valid:
                break
            correction_count += 1
        if correction_count > 0:
            answer += l[len(l)//2]
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input() #test='test')
    #indata = get_input(test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
