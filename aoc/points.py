import numpy as np
from aoc import in_range

class Set2D:
    def __init__(self, x, y=None, values=None, colors=None, default_value=0, default_color='.', missing_color='%'):
        if y is not None:
            self.points = np.column_stack([x, y])
        else:
            self.points = np.array(x)
        assert self.points.ndim == 2 and self.points.shape[1] == 2, 'Wrong dim of x and y'
        assert np.issubdtype(self.points.dtype, np.integer), 'x and y must have integer-type'

        if values is not None:
            self.values = np.array(values)
            assert self.values.shape == (self.points.shape[0],)
        else:
            self.values = np.ones(self.points.shape[0], dtype=np.int32)
        
        if isinstance(colors, dict):
            self.colors = colors
        elif isinstance(colors, list) or isinstance(colors, str):
            self.colors = {i: c for i, c in enumerate(colors)}
        elif colors is None:
            self.colors = {0: '.', 1: '#'}
        else:
            raise ValueError('colors must be dict or list')
        self.default_value = default_value
        self.default_color = default_color
        self.missing_color = missing_color

        self.xlim = np.min(self.points[:, 0]), np.max(self.points[:, 0]) + 1
        self.ylim = np.min(self.points[:, 1]), np.max(self.points[:, 1]) + 1
    
    def __getitem__(self, index):
        return self.points[index, 0], self.points[index, 1], self.values[index]
    
    def __setitem__(self, index, entry):
        assert len(entry) == 3
        self.points[index, 0] = entry[0]
        self.points[index, 1] = entry[1]
        self.values[index] = entry[2]
    
    def __len__(self):
        return self.points.shape[0]

    @staticmethod
    def fromtext(text, colors=None, default_value=0, default_color='.', missing_color='%', ignore_colors='', missing_value=None, offset=(0, 0)):
        # Sanitize input
        if isinstance(text, str):
            text = text.splitlines(keepends=False)
        height = len(text)
        width = len(text[0])
        assert all([len(row) == width for row in text])

        # colors may be given as dict, list or None (use default)
        if isinstance(colors, dict):
            colors = colors
        elif isinstance(colors, list) or isinstance(colors, str):
            colors = {i: c for i, c in enumerate(colors)}
        elif colors is None:
            colors = {0: '.', 1: '#'}
        else:
            raise ValueError('colors must be dict or list')
        
        # Read text matrix
        value_from_color = {v: c for c, v in colors.items()}
        x, y, v = [], [], []
        for iy, row in enumerate(text):
            for ix, c in enumerate(row):
                if c == default_color or c in ignore_colors:
                    pass
                elif c in value_from_color:
                    x.append(ix + offset[0])
                    y.append(iy + offset[1])
                    v.append(value_from_color[c])
                elif missing_value is not None:
                    x.append(ix + offset[0])
                    y.append(iy + offset[1])
                    v.append(missing_value)

        # Create Set2D-object from imported data
        return Set2D(x, y, v, colors, default_value, default_color, missing_color)

    def image(self, xlim=None, ylim=None):
        xlim = xlim if xlim is not None else self.xlim
        ylim = ylim if ylim is not None else self.ylim

        width = self.xlim[1] - self.xlim[0]
        height = self.ylim[1] - self.ylim[0]
        assert width < 4096 and height < 4096, 'Too large! ({}x{} vs. 4096x4096)'.format(width, height)
        
        image = np.full((height, width), self.default_value)
        for xy, v in zip(self.points, self.values):
            if in_range(xy, [xlim[0], ylim[0]], [xlim[1], ylim[1]]):
                image[xy[1] - ylim[0], xy[0] - xlim[0]] = v
        return image

    def ascii(self, xlim=None, ylim=None):
        xlim = xlim if xlim is not None else self.xlim
        ylim = ylim if ylim is not None else self.ylim

        width = self.xlim[1] - self.xlim[0]
        height = self.ylim[1] - self.ylim[0]
        assert width < 200 and height < 500, 'Too large! ({}x{} vs. 200x500)'.format(width, height)

        image = np.full((height, width), self.default_color)
        for xy, v in zip(self.points, self.values):
            if in_range(xy, [xlim[0], ylim[0]], [xlim[1], ylim[1]]):
                image[xy[1] - ylim[0], xy[0] - xlim[0]] = self.colors.get(v, self.missing_color)
        image = [''.join(row) for row in image]

        return image

    def print(self, xlim=None, ylim=None):
        for row in self.ascii(xlim, ylim):
            print(row)