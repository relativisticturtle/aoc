import numpy as np
import aoc


def run(indata):
    L = [int(x) for x in indata.split()]

    # ----------- PART 1 -----------
    #
    def eval_node(pos):
        C, M = L[pos], L[pos+1]
        total = 0
        current_pos = pos + 2
        for c in range(C):
            value, current_pos = eval_node(current_pos)
            total += value
        for m in range(M):
            total += L[current_pos]
            current_pos += 1
        return total, current_pos

    answer, _ = eval_node(0)
    print("Part 1: {}".format(answer))

    # Just trying out if easy to transform
    # general recursive problem to Recursive-class
    class Part1(aoc.search.Recursive):
        def _run(self, pos):
            C, M = L[pos], L[pos+1]
            total = 0
            current_pos = pos + 2
            for c in range(C):
                value, current_pos = self._run(current_pos)
                total += value
            for m in range(M):
                total += L[current_pos]
                current_pos += 1
            self._result[pos] = total
            return total, current_pos
    answer = Part1(None, None).run(0).result()

    # ----------- PART 2 -----------
    #
    def eval_node(pos):
        C, M = L[pos], L[pos+1]
        current_pos = pos + 2

        if C == 0:
            return sum(L[current_pos:(current_pos + M)]), current_pos + M
        
        children = []
        for c in range(C):
            value, current_pos = eval_node(current_pos)
            children.append(value)
        total = 0
        for m in range(M):
            c = L[current_pos] - 1
            if 0 <= c and c < len(children):
                total += children[c]
            current_pos += 1
        return total, current_pos

    answer, _ = eval_node(0)
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':

    # Get input data
    indata = aoc.get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        aoc.clipboard_set(str(answer))
