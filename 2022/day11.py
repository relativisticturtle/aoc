import os
import sys
import copy
import numpy as np

def run(indata):
    M0 = []
    for m in indata.split('\n\n'):
        D = m.splitlines(keepends=False)
        
        # Items
        items = [int(x) for x in D[1][18:].split(',')]
        
        # Operation
        if 'old * old' in D[2][12:]:
            op = (1, 0, 0)
        elif 'old *' in D[2][12:]:
            op = (0, int(D[2][12:].split('*')[-1]), 0)
        elif 'old +' in D[2][12:]:
            op = (0, 1, int(D[2][12:].split('+')[-1]))
        
        # Action
        action = tuple(int(d.split()[-1]) for d in D[3:6])
        M0.append([items, op, action])

    
    # ----------- PART 1 -----------
    #
    M = copy.deepcopy(M0)
    inspections = [0 for _ in M]
    for r in range(20):
        for m in range(len(M)):
            for item in M[m][0]:
                worry = (
                    M[m][1][0] * item * item +
                    M[m][1][1] * item +
                    M[m][1][2]
                ) // 3
                t = M[m][2][1] if (worry % M[m][2][0]) == 0 else M[m][2][2]
                #print('{} --> {}'.format(worry, t))
                M[t][0].append(worry)
            inspections[m] += len(M[m][0])
            M[m][0] = []
    answer = np.prod(sorted(inspections)[-2:])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    M = copy.deepcopy(M0)
    Q = int(np.prod([M[m][2][0] for m in range(len(M))]))

    inspections = [0 for _ in M]
    for r in range(10000):
        for m in range(len(M)):
            for item in M[m][0]:
                worry = (
                    M[m][1][0] * item * item +
                    M[m][1][1] * item +
                    M[m][1][2]
                ) % Q
                t = M[m][2][1] if (worry % M[m][2][0]) == 0 else M[m][2][2]
                #print('{} --> {}'.format(worry, t))
                M[t][0].append(worry)
            inspections[m] += len(M[m][0])
            M[m][0] = []
    answer = np.prod(np.sort(np.array(inspections)).astype(np.int64)[-2:])
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
