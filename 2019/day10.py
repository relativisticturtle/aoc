import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
#from collections import deque
from math import gcd

def run(indata):
	L = indata.splitlines(keepends=False)
	
	directions = []
	W, H = len(L[0]), len(L)
	for dy in range(1-H, H):
		for dx in range(1-W, W):
			if dx == 0 and dy == 0:
				continue
			if gcd(dx, dy) == 1:
				directions.append((dx, dy))
	
	# ----------- PART 1 -----------
	#
	most_visible = 0
	most_at = None
	for y in range(H):
		for x in range(W):
			if L[y][x] != "#":
				continue
			visible = 0
			for dx, dy in directions:
				for s in range(1, max(W,H)):
					if not (0 <= x + s*dx < W and 0 <= y + s*dy < H):
						break
					if L[y + s*dy][x + s*dx] == "#":
						visible += 1
						break
			if visible > most_visible:
				most_visible = visible
				most_at = (x, y)
	ans1 = most_visible
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	ans2 = None
	# M = np.array([[c=="#" for c in l] for l in L], dtype=bool)
	count = 0
	x, y = most_at
	directions.sort(key=lambda d: -np.arctan2(d[0], d[1]))
	while count<200:
		for dx, dy in directions:
			for s in range(1, min(W,H)):
				if not (0 <= x + s*dx < W and 0 <= y + s*dy < H):
					break
				if L[y + s*dy][x + s*dx] == "#":
					L[y + s*dy] = L[y + s*dy][:(x+s*dx)] + "." + L[y + s*dy][(1+x+s*dx):]
					count += 1
					if count == 200:
						ans2 = 100*(x + s*dx) + y + s*dy
					break
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
