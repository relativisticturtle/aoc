import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input

#import numpy as np
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	
	# ----------- PART 1 -----------
	#
	print("Part 1: {}".format(-2018))
	
	# ----------- PART 2 -----------
	#
	print("Part 2: {}".format(-1))
	

if __name__ == '__main__':
	indata = get_input(day=1, year=2018)
	run(indata)
