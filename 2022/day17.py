import os
import sys
import numpy as np

def run(indata):
    L = indata.splitlines(keepends=False)
    J = L[0]

    R = [
        np.array([
            [1, 1, 1, 1]
        ], dtype=int),
        np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ], dtype=int),
        np.array([
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 1],
        ], dtype=int),
        np.array([
            [1],
            [1],
            [1],
            [1],
        ], dtype=int),
        np.array([
            [1, 1],
            [1, 1],
        ], dtype=int),
    ]
    
    # ----------- PART 1 -----------
    #
    #J = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    M = np.zeros((5000, 7), dtype=int)
    top = 0
    time = 0
    for r in range(2022):
        rock = R[r % 5]
        x = 2
        y = M.shape[0] - top - 4
        
        while True:
            jet = J[time % len(J)]
            time += 1
            # Sideways movement
            if jet == '>' and x + rock.shape[1] < M.shape[1]:
                if not np.any(rock & M[(y - rock.shape[0] + 1):(y + 1), (x+1):(x + rock.shape[1] + 1)]):
                    x += 1
            elif jet == '<' and x > 0:
                if not np.any(rock & M[(y - rock.shape[0] + 1):(y + 1), (x-1):(x + rock.shape[1] - 1)]):
                    x -= 1
            
            # Down movement
            if y + 1 == M.shape[0] or np.any(rock & M[(y - rock.shape[0] + 2):(y + 2), x:(x + rock.shape[1])]):
                M[(y - rock.shape[0] + 1):(y + 1), x:(x + rock.shape[1])] |= rock
                top = max(top, M.shape[0] - y + rock.shape[0] - 1)
                
                #for l in M[M.shape[0] - top - 1:, :]:
                #    print(''.join(['.#'[q] for q in l]))
                #print('-------\n')
                break
            else:
                y += 1
            

    answer = top
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    history = dict()
    history_top = []
    answer = None
    M = np.zeros((5000, 7), dtype=int)
    top = 0
    time = 0
    answer = None
    for r in range(2022):
        if answer:
            break
        rock = R[r % 5]
        x = 2
        y = M.shape[0] - top - 4
        
        while True:
            jet = J[time % len(J)]
            time += 1
            # Sideways movement
            if jet == '>' and x + rock.shape[1] < M.shape[1]:
                if not np.any(rock & M[(y - rock.shape[0] + 1):(y + 1), (x+1):(x + rock.shape[1] + 1)]):
                    x += 1
            elif jet == '<' and x > 0:
                if not np.any(rock & M[(y - rock.shape[0] + 1):(y + 1), (x-1):(x + rock.shape[1] - 1)]):
                    x -= 1
            
            # Down movement
            if y + 1 == M.shape[0] or np.any(rock & M[(y - rock.shape[0] + 2):(y + 2), x:(x + rock.shape[1])]):
                M[(y - rock.shape[0] + 1):(y + 1), x:(x + rock.shape[1])] |= rock
                top = max(top, M.shape[0] - y + rock.shape[0] - 1)
                history_top.append(top)
                
                if top > 100:
                    q = (r % 5,) + tuple(M[(M.shape[0] - top - 1):(M.shape[0] + 100 - top), :].reshape(-1))
                    if q in history:
                        _, h0, r0 = history[q]
                        dh = top - h0
                        dr = r - r0
                        cycles = (1000000000000 - r0) // dr
                        residual = (1000000000000 - r0) % dr
                        answer = cycles * dh + history_top[r0 + residual - 1]
                    else:
                        history[q] = time, top, r
                break
            else:
                y += 1
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
