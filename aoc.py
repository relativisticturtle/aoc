import numpy as np

# Direction lists
D4 = ((0, 1), (1, 0), (0, -1), (-1, 0))
D5 = ((0, 1), (1, 0), (0, -1), (-1, 0), (0, 0))
D8 = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
D9 = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 0))

def neighbors(pos, dirs=D4):
    return [tuple(x + dx for x, dx in zip(pos, d)) for d in dirs]

def in_range(x, lim1, lim2=None):
    # Compare scalars
    if not hasattr(x, '__len__'):
        if lim2 is not None:
            return lim1 <= x and x < lim2
        else:
            return 0 <= x and x < lim1
    # Compare arrays
    if not hasattr(lim1, '__len__'):
        lim1 = [lim1] * len(x)
    elif len(x) != len(lim1):
        raise ValueError('`lim1` must have same (or scalar) dimensionality as `x`')
    if lim2 is not None:
        if not hasattr(lim2, '__len__'):
            lim2 = [lim2] * len(x)
        elif len(x) != len(lim2):
            raise ValueError('`lim2` must have same (or scalar) dimensionality as `x`')
        return all([l1 <= xi and xi < l2 for xi, l1, l2 in zip(x, lim1, lim2)])
    else:
        return all([0 <= xi and xi < l1 for xi, l1 in zip(x, lim1)])


def chinese_remainder_theorem(remainders, moduli):
    """Find solution to system of modulus equations

        x == r1 (mod m1)
        x == r2 (mod m2)
        ...
        x == rN (mod mN)
    
    Input
        remainders: [r1, r2, ... rN]
        moduli:     [m1, m2, ... mN]
    """

    # For computational efficiency, sort on moduli
    moduli, remainders = tuple(zip(*sorted(zip(moduli, remainders), reverse=True)))

    M = moduli[0]
    x = remainders[0] % M
    for r, m in zip(remainders[1:], moduli[1:]):
        assert np.gcd(m, M) == 1, 'No common prime factors allowed among moduli'
        # Solve "x + q*N == r"
        #   q*N == r - x (mod m)
        #   q = (r-x (mod m)) * (N^-1 (mod m))
        q = ((r - x) % m) * pow(M, -1, m)

        # Adding q * M preserves previous remainders, while
        # introducing remainder r at current modulus m
        x += q * M
        M *= m
        x = x % M

    return x


class Search:
    def __init__(self, initial_state=None, initial_cost=0, initial_states=None, initial_costs=0):
        # One or more initial states
        if initial_state is not None:
            self.initial_states = [(initial_state, initial_cost)]
        else:
            self.initial_states = []
        if initial_states is not None:
            if not hasattr(initial_costs, '__len__'):
                initial_costs = [0] * len(initial_states)
            elif len(initial_costs) != len(initial_states):
                raise ValueError('`initial_costs` must have same length as `initial_states` (or be scalar)')
            self.initial_states.extend(zip(initial_states, initial_costs))

        # For book-keeping of visited states
        # (as a dict rather than set - to allow memoization)
        self._total_cost = dict()
        self._previous = dict()

    def run(self):
        from collections import deque
        Q = deque()
        Q.extend(self.initial_states)
        while len(Q) > 0:
            # Get state and check if actual (not yet visited)
            state, total_cost = Q.popleft()
            if state in self._total_cost:
                continue
            self._total_cost[state] = total_cost

            # Evaluate
            if self.finished(state):
                return state
            
            # Get candidates and cost of going there
            candidates = self.candidates(state)
            costs = [self.cost(state, c) for c in candidates]

            # Submit to queue
            for candidate, cost in zip(candidates, costs):
                self._previous[candidate] = state
                Q.append((candidate, total_cost + cost))
        # Search ended without finding goal
        return None

    def total_cost(self, state):
        return self._total_cost.get(state, None)

    def finished(self, state):
        return False

    def candidates(self, from_state):
        raise NotImplementedError()

    def cost(self, from_state, to_state):
        return 1
