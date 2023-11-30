class Evolution:
    def __init__(self, evolve, initial_state, initial_data):
        self._evolve = evolve
        self._history = [(initial_state, initial_data)]
        self._visited = {initial_state: 0}
        self._revisit = None

    def run(self, max_iter=-1):        
        while self._revisit is None and (max_iter == -1 or len(self._history) <= max_iter):
            state, data = self._evolve(*self._history[-1])
            if state in self._visited:
                self._revisit = self._visited[state]
            else:
                self._visited[state] = len(self._history)
            self._history.append((state, data))  
        return self

    def history(self, t=-1):
        return self._history[t]
    
    def extrapolate(self, t):
        assert self._revisit is not None
        hit1 = self._revisit
        hit2 = len(self._history) - 1
        dt = (t - hit1) % (hit2 - hit1)
        loops = (t - hit1) // (hit2 - hit1)
        state = self._history[hit1 + dt][0]
        data1 = self._history[hit1][1]
        data2 = self._history[hit2][1]
        return state, loops, data1, data2
