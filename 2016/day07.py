import os
import sys


# Lessons learned
#  - read carefully: missed the cases with multiple hypernet sequences in 1 package
#    "____[------]____[----]____"
#  - set-operations
#    set.union(a, b, c, ...), set.intersect(...)

def has_abba(code):
    for i in range(len(code) - 3):
        if code[i] == code[i + 1]:
            continue
        if code[i] == code[i + 3] and code[i + 1] == code[i + 2]:
            return True
    return False

def get_abas(code, rev=False):
    abas = set()
    for i in range(len(code) - 2):
        if code[i] == code[i + 1]:
            continue
        if code[i] == code[i + 2] and not rev:
            abas.add(code[i:(i+2)])
        elif code[i] == code[i + 2] and rev:
            abas.add(code[(i+1):(i+3)])
    return abas

def run(indata):
    L = indata.splitlines(keepends=False)
    # ----------- PART 1 -----------
    #
    answer = 0
    for l in L:
        package = l.replace(']', '[').split('[')
        if any([has_abba(p) for p in package[1::2]]):
            continue
        if any([has_abba(p) for p in package[0::2]]):
            answer += 1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 0
    for l in L:
        package = l.replace(']', '[').split('[')
        abas = set.union(*[get_abas(p, rev=False) for p in package[0::2]])
        babs = set.union(*[get_abas(p, rev=True) for p in package[1::2]])
        if len(set.intersection(abas, babs)) > 0:
            answer += 1
    print("Part 2: {}".format(answer))
    

if __name__ == '__main__':
    # Initialize
    ROOT = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(ROOT)
    from aoc.utils import get_input, clipboard_set

    # Get input data
    day = int(os.path.basename(__file__)[3:5])
    year = int(os.path.basename(os.path.dirname(__file__)))
    indata = get_input(day, year)
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
