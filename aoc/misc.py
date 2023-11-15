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
