import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)
from aoc_utils import get_input, clipboard_set

import numpy as np
from matplotlib import pyplot as plt
#from collections import deque

def run(indata):
	L = indata.splitlines(keepends=False)
	data = np.array([int(c) for c in L[0]], dtype=int)
	data = data.reshape((-1,6,25))
	
	
	
	
	
	# ----------- PART 1 -----------
	#
	ans1 = None
	max_nz = 0
	for z in range(data.shape[0]):
		nz = np.sum(data[z,:,:]!=0)
		if nz > max_nz:
			max_nz = nz
			ans1 = np.sum(data[z,:,:]==1)*np.sum(data[z,:,:]==2)
		
	print("Part 1: {}".format(ans1))
	clipboard_set("{}".format(ans1))
	
	# ----------- PART 2 -----------
	#
	ans2 = None
	img = np.ones((6,25), dtype=int)*2
	for z in range(data.shape[0]):
		mask = (img==2) & (data[z,:,:]!=2)
		img[mask]=data[z,mask]
	plt.imshow(img)
	plt.show()
	# print("Part 2: {}".format(ans2))
	# clipboard_set("{}".format(ans2))


if __name__ == '__main__':
	day = os.path.basename(__file__)[3:5]
	year = os.path.basename(os.path.dirname(__file__))
	indata = get_input(day=int(day), year=int(year))
	run(indata)
