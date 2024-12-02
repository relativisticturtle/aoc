import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)

    P = np.array([[int(x) for x in l.split(' @ ')[0].split(', ')] for l in indata.splitlines(keepends=False)], dtype=np.int64)
    V = np.array([[int(x) for x in l.split(' @ ')[1].split(', ')] for l in indata.splitlines(keepends=False)], dtype=np.int64)

    # ----------- PART 1 -----------
    #
    def solve_2d(p1, v1, p2, v2):
        M = np.array([[-v1[0], v2[0]], [-v1[1], v2[1]]], dtype=float)
        t = np.linalg.solve(M, [p1[0] - p2[0], p1[1] - p2[1]])
        return t

    answer = 0
    for i in range(len(P)):
        for j in range(i):
            try:
                t = solve_2d(P[i], V[i], P[j], V[j])
            except:
                i1, i2 = i, j
                continue
            if np.any(t<0):
                continue
            p = P[i] + V[i] * t[0]
            if all([200000000000000 <= x and x <= 400000000000000 for x in p[:2]]):
                answer += 1

    print("Part 1: {}".format(answer)) #x 29257
    
    # ----------- PART 2 -----------
    #

    # Using cross-product method (suggested by Denys)

    # (p - pi) x (v - vi) == 0
    # (p x v) - (pi x v) - (p x vi) + (pi x vi) == 0
    # (pi x vi) - (pi x v) - (p x vi) == (pj x vj) - (pj x v) - (p x vj)
    # ((pj - pi) x v) + (p x (vj - vi)) == (pj x vj) - (pi x vi)
    #
    #
    #  [      0           (vj - vi)_z     -(vj - vi)_y]
    #  [ -(vj - vi)_z                      (vj - vi)_x]   [ p ]
    #  [  (vj - vi)_y    -(vj - vi)_x                 ]          =  RHS
    #  [      0          -(pj - pi)_z      (pj - pi)_y]
    #  [  (pj - pi)_z                     -(pj - pi)_x]   [ v ]
    #  [ -(pj - pi)_y     (pj - pi)_x                 ]

    def make_matrix_for(Pi, Vi, Pj, Vj):
        # Make equation system for solving M x = y
        # Returns M, y
        dv = Vj - Vi
        dp = Pj - Pi
        M = [
            [     0,    dv[2],   -dv[1],      0,   -dp[2],    dp[1]],
            [-dv[2],        0,    dv[0],  dp[2],        0,   -dp[0]],
            [ dv[1],   -dv[0],        0, -dp[1],    dp[0],        0],
        ]
        y = np.cross(Pj, Vj) - np.cross(Pi, Vi)
        return M, y

    M1, y1 = make_matrix_for(P[0], V[0], P[1], V[1])
    M2, y2 = make_matrix_for(P[0], V[0], P[2], V[2])
    M = np.concatenate([M1, M2])
    y = np.concatenate([y1, y2])
    PV = np.linalg.solve(M, y)
    answer = int(np.sum(np.round(PV[:3])))
    print("Part 2: {}".format(answer))

    # PV = [24, 13, 10, -3, 1, 2] # test data
    # PV = [
    #   194723518367339
    #   181910661443432
    #   150675954587450
    #   148, 159, 249
    # ]


    def compress(remainders, moduli):
        R = dict()
        for r1, m1 in zip(remainders, moduli):
            m = abs(m1)
            for r2, m2 in zip(remainders, moduli):
                if np.gcd(m, m2, dtype=np.int64) != 1:
                    m = np.gcd(m, m2, dtype=np.int64)
            if m not in R:
                R[m] = r1 % m
            elif R[m] != r1 % m:
                return None
        return R

    def candidates(i):
        c =[]
        for vx in range(-300, 300):
            r, m = zip(*[(p[i], v[i] - vx) for p, v in zip(P, V) if v[i] - vx != 0])
            r0 = [p[i] for p, v in zip(P, V) if v[i] - vx == 0]
            
            R = compress(r, m)
            if R is None:
                continue
            m = [int(x) for x in R.keys()]
            r = [int(x) for x in R.values()]
            p = aoc.math.chinese_remainder_theorem(r, m)
            if not all([p == p0 for p0 in r0]):
                continue
            c.append((vx, p))
        return c
    
    a = [candidates(i) for i in range(3)]

    assert all([len(_a) == 1 for _a in a]), 'Assumption violated'
    answer = a[0][0][1] + a[1][0][1] + a[2][0][1]
    print("Part 2: {}".format(answer))


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
