def run(indata):
    L = indata.splitlines(keepends=False)

    K0 = {
        '7': (0, 0),
        '8': (0, 1),
        '9': (0, 2),
        '4': (1, 0),
        '5': (1, 1),
        '6': (1, 2),
        '1': (2, 0),
        '2': (2, 1),
        '3': (2, 2),
        '0': (3, 1),
        'A': (3, 2),
    }
    K1 = {
        '^': (0, 1),
        'A': (0, 2),
        '<': (1, 0),
        'v': (1, 1),
        '>': (1, 2),
    }
    DIR = {
        '^': (-1, 0),
        '>': ( 0, 1),
        'v': ( 1, 0),
        '<': ( 0,-1),
    }

    memo = dict()
    def cost_for(i, target, current, npad=False): # robot index (0 = human), target pos, and current pos
        if i == 0:
            return 1
        if (i, target, current, npad) in memo:
            return memo[i, target, current, npad]
        
        # Construct 2 possible paths
        D = target[0] - current[0], target[1] - current[1]
        seq1 = '^' * -D[0] + 'v' * D[0] + '<' * -D[1] + '>' * D[1] + 'A'
        seq2 = '<' * -D[1] + '>' * D[1] + '^' * -D[0] + 'v' * D[0] + 'A'

        # Reject if invalid
        def valid(p, seq, npad):
            for d in seq[:-1]:
                p = p[0] + DIR[d][0], p[1] + DIR[d][1]
                if npad and p == (3, 0):
                    return False
                if not npad and p == (0, 0):
                    return False
            return True

        # Pick best valid path
        if valid(current, seq1, npad):
            cost1 = 0
            for d, b in zip(seq1, 'A' + seq1[:-1]):
                cost1 += cost_for(i - 1, K1[d], K1[b])
        else:
            cost1 = 1e12
        if valid(current, seq2, npad):
            cost2 = 0
            for d, b in zip(seq2, 'A' + seq2[:-1]):
                cost2 += cost_for(i - 1, K1[d], K1[b])
        else:
            cost2 = 1e12

        memo[i, target, current, npad] = min(cost1, cost2)
        return memo[i, target, current, npad]

    
    # ----------- PART 1 & 2 -----------
    #
    for part, depth in enumerate([2, 25]):
        answer = 0
        for code in L:
            cost = 0
            for d, b in zip(code, 'A' + code[:-1]):
                cost += cost_for(depth + 1, K0[d], K0[b], npad=True)
            a = cost
            b = int(code[:-1])
            answer += a*b
            #print('{}: {} * {} = {}'.format(code, a, b, a*b))
        print("Part {}: {}".format(part+1, answer))
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
