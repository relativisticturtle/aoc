import numpy as np
import aoc

def run(indata):
    #L = indata.splitlines(keepends=False)
    L = [block.splitlines(keepends=False) for block in indata.split('\n\n')]
    #L = [int(x) for x in indata.split(',')]
    
    seeds = list(map(int, L[0][0].split()[1:]))
    maps = [np.array([list(map(int, l.split())) for l in block[1:]]) for block in L[1:]]

    # ----------- PART 1 -----------
    #
    def find_next(x, recipe):
        # map single value using a recipe (a set of ranges, and their transform)
        for r in recipe:
            if r[1] < x and x < r[1] + r[2]:
                return x - r[1] + r[0]
        return x
    x = seeds
    for recipe in maps:
        x = [find_next(_x, recipe) for _x in x]
    answer = min(x)
    print("Part 1: {}".format(answer))

    # ----------- PART 2 -----------
    #
    def find_next_ranges(x, recipe):
        # map single _range_ using a recipe (a set of ranges, and their transform)
        # ignore outside-of-recipe identity transforms
        y = []
        for r in recipe:
            min_in_range = max(x[0], r[1])
            max_in_range = min(x[0] + x[1], r[1] + r[2])
            if min_in_range < max_in_range:
                offset = - r[1] + r[0]
                y.append((min_in_range + offset, max_in_range - min_in_range))
        return y

    def find_outside_ranges(x, recipe):
        # make outside-of-recipe identity transforms on single range
        exclude = [(r[1], r[1] + r[2]) for r in recipe[np.argsort(recipe[:, 1]), :]]
        xrecipes = []
        if x[0] < exclude[0][0]:
            xrecipes.append([x[0], x[0], exclude[0][0] - x[0]])
        for i in range(1, len(exclude)):
            if exclude[i-1][1] < exclude[i][0]:
                xrecipes.append((exclude[i-1][1], exclude[i-1][1], exclude[i][0] - exclude[i-1][1]))
        if x[0] + x[1] > exclude[-1][1]:
            xrecipes.append([exclude[-1][1], exclude[-1][1], x[0] + x[1] - exclude[-1][1]])
        return find_next_ranges(x, xrecipes)

    # Interpret seeds as ranges instead
    x_ranges = list(zip(seeds[::2], seeds[1::2]))
    for recipe in maps:
        y = []
        for x in x_ranges:
            y.extend(find_next_ranges(x, recipe))
            y.extend(find_outside_ranges(x, recipe))
        x_ranges = y
    answer = min([x[0] for x in x_ranges])
    print("Part 2: {}".format(answer))


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
