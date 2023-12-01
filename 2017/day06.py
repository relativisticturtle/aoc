import aoc
import numpy as np


def run(indata):
    L = indata.splitlines(keepends=False)
    #L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]

    initial = tuple(int(x) for x in L[0].split())

    def evolve(state):
        new_state = list(state)
        i = np.argmax(new_state)
        a = new_state[i]
        new_state[i] = 0
        while a > 0:
            i = (i + 1) % 16
            new_state[i] += 1
            a -= 1
        return tuple(new_state)

    simul = aoc.simul.Evolution(evolve, initial).run()


    # ----------- PART 1 -----------
    #
    answer = len(simul._visited)
    print("Part 1: {}".format(answer)) # 5042
    
    # ----------- PART 2 -----------
    #
    answer = simul.loop_length()
    print("Part 2: {}".format(answer)) # 1086
    

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
