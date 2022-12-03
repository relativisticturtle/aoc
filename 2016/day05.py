import os
import sys
import hashlib

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    answer = ''
    idx = 0
    while len(answer) < 8:
        code = hashlib.md5((L[0] + str(idx)).encode('utf-8')).hexdigest()
        if code.startswith('00000'):
            answer += code[5]
            print(answer)
        idx += 1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = list('        ')
    idx = 0
    while ' ' in answer:
        code = hashlib.md5((L[0] + str(idx)).encode('utf-8')).hexdigest()
        if code.startswith('00000'):
            if code[5] not in '01234567' or answer[int(code[5])] != ' ':
                idx += 1
                continue
            answer[int(code[5])] = code[6]
            print(''.join(answer))
        idx += 1
    answer = ''.join(answer)
    print("Part 2: {}".format(answer))


if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc_utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
