import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)

    # ----------- PART 1 -----------
    #
    p = (0, 0)
    v = {'U': (-1, 0), 'L': (0, -1), 'D': (1, 0), 'R': (0, 1)}
    points = []
    for l in L:
        w = v[l.split()[0]]
        s = int(l.split()[1])
        for _ in range(s):
            p = (p[0] + w[0], p[1] + w[1])
            points.append(p)

    points = np.array(points)
    M = aoc.points.Set2D(points[:, 1], points[:, 0]).image()

    def adjacencies(p):
        return [tuple(q) for q in aoc.neighbors(p, lim=M.shape) if M[q] == 0]
    fill = aoc.search.Path(adjacencies).initial((M.shape[0]//2, M.shape[0]//2)).run().visited()
    for p in fill:
        M[p] = 2

    #import matplotlib.pyplot as plt
    #plt.imshow(M)
    #plt.show()
    answer = np.sum(M > 0)
    print("Part 1: {}".format(answer)) # 67891
    
    # ----------- PART 2 -----------
    #
    p = (0, 0)
    v = {'3': (-1, 0), '2': (0, -1), '1': (1, 0), '0': (0, 1)}
    points = [p]
    rim = 0
    for l in L:
        w = v[l[-2]]
        s = int(l.split()[-1][2:-2], 16)
        p = (p[0] + s * w[0], p[1] + s * w[1])
        points.append(p)
        rim += s

    # Shoelace formula
    area2x = 0
    for i in range(1, len(points)):
        area2x += points[i-1][0] * points[i][1] - points[i-1][1] * points[i][0]
    
    # Shoelace-area will take
    #  - half of the rim: edge passes straight through
    #  - minus 1: left/right turns splits on average half,
    #             except that there are +4 inwards turn that
    #             contribute together +1 rather than +2.
    # Thus:
    #     shoelace area = total area - rim / 2 - 1
    answer = 1 + rim // 2 + abs(area2x) // 2
    print("Part 2: {}".format(answer)) # 94116351948493
    

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
