import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import math
import numpy as np
#from matplotlib import pyplot as plt
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	
	
	
	# ----------- PART 1 -----------
	#
	pos = np.array([[int(a[2:]) for a in l[1:-1].split(", ")] for l in L], dtype=int)
	vel = np.zeros_like(pos)
	
	for i in range(1000):
		vel += np.array([np.sum(np.sign(pos-p), axis=0) for p in pos])
		pos += vel
	
	ans1 = np.sum(np.sum(np.abs(pos), axis=1) * np.sum(np.abs(vel), axis=1))
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	pos = np.array([[int(a[2:]) for a in l[1:-1].split(", ")] for l in L], dtype=int)
	vel = np.zeros_like(pos)
	visited = [dict() for a in range(3)]
	orbit = [None for a in range(3)]
	
	for i in range(1000000):
		vel += np.array([np.sum(np.sign(pos-p), axis=0) for p in pos])
		pos += vel
		ax_hash = [tuple(a) for a in np.vstack((pos, vel)).T]
		for a in range(3):
			if not orbit[a] and ax_hash[a] in visited[a]:
				orbit[a] = i - visited[a][ax_hash[a]]
			else:
				visited[a][ax_hash[a]] = i
		if all(orbit):
			break
	
	print(orbit)
	ans2 = orbit[0]*orbit[1]//math.gcd(orbit[0], orbit[1])
	ans2 = ans2*orbit[2]//math.gcd(ans2, orbit[2])
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
