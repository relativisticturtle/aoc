import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

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
            #if all([7 <= x and x <= 27 for x in p[:2]]):
            if all([200000000000000 <= x and x <= 400000000000000 for x in p[:2]]):
                answer += 1
            #print(p)

    print("Part 1: {}".format(answer)) #x 29257
    
    # ----------- PART 2 -----------
    #

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
                #print(m, R[m], r1)
                return None
        return R

    def candidates(i):
        c =[]
        for vx in range(-200, 200):
            m = [v[i] - vx for v in V]
            r = [p[i] for p in P]
            
            if any([_m == 0 for _m in m]):
                continue
        
            R = compress(r, m)
            if R is None:
                continue
            m = [int(x) for x in R.keys()]
            r = [int(x) for x in R.values()]
            #print(aoc.math.chinese_remainder_theorem(r, m))
            c.append((vx, aoc.math.chinese_remainder_theorem(r, m)))
        return c
    
    candidate_vx = candidates(0)
    candidate_vy = candidates(1)
    candidate_vz = candidates(2)
    
    assert len(candidate_vx) == 1, 'Assumption violated'
    v0, x0 = candidate_vx[0]
    
    t = np.array([- (p[0] - x0) / (v[0] - v0) for p, v in zip(P, V)])
    assert np.all(t == np.round(t)), 'Assumption violated'
    t = np.round(t).astype(np.int64)

    # Knowing t, solve for 2 first points
    # (v2-v0)*t2 + p2 - p0 = 0
    # (v1-v0)*t1 + p1 - p0 = 0
    #
    # v2 * t2 + p2 = v0 * t2 + p0 = A t + p0
    A = [
        [t[0], 0, 0, 1, 0, 0],
        [0, t[0], 0, 0, 1, 0],
        [0, 0, t[0], 0, 0, 1],
        [t[1], 0, 0, 1, 0, 0],
        [0, t[1], 0, 0, 1, 0],
        [0, 0, t[1], 0, 0, 1]
    ]
    y = np.concatenate([
        V[0] * t[0] + P[0],
        V[1] * t[1] + P[1]
    ])
    a = np.linalg.solve(A, y)
    answer = a[3]+a[4]+a[5]
    print("Part 2: {}".format(np.round(answer).astype(np.int64)))
    

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
