import os
import sys


def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    def desnafu(s):
        c = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
        result = 0
        for i, x in enumerate(s[::-1]):
            result += 5**i * c[x]
        return result
    
    def snafu(r):
        result = ''
        while r > 0:
            s = ((r + 2) % 5) - 2
            if s >= 0:
                result = str(s) + result
            elif s == -1:
                result = '-' + result
            elif s == -2:
                result = '=' + result
            assert (r - s) % 5 == 0
            r = (r - s) // 5
        return result

    answer = snafu(sum(desnafu(x) for x in L))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = None
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
