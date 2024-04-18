class Color:
    def __init__(self, r, g=None, b=None):
        if isinstance(r, (list, tuple)) and len(r) == 3 and g is None and b is None:
            self.r, self.g, self.b = r[0], r[1], r[2]
        else:
            self.r, self.g, self.b = r, g, b

    def __getitem__(self, index):
        if index == 0:
            return self.r
        elif index == 1:
            return self.g
        elif index == 2:
            return self.b
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.r = value
        elif index == 1:
            self.g = value
        elif index == 2:
            self.b = value
        else:
            raise IndexError("Index out of range")

    def get_color(self):
        return (self.r, self.g, self.b)
