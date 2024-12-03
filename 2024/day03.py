import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    L = ''.join(L)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    # ----------- PART 1 -----------
    #
    answer = 0
    i = 0
    while i < len(L):
        i = L.find('mul(', i)
        if i < 0:
            break
        try:
            j = L.find(',', i + 4)
            k = L.find(')', j + 1)
            a = int(L[i+4:j])
            b = int(L[j+1:k])
            answer += a*b
            i = k + 1
        except ValueError:
            #print('!!!! mul({}, {})'.format(L[i+4:j], L[j+1:k], a*b))
            i = i + 1

    # 173731097
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    enable = True
    i = 0
    while i < len(L):
        j = L.find('do()', i)
        k = L.find('don\'t()', i)
        i = L.find('mul(', i)
        if j >= 0 and j < i and (j < k or k < 0):
            i = j + 1
            enable = True
            continue
        if k >= 0 and k < i and (k < j or j < 0):
            i = k + 1
            enable = False
            continue
        if i < 0:
            break
        try:
            j = L.find(',', i + 4)
            k = L.find(')', j + 1)
            a = int(L[i+4:j])
            b = int(L[j+1:k])
            answer += a*b if enable else 0
            i = k + 1
        except ValueError:
            #print('!!!! mul({}, {})'.format(L[i+4:j], L[j+1:k], a*b))
            i = i + 1
    
    # x93572208
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
