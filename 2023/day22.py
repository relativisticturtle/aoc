import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    B = [[[int(x) for x in e.split(',')] for e in l.split('~')] for l in indata.splitlines(keepends=False)]
    B = sorted(B, key=lambda b: min(b[0][2], b[1][2]))
    B = np.array(B)
    def fall_down(i):
        minz = min(B[i, 0, 2], B[i, 1, 2])
        xlim = sorted([B[i, 0, 0], B[i, 1, 0]])
        ylim = sorted([B[i, 0, 1], B[i, 1, 1]])

        supports = []
        for j in range(len(B)):
            if j == i:
                continue
            _maxz = max(B[j, 0, 2], B[j, 1, 2])
            _xlim = sorted([B[j, 0, 0], B[j, 1, 0]])
            _ylim = sorted([B[j, 0, 1], B[j, 1, 1]])

            x_ix = max(xlim[0], _xlim[0]), min(xlim[1], _xlim[1])
            y_ix = max(ylim[0], _ylim[0]), min(ylim[1], _ylim[1])

            if _maxz < minz and x_ix[1] >= x_ix[0] and y_ix[1] >= y_ix[0]:
                supports.append((j, minz - _maxz - 1))
        return supports

    def supported(i):
        minz = min(B[i, 0, 2], B[i, 1, 2])
        if minz == 0:
            return [-1]

        xlim = sorted([B[i, 0, 0], B[i, 1, 0]])
        ylim = sorted([B[i, 0, 1], B[i, 1, 1]])

        supports = []
        for j in range(len(B)):
            if j == i:
                continue
            _maxz = max(B[j, 0, 2], B[j, 1, 2])
            _xlim = sorted([B[j, 0, 0], B[j, 1, 0]])
            _ylim = sorted([B[j, 0, 1], B[j, 1, 1]])

            x_ix = max(xlim[0], _xlim[0]), min(xlim[1], _xlim[1])
            y_ix = max(ylim[0], _ylim[0]), min(ylim[1], _ylim[1])

            if _maxz + 1 == minz and x_ix[1] >= x_ix[0] and y_ix[1] >= y_ix[0]:
                supports.append(j)
        return supports
    

    def evolve():
        stationary = False
        for i in range(len(B)):
            s = fall_down(i)
            if len(s) == 0:
                dz = -min(B[i, 0, 2], B[i, 1, 2])
            else:
                dz = -min([_s[1] for _s in s])
            if dz == 0:
                stationary = True
            B[i, 0, 2] += dz
            B[i, 1, 2] += dz
        return stationary

    # ----------- PART 1 -----------
    #
    #for i in range(100):
    while True:
        #print(i)
        if not evolve():
            break

    supporters = []
    for i in range(len(B)):
        s = supported(i)
        if len(s) == 1 and s[0] != -1:
            supporters.append(s[0])

    answer = len(B) - len(np.unique(supporters))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #

    supported_by = [supported(i) for i in range(len(B))]
    supports = [[] for _ in range(len(B))]
    for i, s in enumerate(supported_by):
        for _s in s:
            if _s != -1:
                supports[_s].append(i)


    answer = 0
    for i in range(len(B)):
        #print('{} / {}'.format(i, len(B)))
        falling = {i}
        def adjancencies(i):
            a = []
            for j in supports[i]:
                if all([k in falling for k in supported_by[j]]):
                    falling.add(j)
                    a.append(j)
            return a
        search = aoc.search.Path(adjancencies).initial(i).run()
        answer += len(falling) - 1

    print("Part 2: {}".format(answer)) # 74287
    

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
