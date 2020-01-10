import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
from collections import deque
import IntCode


def explore(machine):
	directions = ((0, 0), (0,-1), (0,1), (-1,0), (1,0))
	opposite_ = (0, 2, 1, 4, 3)
	path2 = {(0, 0): ()}
	oxygen_at = None
	
	dfsQ = deque()
	dfsQ.extend([(1,), (2,), (3,), (4,)])
	while len(dfsQ) > 0:
		path = dfsQ.pop()
		pos = tuple(np.sum([directions[p] for p in path], axis=0))
		
		# Walk this direction and see what happens
		machine.push_input(path[-1])
		machine.run(print_code=False)
		out = machine.pop_output()[-1]
		
		# Retracing?
		if len(path) > 1 and path[-1] == opposite_[path[-2]]:
			assert out > 0
			continue
			
		# Skip if hit wall
		if out == 0:
			path2[pos] = 0
			continue
		
		# Oxygen?
		if out == 2:
			oxygen_at = pos
		
		# Register path
		path2[pos] = path
		
		# Retrace from here
		dfsQ.append(path + (opposite_[path[-1]],))
	
		# Search _new_ squares
		for d in range(1,5):
			new_pos = tuple([p+D for p, D in zip(pos, directions[d])])
			
			# Been there already?
			if new_pos in path2:
				continue
			
			# Give it a try
			dfsQ.append(path + (d,))
	
	# Plot
	xmin = min([pos[0] for pos in path2])
	xmax = max([pos[0] for pos in path2])
	ymin = min([pos[1] for pos in path2])
	ymax = max([pos[1] for pos in path2])
	M = np.zeros((ymax-ymin+1, xmax-xmin+1), dtype=int)
	for pos in path2:
		if isinstance(path2[pos], tuple):
			M[pos[1]-ymin, pos[0]-xmin] = 1
		else:
			M[pos[1]-ymin, pos[0]-xmin] = 2
	plt.imshow(M, extent=(xmin-0.5, xmax+0.5, -ymax-0.5, -ymin+0.5), interpolation="none")
	plt.show()
	return path2, oxygen_at


def run(indata):
	L = indata.splitlines(keepends=False)
	code = [int(c) for c in L[0].split(",")]
	
	# ----------- PART 1 -----------
	#
	machine = IntCode.Machine(code)
	path2, oxygen_at = explore(machine)
	ans1 = len(path2[oxygen_at])
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	for d in path2[oxygen_at]:
		machine.push_input(d)
		machine.run(print_code=False)
		out = machine.pop_output()[-1]
		assert out > 0
	assert out == 2
	
	path2, _ = explore(machine)
	
	ans2 = max([len(path2[pos]) if isinstance(path2[pos], tuple) else 0 for pos in path2])
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
