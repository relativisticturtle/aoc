import numpy as np
import aoc


def test_search_on_2022_12(input):
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


if __name__ == '__main__':
    from aoc_utils import get_input
    tests = [item for item in globals() if item.startswith('test_') and callable(globals()[item])]
    for item in tests:
        try:
            globals()[item](input)
            print('{:70s} : PASS'.format(item))
        except AssertionError as error:
            print('{:70s} : FAIL'.format(item))
            print('> {}'.format(error))