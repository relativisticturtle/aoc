import sys
import argparse
import IntCode

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("intcode", type=str, default='aout.txt')
    args = parser.parse_args()

    with open(args.intcode) as f:
        data = f.read()
    intcode = [int(c) for c in data.split(',')]

    machine = IntCode.Machine(intcode)
    while not machine.halted:
        machine.run(print_code=False)
        if len(machine.output) > 0:
            print('\n'.join(['%d' % c for c in machine.pop_output()]))
        if machine.blocked:
            data = sys.stdin.readline()
            machine.push_input([int(c) for c in data.split()])
    if len(machine.output) > 0:
        print('\n'.join(['%d' % c for c in machine.pop_output()]))