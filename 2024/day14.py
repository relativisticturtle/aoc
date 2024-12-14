import numpy as np
import aoc

#W, H = 11, 7
W, H = 101, 103

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    R = []
    for l in L:
        p = [int(x) for x in l.split()[0].split('=')[1].split(',')]
        v = [int(x) for x in l.split()[1].split('=')[1].split(',')]
        R.append([p, v])
    R = np.array(R)
    
    # ----------- PART 1 -----------
    #
    P100 = R[:, 0, :] + 100 * R[:, 1, :]
    P100[:, 0] = P100[:, 0] % W
    P100[:, 1] = P100[:, 1] % H

    Q = np.array([[0,0,0],[0,0,0],[0,0,0]])
    for p in P100:
        Q[np.sign(p[0] - (W // 2)) + 1, np.sign(p[1] - (H // 2)) + 1] += 1

    answer = Q[0, 0] * Q[0, 2] * Q[2, 0] * Q[2, 2]
    print("Part 1: {}".format(answer)) #x242735104
    #return answer
    
    # ----------- PART 2 -----------
    #
    import matplotlib.pyplot as plt
    C = np.inf
    bestj = 0

    for j in range(10000):
        Pj = R[:, 0, :] + j * R[:, 1, :]
        Pj[:, 0] = Pj[:, 0] % W
        Pj[:, 1] = Pj[:, 1] % H
        if sum(np.std(Pj, axis=0)) < C:
            bestj = j
            C = sum(np.std(Pj, axis=0))
    answer = bestj
    print("Part 2: {}".format(answer))

    # Visualize
    Pj = R[:, 0, :] + bestj * R[:, 1, :]
    Pj[:, 0] = Pj[:, 0] % W
    Pj[:, 1] = Pj[:, 1] % H
    M = aoc.points.Set2D(Pj[:, 0], Pj[:, 1], np.ones_like(Pj[:, 0]))
    plt.imshow(M.image([0, W], [0, H]))
    plt.show()
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
