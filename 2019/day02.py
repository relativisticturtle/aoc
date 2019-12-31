import os
import sys
import clipboard
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input

#import numpy as np
#from collections import deque
import IntCode

def run(indata):
	L = indata.splitlines(keepends=False)
	
	# ----------- PART 1 -----------
	#
	code = [int(c) for c in L[0].split(",")]
	code[1] = 12
	code[2] = 2
	machine = IntCode.Machine(code)
	machine.run(print_code=False)
	ans1 = machine.code[0]
	print("Part 1: {}".format(ans1))
	#clipboard.set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	ans2 = None
	for x in range(100):
		for y in range(100):
			code = [int(c) for c in L[0].split(",")]
			code[1] = x
			code[2] = y
			machine = IntCode.Machine(code)
			machine.run(print_code=False)
			if machine.code[0] == 19690720:
				ans2 = 100*x + y
				break
		if ans2:
			break
	print("Part 2: {}".format(ans2))
	clipboard.set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
