import numpy as np
import aoc

def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    visited = dict()

    def combinations(record, contig):
        state = (record, tuple(contig))
        if state in visited:
            return visited[state]

        if len(contig) == 0:
            if all([r in '?.' for r in record]):
                return 1
            else:
                return 0
        elif all([r in '.' for r in record]):
            return 0
        record0 = record

        valid = 0
        while len(record) >= sum(contig) and len(contig) > 0:
            if all([r in '?#' for r in record[:contig[0]]]) and (len(record) == contig[0] or record[contig[0]] in '?.'):
                # valid
                valid += combinations(record[contig[0]+1:], contig[1:])
            if record[0] in '?.':
                record = record[1:]
            else:
                break
        
        #if valid > 0:
        #    print('{:10s}{:20s}: {}'.format(str(contig), record0, valid))
        visited[state] = valid
        return valid

    # ----------- PART 1 -----------
    #
    answer = 0
    for l in L:
        record = l.split()[0]
        contig = [int(x) for x in l.split()[1].split(',')]
        answer += combinations(record, contig)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for l in L:
        record = '?'.join([l.split()[0]] * 5)
        contig = [int(x) for x in l.split()[1].split(',')] * 5
        a = combinations(record, contig)
        print(a)
        answer += a
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
