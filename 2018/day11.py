import numpy as np
from scipy.signal import convolve2d
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    serial_no = int(L[0])

    X, Y = np.meshgrid(np.arange(300) + 1, np.arange(300) + 1)
    power_level = (((X + 10) * Y + serial_no) * (X + 10) // 100) % 10 - 5
    
    # ----------- PART 1 -----------
    #
    p33 = convolve2d(power_level, np.ones((3, 3)), 'valid')
    max_idx = np.argmax(p33)
    y_idx, x_idx = np.unravel_index(max_idx, p33.shape)
    answer = str((x_idx + 1, y_idx + 1))
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    max_val = 0
    for i in range(2, 300):
        pxx = convolve2d(power_level, np.ones((i, i)), 'valid')
        max_idx = np.argmax(pxx)
        y_idx, x_idx = np.unravel_index(max_idx, pxx.shape)
        if pxx[y_idx, x_idx] > max_val:
            max_val = pxx[y_idx, x_idx]
            answer = str((x_idx + 1, y_idx + 1, i))
            print("Part 2: {}: {}".format(answer, max_val))

    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':

    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
