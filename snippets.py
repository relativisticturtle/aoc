
# NetworkX

import networkx as nx
G = nx.DiGraph()
a = 'node1'
b = 'node2'
G.add_edge(a, b)
inbound_nodes = [edge[0] for edge in G.in_edges(a)]
outbound_nodes = [edge[1] for edge in G.out_edges(a)]





##########################
#  Walking on grid
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