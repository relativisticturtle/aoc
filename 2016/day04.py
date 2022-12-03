import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    
    # ----------- PART 1 -----------
    #
    answer = 0
    for l in L:
        name = ''.join(l.split('-')[:-1])
        chk = l.split('-')[-1].split('[')[-1][:-1]
        idx = int(l.split('-')[-1].split('[')[0])
        letters, counts = np.unique(list(name), return_counts=True)
        try:
            chk_c = [counts[np.where(letters == l)[0][0]] for l in chk]
        except IndexError:
            continue

        decoy = False
        for i in range(4):
            if chk_c[i] < chk_c[i+1] or (chk_c[i] == chk_c[i+1] and chk[i] > chk[i+1]):
                decoy = True
                break
        if not decoy:
            answer += idx
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = None
    for l in L:
        idx = int(l.split('-')[-1].split('[')[0])
        room_name = '-'.join([''.join([chr(((ord(c) + idx - ord('a')) % 26) + ord('a')) for c in word]) for word in l.split('-')[:-1]])
        if room_name == 'northpole-object-storage':
            answer = idx
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
