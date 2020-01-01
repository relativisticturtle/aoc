import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

#import numpy as np
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	
	# ----------- PART 1 -----------
	#
	fuel = 0
	for l in L:
		w = int(l)
		if w > 5:
			fuel += int(w/3) - 2
	print("Part 1: {}".format(fuel))
	clipboard_set("{}".format(fuel))
	
	# ----------- PART 2 -----------
	#
	fuel = 0
	for l in L:
		w = int(l)
		while w > 5:
			fuel += int(w/3) - 2
			w = int(w/3) - 2
	print("Part 2: {}".format(fuel))
	clipboard_set("{}".format(fuel))


if __name__ == '__main__':
	indata = get_input(day=1, year=2019)
	run(indata)

