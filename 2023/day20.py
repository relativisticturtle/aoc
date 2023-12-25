import numpy as np
import aoc
from collections import deque

def run(indata):
    L = indata.splitlines(keepends=False)

    modules = dict()
    broadcaster = None
    for l in L:
        s, r = l.split(' -> ')
        modules[s[1:]] = (s[0], r.split(', '))

    ff_state = dict()
    for m in modules:
        if modules[m][0] == '%':
            ff_state[m] = 0

    cj_inputs = dict()
    for m in modules:
        for out in modules[m][1]:
            if out not in modules:
                continue
            if modules[out][0] == '&':
                if out not in cj_inputs:
                    cj_inputs[out] = dict()
                cj_inputs[out][m] = 0

    pulses_count = [0, 0]
    rx_feeder = [m for m, w in modules.items() if 'rx' in w[1]]
    assert len(rx_feeder) == 1
    rx_feeder = rx_feeder[0]
    pulse_for_rx = dict()

    def evolve(button_presses):
        Q = deque()
        Q.append(('button', 'roadcaster', 0))
        while len(Q) > 0:
            src, m, pulse = Q.popleft()
            pulses_count[pulse] += 1
            if m not in modules:
                continue
            if m == rx_feeder and pulse == 1:
                if src not in pulse_for_rx:
                    pulse_for_rx[src] = []
                pulse_for_rx[src].append(button_presses)
            if modules[m][0] == '&':
                cj_inputs[m][src] = pulse
                out_pulse = int(not all([mem == 1 for mem in cj_inputs[m].values()]))
            elif modules[m][0] == '%':
                if pulse == 1:
                    continue # high pulses are ignored
                ff_state[m] = 1 - ff_state[m]
                out_pulse = ff_state[m]
            elif modules[m][0] == 'b':
                out_pulse = pulse

            for target in modules[m][1]:
                Q.append((m, target, out_pulse))
    
    # ----------- PART 1 -----------
    #
    button_presses = 0
    while button_presses < 1000:
        button_presses += 1
        evolve(button_presses)
    answer = pulses_count[0] * pulses_count[1]
    print("Part 1: {}".format(answer)) # 879834312
    
    # ----------- PART 2 -----------
    #
    while button_presses < 10000:
        button_presses += 1
        evolve(button_presses)

    answer = 1
    for p in pulse_for_rx.values():
        assert p[1] == 2 * p[0], 'Input assumption violated'
        answer *= p[0]

    print("Part 2: {}".format(answer)) # 243037165713371
    

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
