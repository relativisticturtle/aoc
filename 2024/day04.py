import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    M = np.array([list(l) for l in L])

    x = M == 'X'
    m = M == 'M'
    a = M == 'A'
    s = M == 'S'
    
    # ----------- PART 1 -----------
    #
    c_e = np.sum(x[:, :-3] * m[:, 1:-2] * a[:, 2:-1] * s[:, 3:])
    c_w = np.sum(s[:, :-3] * a[:, 1:-2] * m[:, 2:-1] * x[:, 3:])
    c_s = np.sum(x[:-3, :] * m[1:-2, :] * a[2:-1, :] * s[3:, :])
    c_n = np.sum(s[:-3, :] * a[1:-2, :] * m[2:-1, :] * x[3:, :])
    c_se = np.sum(x[:-3, :-3] * m[1:-2, 1:-2] * a[2:-1, 2:-1] * s[3:, 3:])
    c_nw = np.sum(s[:-3, :-3] * a[1:-2, 1:-2] * m[2:-1, 2:-1] * x[3:, 3:])
    c_ne = np.sum(x[3:, :-3] * m[2:-1, 1:-2] * a[1:-2, 2:-1] * s[:-3, 3:])
    c_sw = np.sum(s[3:, :-3] * a[2:-1, 1:-2] * m[1:-2, 2:-1] * x[:-3, 3:])
    answer = c_e+c_w+c_s+c_n+c_se+c_nw+c_ne+c_sw
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    diag1 = (
        m[:-2, :-2] * a[1:-1, 1:-1] * s[2:, 2:] + 
        s[:-2, :-2] * a[1:-1, 1:-1] * m[2:, 2:]
    )
    diag2 = (
        m[2:, :-2] * a[1:-1, 1:-1] * s[:-2, 2:] + 
        s[2:, :-2] * a[1:-1, 1:-1] * m[:-2, 2:]
    )
    # 478
    answer = np.sum(diag1 * diag2)
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
