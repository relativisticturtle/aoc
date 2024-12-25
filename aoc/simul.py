from typing import Callable, Any, Iterable, Union, Hashable, Tuple
from typing_extensions import Self
from inspect import signature


class Evolution:
    """Model the evolution of a system, with optional metadata

    The metadata may be, e.g., an offset that increases every loop,
    but should otherwise not affect the evolution.

    Parameters
    ----------
    evolve : callable
        Takes a state and returns the next.
    initial_state : immutable
        Initial state of the system.
    initial_data : Any
        Initial metadata.
    """
    def __init__(self, evolve, initial_state, initial_data=None):
        parameters = signature(evolve).parameters
        if len(parameters) == 1:
            # Only state
            assert initial_data is None, 'Cannot have evolve(state) with data'
            self._with_data = False
        elif len(parameters) == 2:
            # State and data
            assert initial_data is not None, 'Cannot have evolve(state, data) without data'
            self._with_data = True
        else:
            raise RuntimeError('Must be evolve(state) or evolve(state, data)')

        self._evolve = evolve
        self._visited = {initial_state: 0}
        self._revisit = None
        self._history = [(initial_state, initial_data) if self._with_data else initial_state]

    def run(self, max_iter=-1):        
        while self._revisit is None and (max_iter == -1 or len(self._history) <= max_iter):
            # Evolve from latest
            if self._with_data:
                result = self._evolve(*self._history[-1])
                state = result[0]
            else:
                result = self._evolve(self._history[-1])
                state = result
            
            # Check if repeated state
            if state in self._visited:
                self._revisit = self._visited[state]
            else:
                self._visited[state] = len(self._history)
            
            # Record and continue(?)
            self._history.append(result)
        return self

    def history(self, t=-1):
        return self._history[t]

    def reoccurence(self):
        """Return first occurence-pair states"""
        assert self._revisit is not None, 'Reoccurence has not yet been reached'
        hit1 = self._revisit
        hit2 = len(self._history) - 1
        return hit1, hit2
    
    def loop_length(self):
        """Returns loop-length"""
        assert self._revisit is not None, 'Reoccurence has not yet been reached'
        return len(self._history) - 1 - self._revisit

    def loop_offset(self, t):
        """For a given time, return its offset within the loop"""
        hit1, hit2 = self.reoccurence()
        loop_length = hit2 - hit1
        dt = (t - hit1) % loop_length
        return dt
    
    def loop_number(self, t):
        """For a given time, return how many loops from first revisit"""
        hit1, hit2 = self.reoccurence()
        loop_length = hit2 - hit1
        loops = (t - hit1) // loop_length
        return loops
    
    def extrapolate(self, t):
        """Return state that ought to emerge at the given time"""
        assert self._revisit is not None, 'Reoccurence has not yet been reached'
        hit1 = self._revisit
        dt = self.loop_offset(t)
        return self._history[hit1 + dt]
    
    def extrapolate_with_data(self, t):
        """Return state, #loops, and the reoccurence pairs' metadata for the given time"""
        hit1, hit2 = self.reoccurence()
        loops = self.loop_number(t)
        dt = self.loop_offset(t)
        state = self._history[hit1 + dt][0]
        data1 = self._history[hit1][1]
        data2 = self._history[hit2][1]
        return state, loops, data1, data2
