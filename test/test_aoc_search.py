import numpy as np

from aoc_utils import get_input
import aoc


def test_search_on_2022_12():
    # Parse indata
    indata = get_input(12, 2022, silent=True)
    L = indata.splitlines(keepends=False)
    M = np.array([list(l) for l in L])
    S = np.where(M=='S')
    E = np.where(M=='E')
    start = S[0][0], S[1][0]
    stop = E[0][0], E[1][0]
    M[start] = 'a'
    M[stop] = 'z'

    # Define search
    class Search(aoc.BFS):
        def finished(self, state):
            return state == stop
        
        def adjacencies(self, node):
            return [
                neighbor for neighbor in aoc.neighbors(node)
                if aoc.in_range(neighbor, M.shape) and ord(M[neighbor]) <= ord(M[node]) + 1
            ]

    # Part 1
    answer = Search().append_initial(start).run().get_result()
    assert answer == 472

    # Part 2
    S = np.where(M=='a')
    initial_positions = list(zip(list(S[0]), list(S[1])))
    answer = Search().extend_initial(initial_positions).run().get_result()
    assert answer == 465


def nyi_test_search_on_2022_16():
    # Parse indata
    indata = get_input(16, 2022, silent=True)
    maze = dict()
    for l in indata.splitlines(keepends=False):
        valve = l.split()[1]
        flow = int(l.split()[4][5:-1])
        neigh = [v[:-1] for v in l.split()[9:-1]] + [l.split()[-1]]
        maze[valve] = flow, neigh
    assert False


def test_search_on_2021_09():
    # Parse indata
    indata = get_input(9, 2021, silent=True)
    M = np.array([[int(x) for x in l] for l in indata.splitlines(keepends=False)])

    # Part 1
    low_points = []
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            for q in aoc.neighbors((i, j)):
                if aoc.in_range(q, M.shape) and not M[i, j] < M[q[0], q[1]]:
                    break
            else:
                low_points.append((i, j))
    answer = 0
    for i, j in low_points:
        answer += M[i, j] + 1
    assert answer == 633

    # Part 2
    class Search(aoc.BFS):
        def adjacencies(self, node):
            return [
                neigh for neigh in aoc.neighbors(node)
                if aoc.in_range(neigh, M.shape) and M[node] < M[neigh] and M[neigh] < 9
            ]
    basin_sizes = []
    for i, j in low_points:
        search = Search().append_initial((i, j))
        search.run()
        basin_sizes.append(len(search.get_visited()))
    answer = np.prod(sorted(basin_sizes)[-3:])
    assert answer == 1050192


def test_search_on_2020_07():
    # IS THIS A SEARCH PROBLEM?
    # (or can be?)
    from collections import defaultdict

    # Parse indata
    indata = get_input(7, 2020, silent=True)
    rules = dict()
    canbein = defaultdict(list)
    for l in indata.splitlines(keepends=False):
        bag_color, content = tuple(l.split(' bags contain '))
        if content == 'no other bags.':
            bag_content = []
        else:
            bag_content = [(' '.join(x.split()[1:-1]), int(x.split()[0])) for x in content.split(', ')]
            for c, i in bag_content:
                canbein[c].append(bag_color)
        rules[bag_color] = bag_content
    
    # Part 1
    class Search(aoc.BFS):
        def adjacencies(self, node):
            return canbein[node]
    answer = len(Search().append_initial('shiny gold').run().get_visited()) - 1
    assert answer == 148

    # Part 2
    class Search(aoc.Recursive):
        def adjacencies(self, node):
            return [color for color, count in rules[node]]

        def evaluate(self, node, adjacencies):
            count = 1
            for b, c in rules[node]:
                count += c * self.get_result(b)
            return count
    
    answer = Search().run('shiny gold').get_result() - 1
    assert answer == 24867


if __name__ == '__main__':
    tests = [item for item in globals() if item.startswith('test_') and callable(globals()[item])]
    for item in tests:
        try:
            globals()[item]()
            print('{:70s} : PASS'.format(item))
        except AssertionError as error:
            print('{:70s} : FAIL'.format(item))
            print('> {}'.format(error))
