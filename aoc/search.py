from typing import Callable, Any, Iterable, Union, Hashable, Tuple
from typing_extensions import Self
from collections import deque


def _finished_default(node) -> bool:
    return False


def _cost_default(from_node, to_node) -> int:
    return 1


def _heuristic_default(node) -> int:
    return 0


def _evaluate_default(node) -> Tuple[Any, Any]:
    return 0, None


class Search:
    """Base class for searches"""
    def __init__(self):
        self._previous = dict() # Node prior to this
        self._finish = None
        self._result = dict()

    def finish(self):
        """Get finish-node"""
        return self._finish

    def visited(self):
        """Get all visited nodes

        A node is visited when the evaluation-result 
        (or cost, path-length, ...) has been recorded.
        """
        return self._result.keys()
    
    def result(self, node=None):
        """Get result of finish-node, or specified node

        Returns None if result hasn't been evaluated yet.
        """
        if node is None:
            return self._result.get(self._finish, None)
        else:
            return self._result.get(node, None)
    
    def path_to(self, node=None):
        """Get path from start to this node (or finish-node if unspecified)"""
        path = [node if node is not None else self._finish]
        while path[-1] in self._previous:
            path.append(self._previous[path[-1]])
        return path[::-1]

    def run(self, *args, **kwargs):
        raise NotImplementedError('Search-class is virtual')


class Path(Search):
    """Base class for path-searches

    - cost() is cost of going to next node.
      - Default is 1.

    - heuristic() is minimal cost to finish.
      - Default is 0.

    - finished() checks whether goal has been reached.
      - Default is False.
      - (Search proceeds until all reachable nodes have been visited)
    """

    def __init__(self,
                 adjacencies: Callable[[Any], Iterable],
                 cost: Callable[[Any, Any], Union[int, float]] = None,
                 finished: Callable[[Any], bool] = None,
                 heuristic: Callable[[Any], Union[int, float]] = None,
                ):
        super().__init__()
        self._initial_nodes = dict()
        self._result = dict()
        self._adjacencies = adjacencies
        self._cost = cost if cost is not None else _cost_default
        self._finished = finished if finished is not None else _finished_default
        self._heuristic = heuristic if heuristic is not None else _heuristic_default

        if cost is not None or heuristic is not None:
            # --------------------------------------
            # Djikstra or A-star. Use priority queue
            # --------------------------------------
            import heapq
            def q_init_heapq(items):
                heapq.heapify(items)
                return items
            def q_pop_heapq(queue):
                return heapq.heappop(queue)
            def q_push_heapq(queue, item):
                heapq.heappush(queue, item)
            self.__q_init = q_init_heapq
            self.__q_pop = q_pop_heapq
            self.__q_push = q_push_heapq
        else:
            # -----------------------------
            # Fixed cost. Use regular queue
            # -----------------------------
            def q_init_deque(items):
                return deque(items)
            def q_pop_deque(queue):
                return queue.popleft()
            def q_pop_deque_dfs(queue):     # When need DFS-search...(?)
                return queue.pop()
            def q_push_deque(queue, item):
                queue.append(item)
            self.__q_init = q_init_deque
            self.__q_pop = q_pop_deque
            self.__q_push = q_push_deque

    def initial(self, nodes: Union[set, dict, Hashable], cost=0) -> Self:
        """Append multiple initial start nodes

        Optionally set corresponding initial costs
        """
        if isinstance(nodes, set):
            self._initial_nodes = {node: cost for node in nodes}
        elif isinstance(nodes, dict):
            self._initial_nodes = {node: value for node, value in nodes.items()}
        elif isinstance(nodes, Hashable):
            self._initial_nodes = {nodes: cost}
        else:
            raise ValueError('`nodes` must be set- or dict-type (or hashable)')

        return self

    def run(self):
        class Edge:
            def __init__(self, prev, next, total_cost, heuristic):
                self.prev = prev
                self.next = next
                self.total_cost = total_cost
                self.heuristic = heuristic

            def __lt__(self, obj):
                return self.total_cost + self.heuristic < obj.total_cost + obj.heuristic

        # Initialize queue
        Q = self.__q_init([
            Edge(None, node, cost, self._heuristic(node))
            for (node, cost) in self._initial_nodes.items()
        ])

        # Reset prior to running
        self._finish = None
        self._initial_nodes = dict()

        # Run!
        while len(Q) > 0:
            # Unpack next edge
            edge = self.__q_pop(Q)
            node = edge.next

            # Check if first (or best) visit
            if node in self._result and self._result[node] <= edge.total_cost:
                continue
            self._result[node] = edge.total_cost
            self._previous[node] = edge.prev

            # Check if finished
            if self._finished(node):
                self._finish = node
                return self

            # Submit to queue
            for adjacent in self._adjacencies(node):
                total_cost = edge.total_cost + self._cost(node, adjacent)
                self.__q_push(Q, Edge(node, adjacent, total_cost, self._heuristic(adjacent)))

        # Search ended without finding goal
        return self


class Recursive(Search):
    """Base class for recursive searches
    
    - evaluate() is result of current node - knowing the result of all child-nodes.
      - Default is 1.
    
    - finished() checks whether goal has been reached.
      - Default is False.
      - (Search proceeds until all reachable nodes have been visited)
    """
    # TODO: Identify different patterns
    #  - Recursive  : children found in advance, eval at end, memoization
    #  - Parse      : children found 1 at a time, eval at end
    #  - ...
    def __init__(self,
                 children: Callable[[Any], Iterable],
                 evaluate: Callable[[Any, Any], Union[int, float]],
                ):
        super().__init__()
        self._result = dict()
        self._children = children
        self._evaluate = evaluate if evaluate is not None else _evaluate_default

    def run(self, node):
        # Top-node is finish
        self._run(node)
        self._finish = node

        # Return self to allow method cascading
        return self

    def _run(self, node):
        # Recursive eval
        subresults = dict()
        for child in self._children(node):
            if child not in self._result:
                # Run for node. May emit a sibling-node
                self._run(child)

                # Set current node as parent-node
                self._previous[child] = node

            # Extract result of child-node
            subresults[child] = self._result[child]

        # Evaluate current state
        self._result[node] = self._evaluate(node, subresults)
