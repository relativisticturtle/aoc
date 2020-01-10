import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
from collections import deque
import IntCode

def run(indata):
	L = indata.splitlines(keepends=False)
	code = [int(c) for c in L[0].split(",")]
	
	# ----------- PART 1 -----------
	#
	machine = IntCode.Machine(code)
	machine.run(print_code=False)
	out = np.array(machine.pop_output()).reshape((-1, 3))
	W, H = 1+max(out[:,0]), 1+max(out[:,1])
	
	ans1 = np.sum(out[:,2]==2)
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	code[0] = 2
	machine = IntCode.Machine(code)
	screen = np.zeros((H, W), dtype=int)
	score = 0
	while not machine.halted:
		machine.run(print_code=False)
		out = np.array(machine.pop_output()).reshape((-1, 3))
		for d in out:
			if d[0] == -1:
				score = d[2]
			else:
				screen[d[1], d[0]] = d[2]
		paddle_pos = np.where(screen == 3)[1][0]
		ball_pos = np.where(screen == 4)[1][0]
		machine.push_input(np.sign(ball_pos - paddle_pos))
		#plt.imshow(screen, interpolation="none")
		#plt.show()
		#break
	
	ans2 = score
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
