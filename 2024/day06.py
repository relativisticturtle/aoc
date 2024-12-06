import numpy as np
import aoc


def run(indata):
    M = aoc.points.Set2D.fromtext(indata, colors='#v>^<', ignore_colors='.')
    W = set(tuple(p) for i, p in enumerate(M.points) if M.values[i] == 0)

    assert np.sum(M.values != 0) == 1
    i0 = np.where(M.values == 1)[0]
    i1 = np.where(M.values == 2)[0]
    i2 = np.where(M.values == 3)[0]
    i3 = np.where(M.values == 4)[0]
    if len(i0) == 1:
        g0 = (M.points[i0[0]][0], M.points[i0[0]][1], 0)
    elif len(i1) == 1:
        g0 = (M.points[i1[0]][0], M.points[i1[0]][1], 1)
    elif len(i2) == 1:
        g0 = (M.points[i2[0]][0], M.points[i2[0]][1], 2)
    elif len(i3) == 1:
        g0 = (M.points[i3[0]][0], M.points[i3[0]][1], 3)

    def evolve(g):
        new_p = (g[0] + aoc.D4[g[2]][0], g[1] + aoc.D4[g[2]][1])
        if new_p in W:
            return (g[0], g[1], (g[2] - 1) % 4)
        else:
            if new_p[0] < M.xlim[0] or new_p[0] >= M.xlim[1]:
                return g
            if new_p[1] < M.ylim[0] or new_p[1] >= M.ylim[1]:
                return g
            return (new_p[0], new_p[1], g[2])

    # ----------- PART 1 -----------
    #
    simul = aoc.simul.Evolution(evolve, initial_state=g0).run()

    visited = set()
    for h in simul._history:
        visited.add(h[:2])
    answer = len(visited)
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    answer = 0
    W_orig = W.copy()
    for obst in visited:
        if obst == g0[:2]:
            continue
        W = W_orig.union({obst})
        simul = aoc.simul.Evolution(evolve, initial_state=g0).run()
        if simul._history[-1] != simul._history[-2]:
            answer += 1
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
