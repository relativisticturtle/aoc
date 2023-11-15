import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

#import numpy as np
#from collections import deque
import IntCode

def run(indata):
	L = indata.splitlines(keepends=False)
	code = [int(c) for c in L[0].split(",")]
	
	# ----------- PART 1 -----------
	#
	machine = IntCode.Machine(code)
	machine.push_input(1)
	machine.run(print_code=False)
	ans1 = machine.pop_output()[0]
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	machine = IntCode.Machine(code)
	machine.push_input(2)
	machine.run(print_code=False)
	ans2 = machine.pop_output()[0]
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
