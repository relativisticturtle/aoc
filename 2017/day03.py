import os
import sys
import numpy as np
import itertools

def run(indata):
    L = indata.splitlines(keepends=False)
    s = int(L[0])
    
    # ----------- PART 1 -----------
    #
    position = np.array([0, 0])
    direction = np.array([0, -1])
    left =  np.array([[0, -1], [1, 0]])
    visited = {(0, 0): 1}
    for c in range(1, s):
        if tuple((left @ direction) + position) not in visited:
            direction = left @ direction
        position += direction
        visited[tuple(position)] = c + 1
    
    answer = abs(position[0]) + abs(position[1])
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    position = np.array([0, 0])
    direction = np.array([0, -1])
    left =  np.array([[0, -1], [1, 0]])
    visited = {(0, 0): 1}
    visited[(0, 0)] = 1
    for c in range(1, s):
        if tuple((left @ direction) + position) not in visited:
            direction = left @ direction
        position += direction
        answer = 0
        for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if tuple(position + [dx, dy]) in visited:
                answer += visited[tuple(position + [dx, dy])]
        visited[tuple(position)] = answer
        if answer > s:
            break
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
