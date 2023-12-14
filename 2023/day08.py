import numpy as np
import aoc

# In this problem the input was designed so that the following holds:
#  - Every ghost's cycle is evenly divisible by the instruction's cycle-length
#    (281 in this example)
#    (no need to book-keep the current offset)
#  - First hit at goal-position is after exactly 1 cycle-length
#    (no need to use chinese remainder theorem. lcm is sufficient)
#  - Each ghost only visits one goal-position in its orbit


# REMEMBER when using NumPy
#  !!! dtype=int implies int32 !!!


def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    instr = L[0]
    M = {
        l.split()[0]: (l.split(', ')[0][-3:], l.split(', ')[1][:3])
        for l in L[2:]
    }
    
    start_positions = [p for p in M if p.endswith('A')]
    X = dict()
    for start_pos in start_positions:
        pos = start_pos
        s = 0
        while not pos.endswith('Z'):
            pos = M[pos][instr[s%len(instr)] == 'R']
            s = s+1
        print(pos + ' : ' + str(s)) 
        X[start_pos] = s

    # ----------- PART 1 -----------
    #
    if 'AAA' in X:
        answer = X['AAA']
        print("Part 1: {}".format(answer))  # 16579

    # ----------- PART 2 -----------
    #
    answer = 1
    for c in X.values():
        answer = np.lcm(answer, c, dtype=np.int64)
    print("Part 2: {}".format(answer))  # 12927600769609
    

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
