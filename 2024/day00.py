import numpy as np
import aoc


def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    # ----------- PART 1 -----------
    #
    answer = None
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    #answer = None
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




# ----- Searching -----
# def adjacencies(node):
#     return [(node[0] + d[0], node[1] + d[1]) for d in aoc.D4]
# start_node = (0, 0)
# search = aoc.search.Path(adjacencies).initial({start_node}).run()
# search.result()
# answer = max([search.result(p) for p in search.visited()])


# ----- (Sparse) 2D map of points -----
# M = aoc.points.Set2D.fromtext(indata, colors='.#O')
# for p in M.points:
#     x, y = p
# M.print()
# M_full = M.image(xlim=(-1, 11), ylim=(-2, 12))


# ----- Evolution -----
# def evolve(state):
#     new_state = (state + 1) % 10000
#     return new_state
# simul = aoc.simul.Evolution(evolve, initial_state=0).run()
# state99999 = simul.extrapolate(99999)


# ----- Shoelace formula (polygon area) -----
# > See 2023/day18.py
