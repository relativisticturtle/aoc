def run(indata):
    L = indata.splitlines(keepends=False)
    T = [int(t) for t in L[0].split()[1:]]
    D = [int(d) for d in L[1].split()[1:]]

    def calc(T, D):
        answer = 1
        for t, d in zip(T, D):
            ways = 0
            for _t in range(t):
                _d = _t * (t -_t)
                if _d > d:
                    ways += 1
            answer *= ways
        return answer
    
    # ----------- PART 1 -----------
    #
    answer = calc(T, D)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = calc([int(''.join(map(str, T)))], [int(''.join(map(str, D)))])
    print("Part 2: {}".format(answer)) # 41382569
    

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
