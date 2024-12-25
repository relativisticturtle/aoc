from collections import defaultdict
import itertools
import numpy as np
import aoc


def run(indata):
    #L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    G = dict()
    for l in indata.split('\n\n')[0].splitlines(keepends=False):
        g, v = l.split(': ')
        G[g] = int(v)

    
    OP = {
        'AND': {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1},
        'XOR': {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0},
        'OR': {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}
    }

    L = indata.split('\n\n')[1].splitlines(keepends=False)
    changed = True
    while changed:
        changed = False 
        for l in L:
            op, out = l.split(' -> ')
            g1, op, g2 = op.split()
            if out not in G and g1 in G and g2 in G:
                G[out] = OP[op][G[g1], G[g2]]
                changed = True

    
    # ----------- PART 1 -----------
    #
    answer = ''
    for i in range(99):
        g = 'z{:02d}'.format(i)
        if g in G:
            answer = str(G[g]) + answer
        else:
            break
    answer = int(answer, 2)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    import sys
    sys.setrecursionlimit(100)
    Q = dict()
    L = indata.split('\n\n')[1].splitlines(keepends=False)
    for l in L:
        op, out = l.split(' -> ')
        g1, op, g2 = op.split()
        Q[out] = (g1, op, g2)


    def calc(X, Y, swap_wires=()):
        G = dict()
        rX = str(bin(X))[:1:-1]
        rY = str(bin(Y))[:1:-1]
        rX += '0' * (45 - len(rX))
        rY += '0' * (45 - len(rY))
        for i, x in enumerate(rX):
            G['x{:02d}'.format(i)] = int(x)
        for i, y in enumerate(rY):
            G['y{:02d}'.format(i)] = int(y)
        def eval(g):
            for g1, g2 in swap_wires:
                if g == g1:
                    g = g2
                    break
                if g == g2:
                    g = g1
                    break
            if g in G:
                return G[g]
            
            g1, op, g2 = Q[g]
            G[g] = OP[op][eval(g1), eval(g2)]
            return G[g]
        ans = ''
        for i in range(46):
            g = 'z{:02d}'.format(i)
            if g not in Q:
                break
            try:
                v = eval(g)
            except RecursionError:
                return None
            ans = str(v) + ans
        return int(ans, 2)

    # 1001100011111001101000001111001011001101001000 : 46

    # LEVEL 1
    print('LEVEL 1')
    level1 = defaultdict(dict)
    for l in L:
        op, out = l.split(' -> ')
        g1, op, g2 = op.split()
        if g1.startswith('x') and g2.startswith('y'):
            level1[g1, g2][op] = out
        elif g1.startswith('y') and g2.startswith('x'):
            level1[g2, g1][op] = out
    level1_outs = []
    for g1, g2 in sorted(level1.keys()):
        for op in sorted(level1[g1, g2].keys()):
            out = level1[g1, g2][op]
            print('{} {} {} -> {}'.format(g1, op, g2, out))
        level1_outs.append(out)
    
    print('LEVEL2')
    level2 = defaultdict(dict)
    for out, q in Q.items():
        if out in level1_outs:
            continue
        if q[0] in level1_outs:
            level2[q[0], q[2]][q[1]] = out
        elif q[2] in level1_outs:
            level2[q[2], q[0]][q[1]] = out
    level2_outs = []
    for g1, g2 in sorted(level2.keys(), key=lambda x: level1_outs.index(x[0])):
        for op in sorted(level2[g1, g2].keys()):
            out = level2[g1, g2][op]
            print('{} {} {} -> {}'.format(g1, op, g2, out))
        level2_outs.append(out)

    print('LEVEL3')
    level3 = defaultdict(dict)
    for out, q in Q.items():
        if out in level1_outs or out in level2_outs:
            continue
        if q[0] in level2_outs:
            level3[q[0], q[2]][q[1]] = out
        elif q[2] in level2_outs:
            level3[q[2], q[0]][q[1]] = out
    level3_outs = []
    for g1, g2 in sorted(level3.keys(), key=lambda x: level2_outs.index(x[0])):
        for op in sorted(level2[g1, g2].keys()):
            out = level3[g1, g2][op]
            print('{} {} {} -> {}'.format(g1, op, g2, out))
        level3_outs.append(out)
    
    # LEVEL last
    print('LEVEL last')
    for i in range(46):
        g = 'z{:02d}'.format(i)
        g1, op, g2 = Q[g]
        print('{} {} {} -> {}'.format(g1, op, g2, g))
    #return

    # Determined by manual inspection of net, identifying
    # obvious deviations from pattern
    swaps = (
        ('z19', 'cph'),
        ('z33', 'hgj'),
        ('z13', 'npf'),
    )

    # Determine last pair by brute-force
    candidates = [
        (g1, g2) for (g1, g2) in itertools.product(Q, repeat=2)
        if g1 < g2 and (g2, g1) not in swaps
    ]
    while len(candidates) > 2:
        # Pick random input
        x = np.random.randint(2**44, dtype=np.uint64)
        y = np.random.randint(2**44, dtype=np.uint64)
        z = calc(x, y, swaps)
        if z != x + y:
            print('{} + {} != {}'.format(x, y, z))
        z = x + y

        # Only retain valid candidates
        old_candidates = candidates.copy()
        candidates = []
        for g1, g2 in old_candidates:
            if calc(x, y, swaps + ((g1, g2),)) == z:
                print('{},{}'.format(g1, g2))
                candidates.append((g1, g2))
    answer = ','.join(sorted(list(itertools.chain(*swaps)) + list(candidates[0])))
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
