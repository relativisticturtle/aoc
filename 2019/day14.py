import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

#import numpy as np
#from matplotlib import pyplot as plt
from collections import deque, defaultdict


def make_fuel(reactions, q=1):
	inventory = defaultdict(int)
	order = deque()
	order.append(("FUEL", q))
	ore_cost = 0
	
	while len(order) > 0:
		chemical, q = order.popleft()
		if chemical == "ORE":
			ore_cost += q
			continue
		
		inventory[chemical] -= q
		if inventory[chemical] >= 0:
			continue
		
		Q = reactions[chemical][0]
		N = (-inventory[chemical]+(Q-1)) // Q
		for reagent in reactions[chemical][1]:
			order.append((reagent[0], N*reagent[1]))
		inventory[chemical] += N*Q
	return ore_cost

def run(indata):
	L = indata.splitlines(keepends=False)
	reactions = dict()
	for l in L:
		reagents = l.split(" => ")[0].split(", ")
		product = l.split(" => ")[1]
		reactions[product.split()[1]] = (int(product.split()[0]), [(r.split()[1], int(r.split()[0])) for r in reagents])
	
	# ----------- PART 1 -----------
	#
	ans1 = make_fuel(reactions)
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	lower_bound = 1000000000000//ans1
	upper_bound = lower_bound*2
	
	while lower_bound+1 < upper_bound:
		test_q = (lower_bound+upper_bound)//2
		if make_fuel(reactions, q=test_q) > 1000000000000:
			upper_bound = test_q
		else:
			lower_bound = test_q
	ans2 = lower_bound
	print("Part 2: {}".format(ans2))
	clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
