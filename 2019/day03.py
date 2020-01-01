import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	
	# Directions
	D = {
		'U': (0, 1),
		'D': (0, -1),
		'L': (-1, 0),
		'R': (1, 0)
	}
	
	# Walk every thread
	threads = []
	for l in L:
		walk = np.zeros((0,2), dtype=int)
		for t in l.split(','):
			walk = np.vstack((walk, np.tile(D[t[0]], (int(t[1:]), 1))))
		threads.append(np.cumsum(walk, axis=0))
	
	# ----------- PART 1 -----------
	#
	T1 = set([tuple(pos) for pos in threads[0]])
	T2 = set([tuple(pos) for pos in threads[1]])
	X = T1 & T2
	ans1 = 9999999
	for x in X:
		ans1 = min(abs(x[0])+abs(x[1]), ans1)
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	T1 = dict([(tuple(pos), s+1) for s, pos in enumerate(threads[0])])
	T2 = dict([(tuple(pos), s+1) for s, pos in enumerate(threads[1])])
	ans2 = 9999999
	for x in X:
		ans2 = min(T1[x]+T2[x], ans2)
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
