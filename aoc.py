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
    def __init__(self):
        self._result = dict()   # Outcome at each visited node
        self._previous = dict() # Node prior to this
        self._finish = None

    def get_result(self, node=None):
        if node is None:
            return self._result.get(self._finish, None)
        else:
            return self._result.get(node, None)

    def get_finish(self):
        return self._finish

    def get_visited(self):
        return self._result.keys()
    
    def get_path_to(self, node=None):
        path = [node if node is not None else self._finish]
        while path[-1] in self._previous:
            path.append(self._previous[path-1])
        return path[::-1]

    def run(self, *args, **kwargs):
        raise NotImplementedError('Search-class is virtual')

    def adjacencies(self, node):
        return []

    def evaluate(self, node, *args, **kwargs):
        return None


class BFS(Search):
    def __init__(self):
        super().__init__()
        self._initial_nodes = []

    def append_initial(self, initial_node, initial_cost=0):
        self._initial_nodes.append((initial_node, initial_cost))
        return self

    def extend_initial(self, initial_nodes, initial_costs=0):
        if not hasattr(initial_costs, '__len__'):
            initial_costs = [0] * len(initial_nodes)
        elif len(initial_costs) != len(initial_nodes):
            raise ValueError('`initial_costs` must have same length as `initial_nodes` (or be scalar)')
        self._initial_nodes.extend(zip(initial_nodes, initial_costs))
        return self

    def run(self):
        from collections import deque
        Q = deque()
        Q.extend(self._initial_nodes)

        # Reset these prior to running
        self._finish = None
        self._initial_nodes = []

        # Run!
        while len(Q) > 0:
            # Get node and check if actual (not yet visited)
            node, total_cost = Q.popleft()
            if node in self._result:
                continue
            self._result[node] = total_cost

            # Evaluate
            if self.finished(node):
                self._finish = node
                return self
            
            # Get adjacencies and cost of going there
            adjacencies = self.adjacencies(node)
            costs = [self.evaluate(node, a) for a in adjacencies]

            # Submit to queue
            for adjacent, cost in zip(adjacencies, costs):
                self._previous[adjacent] = node
                Q.append((adjacent, self._result[node] + cost))
        # Search ended without finding goal
        return self

    def evaluate(self, node, adjacent):
        return 1
    
    def finished(self, node):
        return False


class Recursive(Search):
    def run(self, node):
        # Top-node is finish
        self._run(node)
        self._finish = node
        # Return self to allow method cascading
        return self

    def _run(self, node):
        # Get adjacencies
        adjacencies = self.adjacencies(node)

        # Recursive eval
        for adjacency in adjacencies:
            if adjacency in self._result:
                continue
            self._previous[adjacency] = node
            self.run(adjacency)

        # Evaluate current state
        self._result[node] = self.evaluate(node, adjacencies)

    def evaluate(self, node, adjacencies):
        return 0
