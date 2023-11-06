import numpy as np

from aoc_utils import get_input
import aoc



def test_search_on_2022_12():
    # Parse indata
    indata = get_input(12, 2022)
    L = indata.splitlines(keepends=False)
    M = np.array([list(l) for l in L])
    S = np.where(M=='S')
    E = np.where(M=='E')
    start = S[0][0], S[1][0]
    stop = E[0][0], E[1][0]
    M[start] = 'a'
    M[stop] = 'z'

    # Define search
    class Search(aoc.Search):
        def finished(self, state):
            return state == stop
        
        def candidates(self, from_state):
            return [
                neighbor for neighbor in aoc.neighbors(from_state)
                if aoc.in_range(neighbor, M.shape) and ord(M[neighbor]) <= ord(M[from_state]) + 1
            ]

    search = Search(start)
    goal_state = search.run()
    result1 = search.total_cost(goal_state)
    assert result1 == 472 # Part 1 (with my input)

    S = np.where(M=='a')
    search = Search(initial_states=list(zip(list(S[0]), list(S[1]))))
    goal_state = search.run()
    result1 = search.total_cost(goal_state)
    assert result1 == 465 # Part 2 (with my input)


def nyi_test_search_on_2022_16():
    # Parse indata
    indata = get_input(16, 2022)
    maze = dict()
    for l in indata.splitlines(keepends=False):
        valve = l.split()[1]
        flow = int(l.split()[4][5:-1])
        neigh = [v[:-1] for v in l.split()[9:-1]] + [l.split()[-1]]
        maze[valve] = flow, neigh
    assert False


def test_search_on_2021_09():
    # Parse indata
    indata = get_input(9, 2021)
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
    class Search(aoc.Search):
        def candidates(self, from_state):
            return [
                neigh for neigh in aoc.neighbors(from_state)
                if aoc.in_range(neigh, M.shape) and M[from_state] < M[neigh] and M[neigh] < 9
            ]
    basin_sizes = []
    for i, j in low_points:
        search = Search((i, j))
        search.run()
        basin_sizes.append(len(search.visited()))
    answer = np.prod(sorted(basin_sizes)[-3:])
    assert answer == 1050192


if __name__ == '__main__':
    tests = [item for item in globals() if item.startswith('test_') and callable(globals()[item])]
    for item in tests:
        try:
            globals()[item]()
            print('{:70s} : PASS'.format(item))
        except AssertionError as error:
            print('{:70s} : FAIL'.format(item))
            print('> {}'.format(error))