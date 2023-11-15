import os
import sys

def run(indata):
    #L = indata.splitlines(keepends=False)
    commands = [l.splitlines() for l in indata.split('$ ')[1:]]
    commands.extend([['cd ..']]*2)
    
    # ----------- PART 1 -----------
    #
    answer = 0
    D = dict()
    p = '/'
    for c in commands[1:]:
        if c[0] == 'cd ..':
            SZ = sum([sz for nm, sz in D.items() if nm.startswith(p) and nm[-1] != '/'])
            if SZ <= 100000:
                answer += SZ
            D[p] = SZ
            print('{:8d} : {}'.format(int(sz), p))
            p = '/'.join(p.split('/')[:-2]) + '/'
        elif c[0].startswith('cd '):
            p = p + c[0][3:] + '/'
            assert p not in D
        elif c[0] == 'ls':
            SZ = 0
            for n in c[1:]:
                sz, nm = tuple(n.split())
                if sz == 'dir':
                    continue
                D[p + nm] = int(sz)
                print('{:8d} : {}'.format(int(sz), p + nm))

    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    todel = 30000000 - (70000000 - D['/'])
    answer = min([sz for nm, sz in D.items() if nm[-1] == '/' and sz >= todel])
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
