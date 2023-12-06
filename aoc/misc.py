# Direction lists
D4 = ((0, 1), (1, 0), (0, -1), (-1, 0))
D5 = ((0, 1), (1, 0), (0, -1), (-1, 0), (0, 0))
D8 = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
D9 = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 0))

# Arrows, when D4 is interpreted
# - as (dx, dy)
# - with positive y downwards (screen coordinates)
V4 = 'v>^<'


def neighbors(pos, dirs=D4, lim=None):
    if lim is not None:
        if len(lim) == 1 and hasattr(lim[0], '__len__'):
            assert len(lim[0]) == len(pos), 'lim-length must be same as pos-length'
            min_lim = [0] * len(lim[0])
            max_lim = lim[0]
        elif len(lim) == 2 and hasattr(lim[0], '__len__') and hasattr(lim[1], '__len__'):
            assert len(lim[0]) == len(pos), 'lim-length must be same as pos-length'
            assert len(lim[1]) == len(pos), 'lim-length must be same as pos-length'
            min_lim = lim[0]
            max_lim = lim[1]
        else:
            assert len(lim) == len(pos), 'lim-length must be same as pos-length'
            min_lim = [0] * len(lim)
            max_lim = lim

        neigh = []
        for d in dirs:
            p = tuple(x + dx for x, dx in zip(pos, d))
            if all([mn <= q and q < mx for q, mn, mx in zip(p, min_lim, max_lim)]):
                neigh.append(p)
        return neigh
    else:
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
