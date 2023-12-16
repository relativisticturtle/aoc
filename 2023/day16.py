import aoc

def run(indata):
    S = aoc.points.Set2D.fromtext(indata, './\\-|')
    M = S.image()
    
    # ----------- PART 1 -----------
    #
    def adjacent(p):
        q = []
        if M[p[:2]] == 0:     # .
            q = [(p[0] + p[2], p[1] + p[3], p[2], p[3])]
        elif M[p[:2]] == 1:   # /
            v = (0, 0, -p[3], -p[2])
            q = [(p[0] + v[2], p[1] + v[3], v[2], v[3])]
        elif M[p[:2]] == 2:   # \
            v = (0, 0, p[3], p[2])
            q = [(p[0] + v[2], p[1] + v[3], v[2], v[3])]
        elif M[p[:2]] == 3:   # -
            if p[2] == 0:
                q = [(p[0] + p[2], p[1] + p[3], p[2], p[3])]
            else:
                q = [
                    (p[0] + 0, p[1] - 1, 0, -1),
                    (p[0] + 0, p[1] + 1, 0, +1)
                ]
        elif M[p[:2]] == 4:   # |
            if p[3] == 0:
                q = [(p[0] + p[2], p[1] + p[3], p[2], p[3])]
            else:
                q = [
                    (p[0] - 1, p[1] + 0, -1, 0),
                    (p[0] + 1, p[1] + 0, +1, 0)
                ]
        else:
            raise RuntimeError()

        q = [_q for _q in q if aoc.in_range(_q[:2], M.shape)]
        return q

    search = aoc.search.Path(adjacent).initial((0, 0, 0, 1)).run()
    answer = len(set([p[:2] for p in search.visited()]))
    print("Part 1: {}".format(answer)) #7979
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for c in range(M.shape[1]):
        search = aoc.search.Path(adjacent).initial((0, c, 1, 0)).run()
        a = len(set([p[:2] for p in search.visited()]))
        answer = max(a, answer)
        search = aoc.search.Path(adjacent).initial((M.shape[0]-1, c, -1, 0)).run()
        a = len(set([p[:2] for p in search.visited()]))
        answer = max(a, answer)
        print('Column {} / {} : {}'.format(c + 1, M.shape[1], answer))
    for r in range(M.shape[1]):
        search = aoc.search.Path(adjacent).initial((r, 0, 0, 1)).run()
        a = len(set([p[:2] for p in search.visited()]))
        answer = max(a, answer)
        search = aoc.search.Path(adjacent).initial((r, M.shape[1]-1, 0, -1)).run()
        a = len(set([p[:2] for p in search.visited()]))
        answer = max(a, answer)
        print('Row {} / {} : {}'.format(r + 1, M.shape[0], answer))

    print("Part 2: {}".format(answer)) #8437
    

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
