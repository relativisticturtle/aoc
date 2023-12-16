import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    H = indata.strip().split(',')

    def hash(h):
        x = 0
        for c in h:
            x = (17 * (x + ord(c))) % 256
        return x
    # ----------- PART 1 -----------
    #
    answer = sum([hash(h) for h in H])
    print("Part 1: {}".format(answer)) #x503154
    
    # ----------- PART 2 -----------
    #
    boxes = [dict() for _ in range(256)]
    for h in H:
        if h[-1] == '-':
            label = h[:-1]
            i = hash(label)
            if label in boxes[i]:
                boxes[i].pop(label)
        else:
            label = h[:-2]
            i = hash(label)
            f = int(h[-1])
            boxes[i][label] = f

    answer = 0
    for b, box in enumerate(boxes):
        for i, f in enumerate(box.values()):
            answer += (1+b) * (1 + i) * f
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
