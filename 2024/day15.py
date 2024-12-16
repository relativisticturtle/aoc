import numpy as np
import aoc


def run(indata):
    #L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    P = aoc.points.Set2D.fromtext(indata.split('\n\n')[0], colors='.#O@')
    D = indata.split('\n\n')[1].replace('\n', '')
    #M.print()
    
    # ----------- PART 1 -----------
    #
    M = P.image()
    y, x = np.where(M==3)
    p = y[0], x[0]
    M[p] = 0

    def attempt_move(p, d):
        d = {
            '>': (0, 1),
            '<': (0, -1),
            '^': (-1, 0),
            'v': (1, 0),
        }[d]
        
        i=0
        while True:
            i = i+1
            pi = p[0] + i * d[0], p[1] + i * d[1]
            if not aoc.misc.in_range(pi, M.shape):
                return p
            elif M[pi] == 1: # wall
                return p
            elif M[pi] == 0 and i == 1: # empty, no boxes
                return pi
            elif M[pi] == 0 and i > 1: # empty, with boxes
                M[pi] = 2
                p = p[0] + 1 * d[0], p[1] + 1 * d[1]
                M[p] = 0
                return p
            else:
                assert M[pi] == 2

    for d in D:
        p = attempt_move(p, d)
        M2 = M.copy()
        M2[p] = 3
        #print(d)
        #print('\n'.join([''.join(row) for row in np.array(['.', '#', 'O', '@'])[M2]]))
        #print()
    
    answer = 0
    for y in range(M.shape[0]):
        for x in range(M.shape[1]):
            if M[y, x] == 2:
                answer += 100 * y + x
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    indata2 = indata.split('\n\n')[0].replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    P = aoc.points.Set2D.fromtext(indata2, colors='.#[]@')
    M = P.image()
    y, x = np.where(M==4)
    p = y[0], x[0]
    M[p] = 0

    def attempt_move2(p, d):
        d = {
            '>': (0, 1),
            '<': (0, -1),
            '^': (-1, 0),
            'v': (1, 0),
        }[d]


        def adjancencies(q):
            if M[q] in (0, 1): # empty / wall
                return ()
            elif d[1] in (-1, 1):
                return ((q[0] + 1 * d[0], q[1] + 1 * d[1]),)
            elif d[0] in (-1, 1):
                if M[q] == 2:  # [
                    return (
                        (q[0] + 1 * d[0], q[1] + 1 * d[1]),
                        (q[0] + 1 * d[0], q[1] + 1 * d[1] + 1),
                        (q[0], q[1] + 1)
                    )
                elif M[q] == 3:  # [
                    return (
                        (q[0] + 1 * d[0], q[1] + 1 * d[1] - 1),
                        (q[0] + 1 * d[0], q[1] + 1 * d[1]),
                        (q[0], q[1] - 1)
                    )
                assert M[q] in (2, 3)
                return ()
            else:
                print('!!!')

        s = aoc.search.Path(adjancencies).initial({(p[0] + d[0], p[1] + d[1])}).run()
        immovable = False
        for q in s.visited():
            if M[q] == 1:
                immovable = True
                break
        if immovable:
            return p
        M2 = M.copy()
        for q in s.visited():
            if q == p:
                continue
            #M[q[0] + d[0], q[1] + d[1]] = M2[q]
            if (q[0] - d[0], q[1] - d[1]) not in s.visited():
                M[q] = 0
            else:
                M[q] = M2[q[0] - d[0], q[1] - d[1]]
        return p[0] + d[0], p[1] + d[1]

    for d in D:
        p = attempt_move2(p, d)
        M2 = M.copy()
        M2[p] = 4
        #print(d)
        #print('\n'.join([''.join(row) for row in np.array(['.', '#', '[', ']', '@'])[M2]]))
        #print()

    answer = 0
    for y in range(M.shape[0]):
        for x in range(M.shape[1]):
            if M[y, x] == 2:
                answer += 100 * y + x
    print("Part 2: {}".format(answer))
    return answer


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
