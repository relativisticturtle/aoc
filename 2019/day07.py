import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

#import numpy as np
#from collections import deque
import IntCode
from itertools import permutations

def run(indata):
	L = indata.splitlines(keepends=False)
	
	code = [int(c) for c in L[0].split(",")]
	
	# ----------- PART 1 -----------
	#
	ans1 = 0
	for phases in permutations([0, 1, 2, 3, 4]):
		# Initialize amplifiers
		machines = [IntCode.Machine(code) for p in phases]
		for machine, phase in zip(machines, phases):
			machine.push_input(phase)
		# Run 1 by 1
		out = 0
		for machine in machines:
			machine.push_input(out)
			machine.run(print_code=False)
			out = machine.pop_output()[0]
		# Register output
		ans1 = max(ans1, out)
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	ans2 = 0
	for phases in permutations([5, 6, 7, 8, 9]):
		# Initialize amplifiers
		machines = [IntCode.Machine(code) for p in phases]
		for machine, phase in zip(machines, phases):
			machine.push_input(phase)
		# Run in a loop, 1 by 1
		out = 0
		while not machines[-1].halted:
			for machine in machines:
				machine.push_input(out)
				machine.run(print_code=False)
				out = machine.pop_output()[0]
		# Register output
		ans2 = max(ans2, out)
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
