import numpy as np
import aoc

from collections import deque

def run(indata):
    N = int(indata.split()[-2])
    P = int(indata.split()[0])
    
    # ----------- PART 1 -----------
    #
    score = [0] * P
    marbles = deque()
    for i in range(N):
        if i > 0 and i % 23 == 0:
            marbles.rotate(7)
            score[i%P] += i + marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(i)
    answer = max(score)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    score = [0] * P
    marbles = deque()
    for i in range(100 * N):
        if i > 0 and i % 23 == 0:
            marbles.rotate(7)
            score[i%P] += i + marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(i)
    answer = max(score)
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':

    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
