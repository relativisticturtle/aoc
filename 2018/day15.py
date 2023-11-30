import numpy as np
import matplotlib.pyplot as plt
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)

    ge = aoc.points.Set2D.fromtext(L, 'GE', ignore_colors='#.')
    goblins = ge.points[ge.values == 0, :]
    elfs = ge.points[ge.values == 1, :]
    #M = np.array([list(l.replace('E', '.').replace('G', '.')) for l in L])
    M = np.array([list(l) for l in L])


    def adjacencies(p):
        adjacencies = []

        # Break tie by "reading order"
        dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for new_rc in aoc.neighbors(p[:2], dirs):
            if aoc.in_range(new_rc, M.shape) and M[new_rc[0], new_rc[1]] not in ('#', p[2]):
                adjacencies.append((*new_rc, p[2]))
        return adjacencies

    def finished(p):
        return M[p[0], p[1]] in 'GE' and M[p[0], p[1]] != p[2]

    def evolve(M):
        for r in range(M.shape[0]):
            for c in range(M.shape[1]):
                if M[r, c] in 'GE':
                    path = aoc.search.Path(
                        adjacencies,
                        finished=finished
                    ).initial((r, c, M[r, c])).run().path_to()
                    if len(path) == 1:
                        #no more enemies
                        break
                    elif len(path) == 2:
                        #at enemy
                        break
                    else:
                        new_rc = path[2]

    # ----------- PART 1 -----------
    #
    evolve(M)
    answer = ''.join([str(r) for r in R[r_max:(r_max+10)]])
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    print("Part 2: {}".format(answer))


if __name__ == '__main__':
    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
