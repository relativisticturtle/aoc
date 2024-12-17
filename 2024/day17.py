import numpy as np
import aoc

def combo(x, A, B, C):
    if x in [0, 1, 2, 3]:
        return x
    elif x == 4:
        return A
    elif x == 5:
        return B
    elif x == 6:
        return C
    else:
        raise RuntimeError

memo = dict()
def go_recu(A, B, C, P, target):
    orig = (A, B, C)
    if orig in memo:
        return memo[orig]
    i = 0
    result = []
    while i+1 < len(P):
        if P[i] == 0:   #adv
            A = A // 2**combo(P[i+1], A, B, C)
        elif P[i] == 1: #bxl
            B = B ^ P[i+1]
        elif P[i] == 2: #bst
            B = combo(P[i+1], A, B, C) % 8
        elif P[i] == 3: #jnz
            if A != 0:
                i = P[i+1]
                continue
        elif P[i] == 4: #bxc
            B = B ^ C
        elif P[i] == 5: #out
            # Code is like this: 5,5,3,0
            #   out cmb(B); jnz(A, 0)
            r = combo(P[i+1], A, B, C) % 8
            if A == 0:
                # Only output, return
                q = str(r) if target.endswith(str(r)) else None
            else:
                q2 = go_recu(A, B, C, P, target)
                if q2 is not None:
                    q = str(r) + q2 if target.endswith(str(r)+ q2) else None
                else:
                    q = None
                #q = str(r) + q2 if q2 is not None and target.endswith(str(r)+ q2) else None
            memo[orig] = q
            return q
        elif P[i] == 6:   #bdv
            B = A // 2**combo(P[i+1], A, B, C)
        elif P[i] == 7:   #cdv
            C = A // 2**combo(P[i+1], A, B, C)
        else:
            raise RuntimeError
        i+=2
    return ''

def go(A, B, C, P, break_if_not_program=False):
    i = 0
    result = []
    while i+1 < len(P):
        if P[i] == 0:   #adv
            A = A // 2**combo(P[i+1], A, B, C)
        elif P[i] == 1: #bxl
            B = B ^ P[i+1]
        elif P[i] == 2: #bst
            B = combo(P[i+1], A, B, C) % 8
        elif P[i] == 3: #jnz
            if P[i+1] == 0:
                pass
                #print('({}, {}, {})'.format(A,B,C))
            if A != 0:
                i = P[i+1]
                continue
        elif P[i] == 4: #bxc
            B = B ^ C
        elif P[i] == 5: #out
            r = combo(P[i+1], A, B, C) % 8
            result.append(r)
            if break_if_not_program:
                if len(result) > len(P):
                    break
                if r != P[len(result)-1]:
                    break
            #print(r)
        elif P[i] == 6:   #bdv
            B = A // 2**combo(P[i+1], A, B, C)
        elif P[i] == 7:   #cdv
            C = A // 2**combo(P[i+1], A, B, C)
        else:
            raise RuntimeError
        i+=2
    return result

def run(indata):
    L = indata.splitlines(keepends=False)
    A = int(L[0].split(': ')[-1])
    B = int(L[1].split(': ')[-1])
    C = int(L[2].split(': ')[-1])
    P = [int(x) for x in L[4].split(': ')[-1].split(',')]

    # ----------- PART 1 -----------
    #
    result = go(A, B, C, P)
    answer = ','.join([str(r) for r in result])
    print("Part 1: {}".format(answer))
    
    # x1,6,3,1,7,2,3,5,6
    # x1,6,3,1,7,2,3,5,6,0
    # return answer
    
    # ----------- PART 2 -----------
    #
    # Memoization + assume "8x PREVIOUS + SOMETHING" yields answer
    prev = 0
    target = ''.join([str(x) for x in P])
    i = 0
    while True:
        result = go_recu(i, B, C, P, target)
        if result == target:
            print('{:16d} : {}'.format(i, result))
            break
        if result is not None and len(result) > prev:
            prev = len(result)
            print('{:16d} : {}'.format(i, result))
            i *= 8
        else:
            i+=1
    answer = i
    print("Part 2: {}".format(answer))
    return answer


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    #indata = get_input(test='test2')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
