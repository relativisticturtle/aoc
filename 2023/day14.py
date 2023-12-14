import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    S = aoc.points.Set2D.fromtext(indata, '.#O')
    M = S.image()

    # ----------- PART 1 -----------
    #
    moved = True
    while moved:
        moved = False
        for r in range(1, M.shape[0]):
            for c in range(M.shape[1]):
                if M[r, c] == 2 and M[r-1, c] == 0:
                    M[r-1, c] = 2
                    M[r, c] = 0
                    moved = True

    answer = 0
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            if M[r, c] == 2:
                answer += M.shape[0] - r

    print("Part 1: {}".format(answer)) #108614
    
    # ----------- PART 2 -----------
    #
    def evolve(M):
        M = np.array(M)
        for _ in range(4):
            moved = True
            while moved:
                moved = False
                for r in range(1, M.shape[0]):
                    for c in range(M.shape[1]):
                        if M[r, c] == 2 and M[r-1, c] == 0:
                            M[r-1, c] = 2
                            M[r, c] = 0
                            moved = True
            M = np.rot90(M, 3)
        return tuple(tuple(l) for l in M)

    M = S.image()
    simul = aoc.simul.Evolution(evolve, tuple(tuple(l) for l in M)).run()
    M = np.array(simul.extrapolate(1000000000))
    answer = 0
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            if M[r, c] == 2:
                answer += M.shape[0] - r
    print("Part 2: {}".format(answer)) #96447
    

if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input() #test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
