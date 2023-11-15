import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
import IntCode
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	code = [int(c) for c in L[0].split(",")]
	
	# ----------- PART 1 -----------
	#
	hull = np.zeros((101,101), dtype=int)
	heatmap = np.zeros((101,101), dtype=int)
	D = [(0, -1), (1, 0), (0, 1), (-1, 0)]
	pos = [50, 50]
	dir = 0
	visited = set()
	machine = IntCode.Machine(code)
	
	while not machine.halted:
		machine.push_input(hull[pos[1], pos[0]])
		machine.run(print_code=False)
		out = machine.pop_output()
		hull[pos[1], pos[0]] = out[0]
		heatmap[pos[1], pos[0]] += 1
		dir = (dir + 2*out[1] - 1) % 4
		pos = [p + d for p, d in zip(pos, D[dir])]
		visited.add(tuple(pos))
	
	ans1 = len(visited)
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	plt.imshow(heatmap)
	plt.show()
	
	# ----------- PART 2 -----------
	#
	hull = np.zeros((101,101), dtype=int)
	D = [(0, -1), (1, 0), (0, 1), (-1, 0)]
	pos = [50, 50]
	hull[pos[1], pos[0]] = 1
	dir = 0
	machine = IntCode.Machine(code)
	
	while not machine.halted:
		machine.push_input(hull[pos[1], pos[0]])
		machine.run(print_code=False)
		out = machine.pop_output()
		hull[pos[1], pos[0]] = out[0]
		dir = (dir + 2*out[1] - 1) % 4
		pos = [p + d for p, d in zip(pos, D[dir])]
	
	plt.imshow(hull)
	plt.show()
	# ans2 = None
	# print("Part 2: {}".format(ans2))
	# clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
