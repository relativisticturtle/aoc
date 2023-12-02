import numpy as np
import matplotlib.pyplot as plt
import aoc

# Idea 1:
#  - Map-structure. Only operate on map
#  - Simple to setup, but with issues
#    - Book-keep HP, and order

# Idea 2:
#  - Dict: walls, elves, goblins
#  - Keys are positions, values are HP


def run(indata):
    L = indata.splitlines(keepends=False)

    ge = aoc.points.Set2D.fromtext(L, '#GE', ignore_colors='.')
    walls = {tuple(p)[::-1] for p in ge.points[ge.values == 0, :]}
    goblins = {tuple(p)[::-1]: 200 for p in ge.points[ge.values == 1, :]}
    elves = {tuple(p)[::-1]: 200 for p in ge.points[ge.values == 2, :]}

    def adjacencies(p):
        adjacencies = []
        # Break tie by "reading order"
        dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for q in aoc.neighbors(p[:2], dirs):
            if p[2] == 'E' and (q not in walls and q not in elves):
                adjacencies.append((*q, p[2]))
            elif p[2] == 'G' and (q not in walls and q not in goblins):
                adjacencies.append((*q, p[2]))
        return adjacencies

    def finished(p):
        if p[2] == 'E' and p[:2] in goblins:
            return True
        elif p[2] == 'G' and p[:2] in elves:
            return True
        else:
            return False

    def evolve():
        update_order = sorted(list(elves.keys()) + list(goblins.keys()))

        for p in update_order:
            if p in elves:
                P = 'E'
            elif p in goblins:
                P = 'G'
            else:
                continue
            path = aoc.search.Path(
                adjacencies,
                finished=finished
            ).initial((*p, P)).run().path_to()
            if path is None:
                #no more enemies or unreachable
                continue

            if len(path) > 2:
                # Not yet at enemy
                q = path[1][:2]
                if q in elves or q in goblins:
                    print('error')
                if P == 'E':
                    elves[q] = elves.pop(p)
                    print('E ({:2d}, {:2d})  -->  ({:2d}, {:2d})'.format(p[0], p[1], *q))
                else:
                    print('G ({:2d}, {:2d})  -->  ({:2d}, {:2d})'.format(p[0], p[1], *q))
                    goblins[q] = goblins.pop(p)
                p = q

            # choose weakest in range
            Q = []
            dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for q in aoc.neighbors(p[:2], dirs):
                if P == 'E' and q in goblins:
                    Q.append((goblins[q], q))
                elif P == 'G' and q in elves:
                    Q.append((elves[q], q))

            if len(Q) > 0:
                q = sorted(Q)[0][1]

                # deal attack
                if q in elves:
                    elves[q] -= 3
                    if elves[q] <= 0:
                        elves.pop(q)
                elif q in goblins:
                    goblins[q] -= 3
                    if goblins[q] <= 0:
                        goblins.pop(q)
                
        print('-------------------' + str(goblins.values()))

    # ----------- PART 1 -----------
    #
    rounds = 0
    while len(goblins) > 0 and len(elves) > 0:
        evolve()
        rounds += 1
    answer = sum(goblins.values()) * rounds
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    print("Part 2: {}".format(answer))


if __name__ == '__main__':
    # Get input data
    indata = aoc.get_input(test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
