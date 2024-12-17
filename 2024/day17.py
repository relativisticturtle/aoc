def combo(x, A, B, C):
    if x in [0, 1, 2, 3]:
        return x
    elif x == 4:
        return A
    elif x == 5:
        return B
    elif x == 6:
        return C
    else:
        raise RuntimeError

memo = dict()
def go_recu(A, B, C, P):
    orig = (A, B, C)
    if orig in memo:
        return memo[orig]
    i = 0
    while i+1 < len(P):
        if P[i] == 0:   #adv
            A = A // 2**combo(P[i+1], A, B, C)
        elif P[i] == 1: #bxl
            B = B ^ P[i+1]
        elif P[i] == 2: #bst
            B = combo(P[i+1], A, B, C) % 8
        elif P[i] == 3: #jnz
            if A != 0:
                i = P[i+1]
                continue
        elif P[i] == 4: #bxc
            B = B ^ C
        elif P[i] == 5: #out
            # Code is like this: ...,5,5,3,0 <END>
            #   out cmb(B)
            #   jnz(A, 0)
            # Only occurence of 'out' and 'jnz' in program
            #   --> Loop-back to initial (i=0) with new values
            #       of A, B & C. Can implement recursively.
            #       And with memoization!
            if A == 0:
                q = ''
            else:
                q = go_recu(A, B, C, P)
            if q is None:
                return None
            q = str(combo(P[i+1], A, B, C) % 8) + q
            memo[orig] = q
            return q
        elif P[i] == 6:   #bdv
            B = A // 2**combo(P[i+1], A, B, C)
        elif P[i] == 7:   #cdv
            C = A // 2**combo(P[i+1], A, B, C)
        else:
            raise RuntimeError
        i+=2
    return ''

def run(indata):
    L = indata.splitlines(keepends=False)
    A = int(L[0].split(': ')[-1])
    B = int(L[1].split(': ')[-1])
    C = int(L[2].split(': ')[-1])
    P = [int(x) for x in L[4].split(': ')[-1].split(',')]

    # ----------- PART 1 -----------
    #
    result = go_recu(A, B, C, P)
    answer = ','.join(list(result))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #
    # Memoization + assume "8x PREVIOUS + SOMETHING" yields answer
    target = ''.join([str(x) for x in P])
    result = ''
    i = 0
    prev = 0
    while result != target:
        result = go_recu(i, B, C, P)
        if target.endswith(result) and len(result) > prev:
            prev = len(result)
            print('{:20d} | {:20s} : {}'.format(i, oct(i), result))
            if result == target:
                answer = i
                break
            else:
                i *= 8
        else:
            i+=1
    print("Part 2: {}".format(answer))
    return answer


if __name__ == '__main__':
    # Initialize
    from aoc.utils import get_input, clipboard_set

    # Get input data
    indata = get_input()
    
    # Run
    answer = run(indata)

    # Copy to clipboard?
    if answer is not None:
        clipboard_set(str(answer))
