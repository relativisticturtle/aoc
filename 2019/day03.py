import os
import sys
import clipboard
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input

#import numpy as np
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	
	# ----------- PART 1 -----------
	#
	ans1 = None
	print("Part 1: {}".format(ans1))
	clipboard.set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	ans2 = None
	print("Part 2: {}".format(ans2))
	clipboard.set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
