from collections import defaultdict


def run(indata):
    L = indata.splitlines(keepends=False)
    A = defaultdict(list)
    for l in L:
        x = l.split('-')
        A[x[0]].append(x[1])
        A[x[1]].append(x[0])

    # ----------- PART 1 -----------
    #
    T = set()
    for a, B in A.items():
        for b in B:                         # For every edge
            for c in A.keys():              # and every other node
                if c in A[a] and c in A[b]: # check if node connected to both edge vertices
                    T.add(tuple(sorted((a, b, c))))
    answer = 0
    for a, b, c in T:   # Only count tri-sets that has at least one beginning with 't'
        if a[0] == 't' or b[0] == 't' or c[0] == 't':
            answer += 1
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #

    # Define every person as one LAN
    LANs = set([(a,) for a in A])

    # Successively add persons to the LANs
    # if fully connected with current members in that LAN
    changed = True
    while changed:
        changed = False  # Run until no more changes detected
        for a in A:
            for lan in LANs:
                if a in lan:    # (person is already in the LAN)
                    continue
                if all([b in A[a] for b in lan]):
                    # Person is fully connected to this LAN
                    # Replace current LAN by the bigger that
                    # includes the new member
                    LANs.add((a,) + lan)
                    LANs.remove(lan)
                    changed = True
                    break
    
    # Find biggest LAN and print sorted list of members
    biggest = [None, 0]
    for lan in LANs:
        if len(lan) > biggest[1]:
            biggest = [lan, len(lan)]
    answer = ','.join(sorted(biggest[0]))
    print("Part 2: {}".format(answer))
    return answer


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    #indata = get_input(test='test')
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
