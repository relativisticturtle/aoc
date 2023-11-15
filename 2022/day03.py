import os
import sys

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    R = [(set([i for i in l[:(len(l)//2)]]), set([i for i in l[(len(l)//2):]])) for l in L]
    I = [r[0].intersection(r[1]) for r in R]
    answer = 0
    for i in I:
        assert len(i) == 1
        for _i in i:
            answer += ord(_i) - ord('a') + 1 if _i == _i.lower() else ord(_i) - ord('A') + 27

    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for g in range(len(L)//3):
        r1 = set([i for i in L[3*g + 0]])
        r2 = set([i for i in L[3*g + 1]])
        r3 = set([i for i in L[3*g + 2]])
        for i in r1.intersection(r2).intersection(r3):
            assert len(i) == 1
            for _i in i:
                answer += ord(_i) - ord('a') + 1 if _i == _i.lower() else ord(_i) - ord('A') + 27
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
