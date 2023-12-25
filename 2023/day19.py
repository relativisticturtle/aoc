import numpy as np
import aoc

def run(indata):
    L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]

    # Parse workflows
    W = dict()
    for l in L[0]:
        s = l.split('{')
        W[s[0]] = tuple(t.split(':') for t in s[1][:-1].split(','))
    
    # Parse parts
    P = [eval(l.replace('=', '\':').replace(',', ',\'').replace('{', '{\'')) for l in L[1]]

    # Expand and simplify workflows
    W2 = dict()
    workflows = list(W.keys())
    for lbl in workflows:
        rules = W[lbl]
        for i in range(len(rules) - 1):
            x = 'xmas'.index(rules[i][0][0])
            ineq = rules[i][0][1]
            val = int(rules[i][0][2:])
            new_lbl = lbl + (str(i) if i>0 else '')
            if ineq == '<':
                W2[new_lbl] = [x, val, rules[i][-1], lbl + str(i+1)]
            elif ineq == '>':
                W2[new_lbl] = [x, val + 1, lbl + str(i+1), rules[i][-1]]
        i = len(rules) - 1
        new_lbl = lbl + (str(i) if i>0 else '')
        W2[new_lbl] = rules[-1][-1]

    # ----------- PART 1 -----------
    # 
    def apply_rule(rule, p):
        outcome = rule
        while outcome not in 'AR':
            if isinstance(W2[outcome], list):
                x, v, o1, o2 = W2[outcome]
                outcome = o1 if p[x] < v else o2
            else:
                outcome = W2[outcome]
        return outcome

    answer = 0
    for p in P:
        if apply_rule('in', [p[x] for x in 'xmas']) == 'A':
            answer += sum(p.values())
    print("Part 1: {}".format(answer)) #472630

    # ----------- PART 2 -----------
    #
    import copy
    def admissible_from(wf, limits):
        if any([l[1] <= l[0] for l in limits]):
            return 0
        if wf == 'A':
            return np.prod([l[1] - l[0] for l in limits], dtype=np.int64)
        elif wf == 'R':
            return 0
        
        if isinstance(W2[wf], list):
            x, val, wf1, wf2 = W2[wf]
            limits1 = copy.deepcopy(limits)
            limits1[x][1] = val
            limits2 = copy.deepcopy(limits)
            limits2[x][0] = val
            return admissible_from(wf1, limits1) + admissible_from(wf2, limits2)
        else:
            return admissible_from(W2[wf], limits)

    answer = admissible_from('in', [[1, 4001], [1, 4001], [1, 4001], [1, 4001]])
    print("Part 2: {}".format(answer)) # 116738260946855
    

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
