
# NetworkX

import networkx as nx
G = nx.DiGraph()
a = 'node1'
b = 'node2'
G.add_edge(a, b)
inbound_nodes = [edge[0] for edge in G.in_edges(g)]
outbound_nodes = [edge[1] for edge in G.out_edges(g)]


