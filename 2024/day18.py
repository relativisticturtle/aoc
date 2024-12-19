import numpy as np
import aoc
from PIL import Image

def run(indata):
    L = indata.splitlines(keepends=False)
    P = [tuple(map(int, l.split(','))) for l in L]
    
    # ----------- PART 1 -----------
    #
    
    # Let first 1024 bytes fall
    M = np.zeros((71, 71))
    for p in P[:1024]:
        M[p] = 1

    def adjacencies(p):
        adj = []
        for d in aoc.D4:
            q = p[0] + d[0], p[1] + d[1]
            if not aoc.in_range(q, M.shape):
                continue
            if M[q] == 0:
                adj.append(q)
        return adj
    
    s = aoc.search.Path(adjacencies).initial({(0,0)}).run()
    answer = s.result((70, 70))
    print("Part 1: {}".format(answer))
    
    # ----------- PART 2 -----------
    #

    # Re-init (for visualization)
    M = np.zeros((71, 71))
    s = aoc.search.Path(adjacencies).initial({(0,0)}).run()
    current_path = s.path_to((70, 70))
    
    images = []
    for p in P:
        M[p] = 1
        # Only do new path-search if byte falls on
        # previously established path
        if p in current_path:
            s = aoc.search.Path(adjacencies).initial({(0,0)}).run()
            if s.result((70, 70)) is None:
                # Finally, no path to exit anymore
                answer = '{},{}'.format(*p)
                break
        current_path = s.path_to((70, 70))

        # For visualization
        img = np.repeat(((1-M) * 255).astype(np.uint8)[..., np.newaxis], 3, axis=2)
        for q in current_path:
            img[q[0], q[1], :] = [255, 0, 0]
        images.append(img)

    for _ in range(5000):
        images.append(np.repeat(((1-M) * 255).astype(np.uint8)[..., np.newaxis], 3, axis=2))
    images = np.array(images).repeat(3, 1).repeat(3, 2)
    images = (Image.fromarray(img) for img in images[::20, ...])
    img0 = next(images)
    img0.save(
        '2024_18_p2.gif',
        format='GIF',
        append_images=images,
        save_all=True,
        duration=2,
        loop=0
    )

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
