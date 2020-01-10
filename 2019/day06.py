import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

#import numpy as np
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	
	orbits = dict()
	for l in L:
		obj = l.split(")")
		orbits[obj[1]] = obj[0]
	
	# ----------- PART 1 -----------
	#
	ans1 = 0
	for obj0 in orbits:
		obj = obj0
		while obj != "COM":
			obj = orbits[obj]
			ans1 += 1
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	trace_san = dict()  # distance to SAN(ta)
	obj = "SAN"
	l = 0
	while obj != "COM":
		obj = orbits[obj]
		trace_san[obj] = l
		l += 1
	obj = "YOU"  # step until intercept SAN(ta) trace
	l = 0
	while obj not in trace_san:
		obj = orbits[obj]
		l += 1
	ans2 = trace_san[obj] + l - 1
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
