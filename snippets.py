##########################
# NetworkX
#
#
import networkx as nx
G = nx.DiGraph()
a = 'node1'
b = 'node2'
G.add_edge(a, b)
inbound_nodes = [edge[0] for edge in G.in_edges(a)]
outbound_nodes = [edge[1] for edge in G.out_edges(a)]



##########################
# WALKING on grid
#
#
#  Right-hand system:
#
#     y   
#       ^      position = [x, y]
#       |
#       |
#       +------>  x
#
import numpy as np
import hw_python.utils.transformations as T
M_left = T.rotate(90, 'Z', degrees=True)
M_right = T.rotate(-90, 'Z', degrees=True)
M_fw = T.translate(0, 1, 0)                     # Y is forward-direction

# Turn left, go forward, turn right, forward 5 steps
# (!!! note order when doing intrinsic transforms)
M = M_left @ M_fw @ M_right @ np.linalg.matrix_power(M_fw, 5)

pos = M[:2, 3].round().astype(int)
visited = {tuple(pos): 1}                       # Use dict for book-keeping?
visited[tuple(pos)] = 'Kilroy'



##########################
# SEARCH (using Queues)
#
#
from collections import deque
Q = deque()
Q.append(('START', 0))
V = dict()
while len(Q) > 0:
    word, value = Q.popleft()
    for i in range(1, len(word)):
        if word[i:] not in V:
            Q.append((word, value + i))
            V[word[i:]] = value + i
answer = sum(V.values())



##########################
# INSTRUCTIONS
#
#
L = ['add x, 1', 'cmp y, 0']
C = [l.split() for l in L]
C = [[l.split()[0]] + ' '.join(l.split()[1:]).split(', ') for l in L]

i = 0
while i < len(C):
    # REMEMBER TO "i += 1" AT ANY CONTINUE!
    if C[i][0] == 'add':
        print('add {} {}'.format(*C[i][1:]))
    elif C[i][0] == 'cmp':
        print('cmp {} {}'.format(*C[i][1:]))
    i += 1


##########################
# CHINESE REMAINDER THEOREM
#
#
from aoc_algo import chinese_remainder_theorem
remainders = [1, 2, 3, 4, 5]
moduli = [5, 14, 13, 27, 11]
print('\n' + '\n'.join(['x == {} (mod {:2d})'.format(r, m) for r, m in zip(remainders, moduli)]))
x = chinese_remainder_theorem(remainders, moduli)
print('--> x = {}'.format(x))
