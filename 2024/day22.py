import numpy as np


def run(indata):
    L = indata.splitlines(keepends=False)
    S = [int(s) for s in L]

    def mix(a, s):
        return a ^ s

    def prune(s):
        return s % 16777216

    # ----------- PART 1 & 2 -----------
    #
    part1 = 0
    M = np.zeros((len(S), 2000), dtype=int)
    for j, s0 in enumerate(S):
        s = s0
        for i in range(2000):
            # 1
            s = prune(mix(64 * s, s))
            s = prune(mix(s // 32, s))
            s = prune(mix(2048 * s, s))
            M[j, i] = s % 10
        part1 += s
    print("Part 1: {}".format(part1))

    total = dict()
    for j, m in enumerate(M):
        visited = set()
        for i in range(4, len(m)):
            x = (
                m[i-3] - m[i-4],
                m[i-2] - m[i-3],
                m[i-1] - m[i-2],
                m[i-0] - m[i-1]
            )
            if x in visited: # only use first occurence
                continue
            visited.add(x)
            if x in total:
                total[x] += m[i]
            else:
                total[x] = m[i]

    answer = max(total.values())
    print("Part 2: {}".format(answer))
    return answer


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
