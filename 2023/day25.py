import numpy as np
import aoc

def run(indata):
    G = dict()
    for l in indata.splitlines(keepends=False):
        p = l.split(': ')[0]
        Q = l.split(': ')[1].split()
        
        if p in G:
            for q in Q:
                G[p].add(q)    
        else:
            G[p] = set(Q)
        for q in Q:
            if q in G:
                G[q].add(p)
            else:
                G[q] = {p}

    # ----------- PART 1 -----------
    #
    removed_edges = []
    def adjacent(p):
        return [q for q in G[p] if ((p, q) not in removed_edges and (q, p) not in removed_edges)]
    
    # Choose 2 nodes that are probably in different "sub-graphs"
    xnodes = ['mgz']
    for _ in range(6):
        search = aoc.search.Path(adjacent).initial(xnodes[-1]).run()
        nodes, dist = zip(*search._result.items())
        xnodes.append(nodes[np.argmax(dist)])
    xnodes = xnodes[-2:]
    print('Chosen end-nodes: {}'.format(xnodes))

    # Along the paths, successively remove an edge until path is no more
    answer = None
    path1 = aoc.search.Path(adjacent).initial(xnodes[0]).run().path_to(xnodes[1])
    edges1 = [(path1[i], path1[i+1]) for i in range(len(path1) - 1)]
    # Optional reshuffle, so that look at middle edges first, for optimization
    #count = 0
    #import itertools
    #edges1 = list(itertools.chain(*zip(edges1[len(edges1)//2:], edges1[:len(edges1)//2][::-1] + [('x', 'x')]*(len(edges1)%2))))
    for e1 in edges1:
        removed_edges.append(e1)
        path2 = aoc.search.Path(adjacent).initial(xnodes[0]).run().path_to(xnodes[1])
        edges2 = [(path2[i], path2[i+1]) for i in range(len(path2) - 1)]
        edges2 = [e2 for e2 in edges2 if e2 not in edges1]
        #edges2 = list(itertools.chain(*zip(edges2[len(edges2)//2:], edges2[:len(edges2)//2][::-1] + [('x', 'x')]*(len(edges2)%2))))

        for e2 in edges2:
            removed_edges.append(e2)
            path3 = aoc.search.Path(adjacent).initial(xnodes[0]).run().path_to(xnodes[1])
            edges3 = [(path3[i], path3[i+1]) for i in range(len(path3) - 1)]
            edges3 = [e3 for e3 in edges3 if e3 not in (edges1 + edges2)]
            #edges3 = list(itertools.chain(*zip(edges3[len(edges3)//2:], edges3[:len(edges3)//2][::-1] + [('x', 'x')]*(len(edges3)%2))))

            for e3 in edges3:
                #count += 1
                removed_edges.append(e3)
                search = aoc.search.Path(adjacent).initial(xnodes[0]).run()
                path4 = search.path_to(xnodes[1])
                if path4 is None:
                    count1 = len(search.visited())
                    count2 = len(G) - count1
                    answer = count1 * count2
                if answer: break
                removed_edges.pop()
            if answer: break
            removed_edges.pop()
        if answer: break
        removed_edges.pop()

    #print(count)
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    answer = 'Merry Christmas!'
    print("Part 2: {}".format(answer))


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input() #test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
