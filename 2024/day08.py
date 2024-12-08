import numpy as np
import aoc
import itertools


def run(indata):
    colors = set(list(''.join(indata.splitlines(keepends=False))))
    colors = sorted([c for c in colors if c != '.'])
    M = aoc.points.Set2D.fromtext(indata, colors=colors, ignore_colors='.')
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    M.xlim = (0, len(indata.splitlines(keepends=False)[0]))
    M.ylim = (0, len(indata.splitlines(keepends=False)))
    
    # ----------- PART 1 -----------
    #
    ANs = set()
    for c in M.colors:
        P = np.where(M.values == c)[0]
        #print(P)
        for i1, i2 in itertools.combinations(P, 2):
            #print(i1, i2)
            an1 = 2 * np.array(M.points)[i1] - np.array(M.points)[i2]
            an2 = 2 * np.array(M.points)[i2] - np.array(M.points)[i1]
            if an1[0] >= M.xlim[0] and an1[0] < M.xlim[1] and an1[1] >= M.ylim[0] and an1[1] < M.ylim[1]:
                ANs.add((an1[0], an1[1]))
                print(an1)
            if an2[0] >= M.xlim[0] and an2[0] < M.xlim[1] and an2[1] >= M.ylim[0] and an2[1] < M.ylim[1]:
                ANs.add((an2[0], an2[1]))
                print(an2)
    answer = len(ANs)
    print("Part 1: {}".format(answer)) # x274
    
    # ----------- PART 2 -----------
    #
    ANs = set()
    for c in M.colors:
        P = np.where(M.values == c)[0]
        #print(P)
        for i1, i2 in itertools.combinations(P, 2):
            for x, y in itertools.product(range(M.xlim[0], M.xlim[1]), range(M.ylim[0], M.ylim[1])):
                an = np.array([x, y])
                if np.cross(np.array(M.points)[i1] - an, np.array(M.points)[i2] - an) == 0:
                    ANs.add((an[0], an[1]))
    answer = len(ANs)
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    #indata = get_input(test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
