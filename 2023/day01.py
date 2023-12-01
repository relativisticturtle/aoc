def run(indata):
    def calibration_sum(indata):
        L = indata.splitlines(keepends=False)
        answer = 0
        for l in L:
            v = 0
            for c in l:
                if c in '0123456789':
                    v += 10 * int(c)
                    break
            for c in l[::-1]:
                if c in '0123456789':
                    v += int(c)
                    break
            answer += v
        return answer
    
    # ----------- PART 1 -----------
    #
    answer = calibration_sum(indata)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    for i, w in enumerate(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']):
        indata = indata.replace(w, w + str(i) + w)
    answer = calibration_sum(indata)
    print("Part 2: {}".format(answer)) # 53348
    

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
