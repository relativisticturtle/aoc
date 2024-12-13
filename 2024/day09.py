import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    L[0] = L[0] + '0'
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    
    # ----------- PART 1 -----------
    #
    M = []
    for id, (i, j) in enumerate(zip(L[0][::2], L[0][1::2])):
        for _ in range(int(i)):
            M.append(int(id))
        for _ in range(int(j)):
            M.append(-1)
    
    startj = 0
    for i in range(len(M)-1, -1, -1):
        if M[i] == -1:
            continue
        for j in range(startj, i):
            if M[j] == -1:
                M[j] = M[i]
                M[i] = -1
                break
            elif j == startj:
                startj += 1
    answer = 0
    for i, id in enumerate(M):
        if id == -1:
            continue
        answer += i * id
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    M = []
    for id, (i, j) in enumerate(zip(L[0][::2], L[0][1::2])):
        for _ in range(int(i)):
            M.append(int(id))
        for _ in range(int(j)):
            M.append(-1)
    
    startj = 0
    i = len(M)
    while i > 0:
        i -= 1
        while i>0 and M[i-1] == M[i]:
            i-=1
        if M[i] == -1:
            continue
        for j in range(startj, i):
            if M[j] == -1:
                s = 1
                moveable = False
                while i+s < len(M):
                    if M[i + s] != M[i]:
                        moveable = True
                        break
                    if M[j + s] != -1:
                        break
                    s+=1
                if moveable or i+s == len(M):
                    M[j:(j+s)] = M[i:(i+s)]
                    M[i:(i+s)] = [-1] * s
                    break
            elif j == startj:
                startj += 1
    answer = 0
    for i, id in enumerate(M):
        if id == -1:
            continue
        answer += i * id
    print("Part 2: {}".format(answer))
    return answer


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
