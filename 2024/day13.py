import numpy as np
import aoc


def run(indata):
    #L = indata.splitlines(keepends=False)
    L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    Q = []
    for block in L:
        a = [int(d.split('+')[1]) for d in block[0].split(':')[1].split(', ')]
        b = [int(d.split('+')[1]) for d in block[1].split(':')[1].split(', ')]
        p = [int(d.split('=')[1]) for d in block[2].split(':')[1].split(', ')]
        Q.append([a, b, p])
    
    # ----------- PART 1 & 2 -----------
    #
    answers = [0, 0]
    for q in Q:
        q2 = [q[2], [10000000000000 + x for x in q[2]]]
        for i in [0, 1]:
            ab = np.linalg.solve(np.column_stack(q[:2]), q2[i])
            a, b = int(np.round(ab[0])), int(np.round(ab[1]))
            if a * q[0][0] + b * q[1][0] != q2[i][0]:
                continue
            if a * q[0][1] + b * q[1][1] != q2[i][1]:
                continue
            answers[i] += 3 * a + 1 * b

    print("Part 1: {}".format(answers[0]))
    print("Part 2: {}".format(answers[1]))


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
