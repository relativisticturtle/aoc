import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc.utils import get_input, clipboard_set

#import numpy as np
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	start = int(L[0].split("-")[0])
	stop = int(L[0].split("-")[1])
	
	# ----------- PART 1 -----------
	#
	ans1=0
	for i in range(start, stop+1):
		pwd = "%d" % i
		# 6-digit
		if len(pwd) != 6: 
			continue
		# Increasing
		if not all([int(pwd[p]) <= int(pwd[p+1]) for p in range(5)]):
			continue
		# Group of 2
		if not any([pwd[p] == pwd[p+1] for p in range(5)]):
			continue
		ans1 += 1
		
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	ans2 = 0
	for i in range(start, stop+1):
		pwd = "%d" % i
		# 6-digit
		if len(pwd) != 6: 
			continue
		# Increasing
		if not all([int(pwd[p]) <= int(pwd[p+1]) for p in range(5)]):
			continue
		# Group of _exactly_ 2
		gr2 = [False] + [pwd[p] == pwd[p+1] for p in range(5)] + [False]
		if not any([gr2[p] and not gr2[p-1] and not gr2[p+1] for p in range(1,6)]):
			continue
		ans2 += 1
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
